# REANCloud CONFIDENTIAL
# __________________
#
#  (C) 2018 REANCloud LLC
#  All Rights Reserved.
#
# NOTICE: All information contained herein is, and remains
# the property of REANCloud LLC and its suppliers,
# if any. The intellectual and technical concepts contained
# herein are proprietary to REANCloud LLC and its suppliers
# and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from REANCloud LLC.
""" This module adds an expiration tag to EC2 instances """
from datetime import datetime
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants
from common.common_constants import TagsConstants
from common.common_constants import ActionMessages
from common.common_constants import ComplianceConstants, ResourceConstants, ManagedCloudConstants
from common.framework_objects import EvaluationResult
from common.date_validation_util import DateValidationUtil
from common.i18n import Translation as _
from ec2_expiry_tag.ec2_expiry_tag_constants import Constants


class Ec2ExpiryTagAction(AbstractAction):
    """ This class performs an action if resource is non-compliant """

    def stopInstances(self, ec2Client, instanceID):
        """ This method will stop the instance. """
        response = ec2Client.stop_instances(
            InstanceIds=[
                instanceID,
            ]
        )

        if response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
            LoggerUtility.logInfo("Instance: {} successfully stopped".format(instanceID))
            return True
        else:
            LoggerUtility.logInfo("There was error stopping the instance: {}".format(instanceID))
            return False

    def terminateInstance(self, ec2Client, eventItem):
        """ This method will terminate the instance. """
        terminateInstanceMesssage = ""
        amiId = ""
        instanceID = eventItem.resourceId

        isInstanceType = eventItem.configItems.get('instancelifecycle', None)
        if isInstanceType != "spot":
            response = ec2Client.modify_instance_attribute(InstanceId=instanceID, DisableApiTermination={'Value': False})
            if response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                LoggerUtility.logInfo("Successfully Modified the attribute")
            else:
                terminateInstanceMesssage = "Error occoured while modifying attribute - DisableApiTermination"

        if not terminateInstanceMesssage:
            amiId, amiCreationError = self.createAMI(ec2Client, eventItem)
            if not amiCreationError:
                response = ec2Client.terminate_instances(
                    InstanceIds=[
                        instanceID,
                    ]
                )

                if response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                    LoggerUtility.logInfo("Instance: {} successfully terminated".format(instanceID))
                    terminateInstanceMesssage = Constants.EC2_SUCCESSFULLY_TERMINATED
                else:
                    terminateInstanceMesssage = "Error occured while terminating instance"
                    LoggerUtility.logInfo("There was error terminating the instance: {}".format(instanceID))
            else:
                terminateInstanceMesssage = "As errror occured while creating AMI, so we are not deleting instance"

        return terminateInstanceMesssage, amiId

    def addExpirationDateTag(self, ec2Client, eventItem, defaultValidity=0, spotTagKey='False'):
        """ This method will add ExpirationDate tag. """
        expirationDate = DateValidationUtil.addDaysToToday(defaultValidity)

        if spotTagKey == 'True':
            expirationTag = [
                {
                    'Key': spotTagKey,
                    'Value': expirationDate
                }
            ]
        else:
            expirationTag = [
                {
                    'Key': TagsConstants.EXPIRATION_DATE_TAG_KEY,
                    'Value': expirationDate
                }
            ]

        try:
            response = ec2Client.create_tags(Resources=[eventItem.resourceId], Tags=expirationTag)

            requestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]
            if requestStatus == 200:
                self._AbstractAction__actionMessage = _(ActionMessages.RESOURCE_EXPIRATION_TAG_ADDED)
                LoggerUtility.logInfo(ActionMessages.RESOURCE_EXPIRATION_TAG_ADDED)
                return True

            else:
                errorMessage = ActionMessages.RESOURCE_ACTION_ERROR_MESSAGE.format(
                    'adding Expiration Tag to',
                    eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME],
                    eventItem.resourceId,
                    requestStatus
                )
                self._AbstractAction__actionMessage = _(errorMessage)
                LoggerUtility.logError(errorMessage)
                return False

        except Exception as e:
            LoggerUtility.logError(e)

    def createAMI(self, ec2Client, eventItem):
        """ This method will create ami with resource id """
        instanceId = eventItem.resourceId
        mncTags = [
            {
                'Key': 'actionTakenByMNC',
                'Value': 'Instance Terminated and AMI created by EC2_Expiry_Tag rule'
            }, {
                'Key': 'complianceViolation',
                'Value': 'ExpriationDate is expirted'
            }, {
                'Key': 'instanaceId',
                'Value': instanceId
            }]

        amiId = ""
        amiCreationError = ""
        timeStamp = str(datetime.now()).replace(':', '.')
        amiName = ("Instance id - " + instanceId + " on " + timeStamp)
        try:
            amiResponse = ec2Client.create_image(InstanceId=instanceId, Name=amiName, Description="MNC created AMI from instance - " + instanceId + " for EC2 Expiration Date Validation Rule", NoReboot=True)
            if amiResponse['ResponseMetadata']['HTTPStatusCode'] == 200:
                amiId = amiResponse['ImageId']
                LoggerUtility.logInfo("Created AMI {}".format(amiId))
                if amiId:
                    tags = eventItem.configItems[TagsConstants.EC2_INSTANCE_TAGS]
                    formatedTags = []
                    if tags:
                        formatedTags = [{'Key': tag['key'], 'Value': tag['value']} for tag in tags]
                    formatedTags.extend(mncTags)
                    response = ec2Client.create_tags(Resources=[amiId], Tags=formatedTags)
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        LoggerUtility.logInfo("Tags added successfully to AMI Id - {}".format(amiId))
                    else:
                        amiCreationError = "Error occoured while adding tags to AMI Id - {}".format(amiId)
            else:
                amiCreationError = "Unable to create AMI for instance Id {}".format(instanceId)
        except ClientError as cliExp:
            amiCreationError = "Client error occoured while creating AMI for EC2 expiry tag - {}".format(cliExp)
        except Exception as expMessage:
            amiCreationError = "Error occoured while creating AMI for EC2 expiry tag - {}".format(expMessage)

        if amiCreationError:
            LoggerUtility.logError(amiCreationError)
        else:
            LoggerUtility.logInfo("AMI created successfully with name {}".format(amiName))

        return amiId, amiCreationError

    def performAction(self, eventItem):  # pylint:disable=R0912,R0915
        """ This class performs an action if resource is non-compliant """
        errorMessage = ""
        amiId = ""
        evaluationResult = EvaluationResult()
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            tagValues = {}
            if TagsConstants.EC2_INSTANCE_TAGS in eventItem.configItems:
                for tag in eventItem.configItems[TagsConstants.EC2_INSTANCE_TAGS]:
                    tagValues.update({tag[Constants.EC2_REQUIRED_TAG_KEY]: tag[Constants.EC2_REQUIRED_TAG_VALUE]})
            else:
                eventItem.configItems.update({TagsConstants.EC2_INSTANCE_TAGS: []})

            isInstanceType = eventItem.configItems.get('instancelifecycle', None)
            spot_tag_value = tagValues.get('True', None)
            limit_expiration_date = int(self._AbstractAction__eventParam.configParam[Constants.LIMIT_EXPIRTION_DATE_REFERENCE])
            response = False

            if eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_VALIDITY_EXPIRED:
                if eventItem.configItems['state']['name'] == 'running':
                    if isInstanceType == 'spot' and isInstanceType is not None:
                        response, amiId = self.terminateInstance(ec2Client, eventItem)

                        if response == Constants.EC2_SUCCESSFULLY_TERMINATED:
                            LoggerUtility.logInfo("Terminated the stopped spot instance: {}".format(eventItem.resourceId))
                            evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                        else:
                            LoggerUtility.logInfo("Unable to terminate the stopped spot instance: {}".format(eventItem.resourceId))
                            evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                        evaluationResult.annotation = response

                    else:
                        response = self.stopInstances(ec2Client, eventItem.resourceId)

                        if response:
                            expirationDays = int(self._AbstractAction__eventParam.configParam[Constants.EXPIRATION_DAYS])
                            response = self.addExpirationDateTag(ec2Client, eventItem, expirationDays)
                            LoggerUtility.logInfo("Stopped the instance: {}".format(eventItem.resourceId))
                            evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                            evaluationResult.annotation = "Stopped the instance"
                        else:
                            LoggerUtility.logInfo("Unable to stop the instance: {}".format(eventItem.resourceId))
                            evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                            evaluationResult.annotation = "Unable to stop the instance"

                elif eventItem.configItems['state']['name'] == 'stopped':
                    response, amiId = self.terminateInstance(ec2Client, eventItem)

                    if response == Constants.EC2_SUCCESSFULLY_TERMINATED:
                        LoggerUtility.logInfo("Terminated the instance: {}".format(eventItem.resourceId))
                        evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    else:
                        LoggerUtility.logInfo("Unable to terminate the instance: {}".format(eventItem.resourceId))
                        evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = response

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_ABOUT_TO_EXPIRE:
                LoggerUtility.logInfo("Instance {} will get expire in {} days".format(eventItem.resourceId, eventItem.configItems[ResourceConstants.RESOURCE_REMAINING_VALIDITY]))
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "Instance will get expire in {} days".format(eventItem.configItems[ResourceConstants.RESOURCE_REMAINING_VALIDITY])

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] != ComplianceConstants.UNABLE_TO_CHECK_RESOURCE_COMPLIANCE:
                response = self.addExpirationDateTag(ec2Client, eventItem, limit_expiration_date)

                if response:
                    LoggerUtility.logInfo("Added tag to the instance")
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = "Added tag to the instance."
                else:
                    LoggerUtility.logInfo("Unable to add tag to the instances")
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = "Unable to add tag to the instance"

            if amiId:
                eventItem.configItems.update({"amiid": amiId})

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while performing action for ec2_expiry_tag rule. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.annotation = errorMessage
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION

        self._AbstractAction__actionMessage = evaluationResult.annotation
        return evaluationResult
