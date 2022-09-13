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
""" This module enables the delete on termination on the respective EBS Volumes. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants, EC2Constants, ComplianceConstants, ManagedCloudConstants
from common.framework_objects import EvaluationResult
from enable_delete_on_termination_ebs.enable_delete_on_termination_ebs_constants import Constants


class EnableDeleteOnTerminationEBSAction(AbstractAction):
    """ This class enables the delete on termination on the respective EBS Volumes. """
    def __modifyBlockDeviceMappings(self, mapping):
        """ This method will modify block device mapping. """
        blockDeviceMappings = [
            {
                'DeviceName': mapping[Constants.EC2_DEVICE_NAME],
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeId': mapping[Constants.EBS_VOLUME][EC2Constants.EBS_VOLUME_ID]
                }
            }
        ]
        return blockDeviceMappings

    def performAction(self, eventItem):
        evaluationResult = EvaluationResult()
        errorMessage = ""
        awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
        try:
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )
            actionSuccessfull = False
            for mappings in eventItem.configItems[Constants.EC2_BLOCK_DEVICE_MAPPINGS]:
                if not mappings[Constants.EBS_VOLUME][Constants.EBS_DELETE_ON_TERMINATION]:
                    BlockDeviceMappings = self.__modifyBlockDeviceMappings(mappings)
                    response = ec2Client.modify_instance_attribute(InstanceId=eventItem.resourceId, BlockDeviceMappings=BlockDeviceMappings)

                    status = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]

                    if status == 200:
                        LoggerUtility.logInfo("Enabled delete on termination for volume: {} attached to instance: {}".format(
                            mappings[Constants.EBS_VOLUME][EC2Constants.EBS_VOLUME_ID],
                            eventItem.resourceId))
                        evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                        evaluationResult.annotation = _("Enabled delete on termination")
                    else:
                        LoggerUtility.logInfo("Failed to modify the Instance Attribute. Error Code: {}".format(status))
                        evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                        evaluationResult.annotation = _("Enabled delete on termination")

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type which it doesn't possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error while occurred performing action for enabling delete on termination of EBS. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)
        else:
            LoggerUtility.logInfo(evaluationResult.annotation)

        self._AbstractAction__actionMessage = evaluationResult.annotation
        return evaluationResult
