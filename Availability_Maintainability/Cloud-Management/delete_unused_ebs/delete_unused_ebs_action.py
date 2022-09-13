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
"""This module will perform action based on the Evaluation Result."""
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.i18n import Translation as _
from common.framework_objects import EvaluationResult
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants, ComplianceConstants
from delete_unused_ebs.delete_unused_ebs_constants import EBSVolumeConstants


class DeleteUnusedEBSAction(AbstractAction):
    """This class perform action as it stop Instances if it is non_compliant """
    def __findNameTag(self, eventItem):
        """ Method is to find name tag."""
        try:
            if EBSVolumeConstants.TAGS in eventItem.configItems.keys():
                for tag in eventItem.configItems[EBSVolumeConstants.TAGS]:
                    if tag[EBSVolumeConstants.TAG_KEY] == EBSVolumeConstants.NAME_TAG:
                        return tag[EBSVolumeConstants.TAG_VALUE]

            return False
        except Exception as e:
            LoggerUtility.logError("Error occured while fetching volume name. {}".format(e))
            return False

    def performAction(self, eventItem):
        try:
            evaluationResult = EvaluationResult()

            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[EBSVolumeConstants.AWS_REGION]
            )

            nameTag = self.__findNameTag(eventItem)
            snapDescription = eventItem.resourceId

            if nameTag:
                snapDescription = nameTag + "--" + eventItem.resourceId
            response = ec2Client.create_snapshot(Description=snapDescription,
                                                 VolumeId=eventItem.resourceId)

            if response[EBSVolumeConstants.EBS_RESPONSE_METADATA][EBSVolumeConstants.EBS_HTTP_STATUS_CODE] == 200:
                LoggerUtility.logInfo("Snapshot creation was successful for volume: {}".format(eventItem.resourceId))
                deleteResponse = ec2Client.delete_volume(VolumeId=eventItem.resourceId)
                if deleteResponse[EBSVolumeConstants.EBS_RESPONSE_METADATA][EBSVolumeConstants.EBS_HTTP_STATUS_CODE] == 200:
                    LoggerUtility.logInfo("Volume: {} successfully deleted".format(eventItem.resourceId))
                    self._AbstractAction__actionMessage = _("The unattached EBS volumes are deleted.")
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = ('EBS volume is deleted successfully which makes it COMPLIANT_RESOURCE.')
                else:
                    self._AbstractAction__actionMessage = _("Error deleting volume: {}, HTTPStatus Code : {}." /
                                                            + format(eventItem.resourceId,
                                                                     response[EBSVolumeConstants.EBS_RESPONSE_METADATA]
                                                                     [EBSVolumeConstants.EBS_HTTP_STATUS_CODE]))
                    LoggerUtility.logError("Error deleting volume: {}, HTTPStatus Code : {}." /
                                           + format(eventItem.resourceId,
                                                    response[EBSVolumeConstants.EBS_RESPONSE_METADATA]
                                                    [EBSVolumeConstants.EBS_HTTP_STATUS_CODE]))
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = ("Failed to delete EBS volume")
            else:
                self._AbstractAction__actionMessage = _("Error creating snapshot of the volume: {}, HTTPStatus Code : {}." /
                                                        + format(eventItem.resourceId,
                                                                 response[EBSVolumeConstants.EBS_RESPONSE_METADATA]
                                                                 [EBSVolumeConstants.EBS_HTTP_STATUS_CODE]))
                LoggerUtility.logError("Error creating snapshot of the volume: {}, HTTPStatus Code : {}." /
                                       + format(eventItem.resourceId,
                                                response[EBSVolumeConstants.EBS_RESPONSE_METADATA]
                                                [EBSVolumeConstants.EBS_HTTP_STATUS_CODE]))
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = ('EBS volume is not attached to any instance. Not deleted successfully which makes it NON_COMPLIANT_RESOURCE.')

        except ValueError as e:
            LoggerUtility.logError("The content of the object you tried to assign the value is invalid. {}".format(e))
            self._AbstractAction__actionMessage = _("The content of the object you tried to assign the value is invalid. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _("The content of the object you tried to assign the value is invalid. {}".format(e))
        except AttributeError as e:
            LoggerUtility.logError("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
            self._AbstractAction__actionMessage = _("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
        except TypeError as e:
            LoggerUtility.logError("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
            self._AbstractAction__actionMessage = _("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
        except NameError as e:
            LoggerUtility.logError("Trying to access a variable that you have not defined properly. {}".format(e))
            self._AbstractAction__actionMessage = _("Trying to access a variable that you have not defined properly. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _("Trying to access a variable that you have not defined properly. {}".format(e))
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            self._AbstractAction__actionMessage = _("Boto client error occured. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _("Boto client error occured. {}".format(e))
        except Exception as e:
            LoggerUtility.logError("Error occured while deleting EBS volumes. {}".format(e))
            self._AbstractAction__actionMessage = _("Error occured while deleting EBS volumes. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _("Error occured while deleting EBS volumes. {}".format(e))

        return evaluationResult
