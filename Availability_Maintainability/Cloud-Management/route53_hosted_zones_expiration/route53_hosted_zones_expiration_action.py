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
from common.framework_objects import EvaluationResult
from common.date_validation_util import DateValidationUtil
from common.common_constants import BotoConstants, ResourceConstants, ComplianceConstants, ActionMessages, TagsConstants
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from route53_hosted_zones_expiration.route53_hosted_zones_expiration_constants import Route53Constants


class HostedZoneExpirationAction(AbstractAction):
    """This class perform action if resource is non_compliant """
    def __deleteHostedZone(self, HZClient, eventItem):
        """this method will delete hosted zones"""
        try:
            response = HZClient.delete_hosted_zone(Id=eventItem.resourceId)
            deleteRequestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]

            if deleteRequestStatus == 200:
                self._AbstractAction__actionMessage = _("{} has been deleted".format(Route53Constants.RESOURCE_NAME))
                LoggerUtility.logInfo("{}: {} Deleted".format(Route53Constants.RESOURCE_NAME, eventItem.resourceId))
                return True

            else:
                errorMessage = ActionMessages.RESOURCE_ACTION_ERROR_MESSAGE.format(
                    'deleting',
                    eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME],
                    eventItem.resourceId,
                    deleteRequestStatus
                )
                self._AbstractAction__actionMessage = _(errorMessage)
                LoggerUtility.logError(errorMessage)
                return False

        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            return False
        except Exception as e:
            LoggerUtility.logError("Error occured while {}".format(e))
            return False

    def __addExpirationDateTag(self, HZClient, eventItem):
        """This method will add expirataion date tag to the resource if it does not satisfy validations."""
        defaultValidity = int(self._AbstractAction__eventParam.configParam[ResourceConstants.RESOURCE_VALIDITY_RULE_PARAM])
        expirationDate = DateValidationUtil.addDaysToToday(defaultValidity)

        expirationTag = [
            {
                'Key': TagsConstants.EXPIRATION_DATE_TAG_KEY,
                'Value': expirationDate
            }
        ]

        try:
            response = HZClient.change_tags_for_resource(
                ResourceType=Route53Constants.HOSTED_ZONES[:-1],
                ResourceId=eventItem.resourceId,
                AddTags=expirationTag
            )
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

        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            return False
        except Exception as e:
            LoggerUtility.logError("Error occured while {}".format(e))
            return False

    def performAction(self, eventItem):
        errorMessage = ""
        evaluationResult = EvaluationResult()
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            HZClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_ROUTE53,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName
            )

            response = False

            if eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_VALIDITY_EXPIRED:
                response = self.__deleteHostedZone(HZClient, eventItem)
                if response:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Route53 hosted zones deleted successfully")
                else:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Failed to delete Route53 hosted zones.")

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND or \
                    eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_DATE_LIMIT_EXCEEDED or \
                    eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_DATE_INVALID:
                response = self.__addExpirationDateTag(HZClient, eventItem)
                if response:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Expiration date added to Route53 hosted zones successfully")
                else:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Failed to add ExpirationDate on Route53 hosted zones.")
            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_ABOUT_TO_EXPIRE:
                response = self._AbstractAction__actionMessage = _(ActionMessages.RESOURCE_ABOUT_TO_EXPIRE)
                LoggerUtility.logInfo(ActionMessages.RESOURCE_ABOUT_TO_EXPIRE)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("Route53 hosted zones is about to expire. Update before get deleted.")

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
            errorMessage = "Error occured while deleting hosted zones. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            self._AbstractAction__actionMessage = _(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)
        else:
            LoggerUtility.logInfo(evaluationResult.annotation)

        return evaluationResult
