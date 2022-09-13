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
""" This module will add available defined security groups to the instance """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.i18n import Translation as _
from common.abstract_action import AbstractAction
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants, ActionMessages, ComplianceConstants, ManagedCloudConstants
from common.framework_objects import EvaluationResult
from attach_security_group_to_all_instances.attach_security_group_to_all_instances_constants import Constants


class AttachSecurityGroupToInstancesAction(AbstractAction):
    """ This class will add available defined security groups to the instance """
    def performAction(self, eventItem):
        errorMessage = ""
        try:
            evaluationResult = EvaluationResult()
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            if Constants.ATTACH_GROUPS in eventItem.configItems.keys():
                currentSecurityGroups = [securityGroup[Constants.GROUP_ID] for securityGroup in eventItem.configItems[Constants.SECURITY_GROUPS]]
                response = ec2Client.modify_instance_attribute(
                    Groups=eventItem.configItems[Constants.ATTACH_GROUPS].split(',') + currentSecurityGroups, InstanceId=eventItem.resourceId)
                requestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]
            else:
                requestStatus = 200

            if requestStatus == 200:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = ('Added available defined security groups to the instance.')
            else:
                errorMessage = ActionMessages.RESOURCE_ACTION_ERROR_MESSAGE.format(
                    'attaching security group to', 'instance',
                    eventItem.resourceId,
                    requestStatus
                )
                self._AbstractAction__actionMessage = _(errorMessage)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = ('Unable to add available defined security groups to the instance.')

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type doesn't possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while performing action on attaching security group to all instances. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)
        else:
            LoggerUtility.logInfo(evaluationResult.annotation)

        self._AbstractAction__actionMessage = evaluationResult.annotation
        return evaluationResult
