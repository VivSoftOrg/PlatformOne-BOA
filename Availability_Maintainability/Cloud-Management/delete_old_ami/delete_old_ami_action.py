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
from delete_old_ami.delete_old_ami_constants import AMIConstants


class DeleteOldAMIAction(AbstractAction):
    """This class perform action on AMIs, first deregister AMI and then delete snapshot if it is non_compliant """

    def performAction(self, eventItem):
        try:
            errorMessage = ""
            evaluationResult = EvaluationResult()

            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[AMIConstants.AWS_REGION]
            )

            imageId = eventItem.configItems[AMIConstants.Image_Id_Lower]
            snapIdList = [snap['ebs']['snapshotid'] for snap in eventItem.configItems['blockdevicemappings'] if 'ebs' in snap.keys()]

            deletedSnapshotIds = []
            notDeletedSnapshotIds = []

            responseDeregister = ec2Client.deregister_image(ImageId=imageId)

            if responseDeregister[AMIConstants.RESPONSE_METADATA][AMIConstants.HTTP_STATUS_CODE] == 200:
                LoggerUtility.logInfo("AMI id : {} deregistered successfully.".format(imageId))

                for snapId in snapIdList:
                    responseDeleteSnapshot = ec2Client.delete_snapshot(SnapshotId=snapId)
                    if responseDeleteSnapshot[AMIConstants.RESPONSE_METADATA][AMIConstants.HTTP_STATUS_CODE] == 200:
                        LoggerUtility.logInfo('AMI snapshot id : {} successfully deleted.'.format(snapId))
                        deletedSnapshotIds.append(snapId)
                    else:
                        LoggerUtility.logError('Unable to delete AMI snapshot id {} .'.format(snapId))
                        notDeletedSnapshotIds.append(snapId)

                if notDeletedSnapshotIds != []:
                    errorMessage = _("AMI id : {} deregistered successfully but unable to delete AMI snapshots with ids : {}.".format(imageId, notDeletedSnapshotIds))
                else:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                    evaluationResult.annotation = _("AMI id deregistered and related AMI snapshots are deleted successfully.")
                    LoggerUtility.logInfo(_("AMI id : {} deregistered and related AMI snapshots are deleted successfully.".format(imageId)))

            else:
                errorMessage = _("Unable to deregister AMI id : {} and hence associated AMI Snapshots are not deleted.".format(imageId))

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
            errorMessage = "Error occurred while performing an action for delete_old_ami rule. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)

        self._AbstractAction__actionMessage = evaluationResult.annotation
        return evaluationResult
