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
from common.logger_utility import LoggerUtility
from common.framework_objects import EvaluationResult
from common.common_constants import ManagedCloudConstants, BotoConstants, ComplianceConstants, ResourceConstants, TagsConstants
from common.rds_constants import RdsConstants
from common.date_validation_util import DateValidationUtil
from common.RdsUtils import RdsUtils


class CheckRdsOwnerTagValuesAction(AbstractAction):
    """This class perform action as it stop Instances if it is non_compliant """
    def performAction(self, eventItem):
        evaluationResult = EvaluationResult()
        errorMessage = ""
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            rdsClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_RDS,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            actionMessage = ""
            response = False
            instanceStatus = eventItem.configItems[RdsConstants.RDS_STATE_REFERENCE]
            instanceIdentifier = eventItem.configItems[RdsConstants.RDS_INSTANCE_IDENTIFIER]
            if RdsUtils.isRdsMultiAZ(eventItem):
                multiAZ_Message = RdsConstants.MUTLI_AZ_RDS_ACTION_MESSAGE.format(instanceIdentifier)
                self._AbstractAction__actionMessage = _(multiAZ_Message)
                LoggerUtility.logInfo(multiAZ_Message)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = multiAZ_Message
                return evaluationResult

            elif instanceStatus == RdsConstants.RDS_AVAILABLE_STATE_REFERENCE and \
                    eventItem.configItems['engine'] != 'aurora':  # Aurora doesn't support start and stop
                response = RdsUtils.stopRdsInstance(rdsClient, instanceIdentifier, eventItem)
                actionMessage += str(eventItem.configItems['rdsStopActionMessage'])

            expirationDateLimit = int(self._AbstractAction__eventParam.configParam[ResourceConstants.RESOURCE_VALIDITY_RULE_PARAM])
            state = DateValidationUtil.updateEventActionBasedOnDate(eventItem, expirationDateLimit, TagsConstants.NO_OWNER_EXPIRATION_DATE_TAG_KEY)
            # Get number of remaining days from updated eventItem
            if eventItem.configItems.__contains__(ResourceConstants.RESOURCE_REMAINING_VALIDITY):
                validityRemaining = eventItem.configItems[ResourceConstants.RESOURCE_REMAINING_VALIDITY]

            if state in [ResourceConstants.RESOURCE_VALIDITY_EXPIRED]:
                response = RdsUtils.deleteRds(rdsClient, instanceIdentifier, eventItem)
                self._AbstractAction__actionMessage = _(eventItem.configItems['rdsDeleteActionMessage'])
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("Resource does not adhere taging standards.")

            elif state in [ResourceConstants.RESOURCE_EXPIRATION_DATE_INVALID, ResourceConstants.RESOURCE_EXPIRATION_DATE_LIMIT_EXCEEDED, ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND]:
                defaultValidity = int(self._AbstractAction__eventParam.configParam[ResourceConstants.RESOURCE_VALIDITY_RULE_PARAM])
                response = RdsUtils.addExpirationDateTag(rdsClient, defaultValidity, eventItem, TagsConstants.NO_OWNER_EXPIRATION_DATE_TAG_KEY)
                actionMessage += str(eventItem.configItems['addExpirationDateMessage'])
                self._AbstractAction__actionMessage = _(actionMessage)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("Resource does not have Owner tag to the resource. Adding expiration date.")

            elif state in [ResourceConstants.RESOURCE_ABOUT_TO_EXPIRE, ResourceConstants.RESOURCE_HAS_VALIDITY]:
                actionMessage += RdsConstants.RDS_EXPIRATION_REMAINING_DAYS.format(instanceIdentifier, validityRemaining)
                response = self._AbstractAction__actionMessage = _(actionMessage)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _(actionMessage)
                LoggerUtility.logInfo(actionMessage)

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
            errorMessage = "Error occured while deleting RDS instance. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            self._AbstractAction__actionMessage = _(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)

        return evaluationResult
