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

""" This module will fetch the resource details and send it to Evaluator.  """
from datetime import datetime
from dateutil.parser import parse

from botocore.exceptions import ClientError
from dateutil.relativedelta import relativedelta

from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.boto_utility import BotoUtility
from common.common_constants import (ActionMessages, AWSResourceClassConstants,
                                     BotoConstants, ComplianceConstants,
                                     ManagedCloudConstants, ResourceConstants)
from common.common_utility import CommonUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.date_validation_util import DateValidationUtil
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from rules_common.aws_resource_utility.rules_constants import RulesConstants, TagsConstants
from tag_validator.tag_validator_constants import Constants


class Ec2Utility():
    """ This class is created for processing EC2 resources using Boto Client"""

    def __init__(self, eventParam):
        self.eventParam = eventParam

    def __parseAndFetchInstanceDetails(self, instanceObject):
        """Method will fetch instance details and assign it to configItems."""
        resourceId = instanceObject[RulesConstants.EC2_INSTANCE_ID]
        configItems = instanceObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.EC2_INSTANCE, configItems=configItems)

    def fetchResources(self):
        ec2InstancesList = []
        try:
            awsPartitionName = self.eventParam.awsPartitionName
            regions = BotoUtility.getRegions(self.eventParam.accNo, awsPartitionName)
            for region in regions:
                ec2Client = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_EC2,
                    self.eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )
                LoggerUtility.logInfo('Fetching EC2 Instances in region: {}'.format(region))
                paginatorResponse = ec2Client.get_paginator('describe_instances')
                for response in paginatorResponse.paginate(Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped', 'pending']}]):
                    instanceResponse = CommonUtility.changeDictionaryKeysToLowerCase(response)
                    for reservation in instanceResponse[RulesConstants.RESPONSE_RESERVATIONS_REFERENCE]:
                        for instanceObject in reservation[RulesConstants.EC2_INSTANCES_REFERENCE]:
                            instanceObject.update({ManagedCloudConstants.REGION_REFERENCE: region})
                            eventItems = self.__parseAndFetchInstanceDetails(instanceObject)
                            if eventItems.configItems[RulesConstants.EC2_STATE_REFERENCE][RulesConstants.EC2_STATE_NAME] is not RulesConstants.EC2_TERMINATED_STATE_REFERENCE:
                                ec2InstancesList.append(eventItems)

        except ValueError as e:
            raise Exception("Failed to  fetch EC2 Instances. Error is {}".format(str(e)))

        return ec2InstancesList

    def __takeSnapshotOfVolume(self, ec2Client, eventItem, tagValues):
        """ This method fetches the volume id and creates the snapshot for that volume """
        try:
            anySnapshotFailed = False
            snapshotCreated = False
            snapshotIDs = []
            if 'blockdevicemappings' in eventItem.configItems.keys():
                blockdevicemappings = eventItem.configItems['blockdevicemappings']
                for mappings in blockdevicemappings:
                    if 'ebs' in mappings:
                        volumeID = mappings['ebs']['volumeid']

                        # Create snapshot
                        response = ec2Client.create_snapshot(
                            Description='Snapshot created for the volume: %s and of Instance: %s' % (volumeID, eventItem.resourceId),
                            VolumeId=volumeID,
                            TagSpecifications=[
                                {
                                    'ResourceType': 'snapshot',
                                    'Tags': [
                                        {
                                            'Key': 'Name',
                                            'Value': tagValues.get('Name', eventItem.resourceId)
                                        },
                                    ]
                                },
                            ]
                        )

                        if response[RulesConstants.STATUS_CODE_RESPONSE_METADATA][RulesConstants.HTTP_STATUS_CODE] == 200:
                            LoggerUtility.logInfo("Successfully created the snapshot with ID: {}".format(response['SnapshotId']))
                            snapshotIDs.append(response['SnapshotId'])
                            snapshotCreated = True
                        else:
                            LoggerUtility.logInfo("Unable to create the snapshot")
                            anySnapshotFailed = True

                if snapshotCreated and not anySnapshotFailed:
                    eventItem.configItems.update({'snapshotid': snapshotIDs})
                    return True
                else:
                    LoggerUtility.logInfo("Failed to create snapshot for all the attached volume")
                    return False
            else:
                LoggerUtility.logInfo("There is no volume attached to the instance")
                return False
        except Exception as e:
            LoggerUtility.logError(e)
            raise Exception("Failed to create snapshot for all the attached volume".format(e))

    def __disableAttachedAutoScalingGroups(self, autoScalingClient, eventItem):
        """ This method disbale the launch process of an attached auto scaling groups to an instance """
        try:
            responseASG = autoScalingClient.describe_auto_scaling_instances(InstanceIds=[eventItem.resourceId])
            if responseASG['AutoScalingInstances']:
                LoggerUtility.logInfo("Instance has an autoscaling group attached to it")
                for response in responseASG['AutoScalingInstances']:
                    suspendProcess = autoScalingClient.suspend_processes(AutoScalingGroupName=response['AutoScalingGroupName'], ScalingProcesses=['Launch', 'Terminate'])
                    if suspendProcess[RulesConstants.STATUS_CODE_RESPONSE_METADATA][RulesConstants.HTTP_STATUS_CODE] == 200:
                        LoggerUtility.logInfo("Successfully suspended the autoscaling process")
                        return True
                    else:
                        LoggerUtility.logInfo("Unable to suspend the  Launch and Terminate process of autoscaling group {}".format(response['AutoScalingGroupName']))
                        return False
            else:
                LoggerUtility.logInfo("There is no autoscaling group attached to the instance")
                return True
        except Exception as e:
            LoggerUtility.logError(e)
            LoggerUtility.logInfo("Unable to suspend the launch process of auto scaling group")
            raise Exception("Failed to disable autoscaling group".format(e))

    def __stopInstances(self, ec2Client, eventItem):
        """ This method will stop the instance. """
        try:
            if eventItem.configItems[RulesConstants.EC2_STATE_REFERENCE][RulesConstants.EC2_STATE_NAME] == RulesConstants.EC2_RUNNING_STATE_REFERENCE or eventItem.configItems[RulesConstants.EC2_STATE_REFERENCE][RulesConstants.EC2_STATE_NAME] == RulesConstants.EC2_PENDING_STATE_REFERENCE:
                response = ec2Client.stop_instances(
                    InstanceIds=[
                        eventItem.resourceId,
                    ], Force=True)
                return bool(response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200)
            else:
                LoggerUtility.logInfo("Instance is already stopped")
                return True

        except Exception as e:
            LoggerUtility.logError(e)
            raise Exception("Failed to stop instance ".format(e))
            return False

    def __terminateInstances(self, ec2Client, eventItem):
        """ This method terminate the ec2 instances """
        try:
            response = ec2Client.modify_instance_attribute(InstanceId=eventItem.resourceId, DisableApiTermination={'Value': False})
            if response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                response = ec2Client.terminate_instances(
                    InstanceIds=[
                        eventItem.resourceId,
                    ])
                return bool(response[RulesConstants.STATUS_CODE_RESPONSE_METADATA][RulesConstants.HTTP_STATUS_CODE] == 200)
            else:
                return False
        except Exception as e:
            LoggerUtility.logError(e)
            raise Exception("Failed to terminate instance".format(e))

    def __addRetentionPeriodTag(self, ec2Client, eventItem, tagKey, defaultValidity=0):
        """ This method will add ExpirationDate tag. """
        expirationDate = DateValidationUtil.addDaysToToday(defaultValidity)

        retentionPeriodTag = [
            {
                'Key': tagKey,
                'Value': expirationDate
            }
        ]

        try:
            response = ec2Client.create_tags(Resources=[eventItem.resourceId], Tags=retentionPeriodTag)

            requestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]
            if requestStatus == 200:
                self.actionMessages = _(ActionMessages.RESOURCE_EXPIRATION_TAG_ADDED)
                LoggerUtility.logInfo("RetentionPeriod tag has been successfully added to the resource")
                return True

            else:
                errorMessage = ActionMessages.RESOURCE_ACTION_ERROR_MESSAGE.format(
                    'adding RetentionPeriod Tag to',
                    eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME],
                    eventItem.resourceId,
                    requestStatus
                )
                self.actionMessages = _(errorMessage)
                self.evaluationResult.annotation = _(errorMessage)
                self.evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                LoggerUtility.logError(errorMessage)
                return False

        except Exception as e:
            LoggerUtility.logError(e)
            raise Exception("Failed to add retention period tags".format(e))

    def removeInstanceTag(self, instanceId, instanceRegion, tagKey):
        """ This method removes the retention period tag from the instance """
        try:
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self.eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                self.eventParam.awsPartitionName,
                instanceRegion
            )

            response = ec2Client.delete_tags(Resources=[instanceId], Tags=[{'Key': tagKey}])
            return bool(response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200)
        except Exception as e:
            LoggerUtility.logError(e)
            return False

    def executeTagNonComplianceAction(self, evaluationResult, eventItem):
        """ This method performs action on EC2 Instances tagged without Compliant Tags"""
        retentionPeriodDays = int(self.eventParam.configParam['RetentionPeriod'])
        self.evaluationResult = evaluationResult
        self.actionMessages = None
        errorMessage = ""
        stopInstance = False
        try:
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self.eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                self.eventParam.awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            autoScalingClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_ASC,
                self.eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                self.eventParam.awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            retentionPeriod = eventItem.configItems[TagsConstants.TAGS_REFERENCE].get('RetentionPeriod')
            if retentionPeriod:
                if parse(retentionPeriod).isoformat() <= datetime.now().isoformat():
                    LoggerUtility.logInfo("Instance has passed retentionPeriod and the Tags still does not adhere to organization standards.")

                    response = self.__disableAttachedAutoScalingGroups(autoScalingClient, eventItem)
                    if response:
                        response = self.__takeSnapshotOfVolume(ec2Client, eventItem, eventItem.configItems[TagsConstants.TAGS_REFERENCE])
                        msg = ""
                        if response:
                            LoggerUtility.logInfo("Successfully created the snapshot")
                            response = self.__terminateInstances(ec2Client, eventItem)
                            if response:
                                msg = "Instance has been terminated after creating Snaphots of all the attached EBS Volumes."
                                self.evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                            else:
                                msg = "Could not terminate the instance"
                                self.evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                        else:
                            msg = "Unable to create snapshot for the instance"
                            self.evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE

                        LoggerUtility.logInfo(msg)
                        self.actionMessages = _(msg)
                        self.evaluationResult.annotation = _(msg)
                    else:
                        msg = "Unable to suspend the launch and termination process of the auto scaling group"
                        LoggerUtility.logInfo(msg)
                        self.evaluationResult.annotation = _(msg)
                        self.evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE

                else:
                    LoggerUtility.logInfo("Instance will be terminated soon if the tags are not corrected.")
                    stopInstance = True

            else:
                response = self.__addRetentionPeriodTag(ec2Client, eventItem, Constants.RETENTION_PERIOD_TAG_KEY, retentionPeriodDays)
                stopInstance = True if response else False

            if stopInstance and self.__disableAttachedAutoScalingGroups(autoScalingClient, eventItem):
                msg = "Instance Stopped" if self.__stopInstances(ec2Client, eventItem) else "Could not stop instance"
                LoggerUtility.logInfo(msg)
                self.actionMessages = _(msg)
                self.evaluationResult.annotation = _(msg)
                self.evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is Invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type doesn't possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while taking action on Instance. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            self.evaluationResult.annotation = _(errorMessage)
            self.evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION

        return self.evaluationResult, self.actionMessages
