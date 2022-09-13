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
"""This module will Evaluate the Rule and mark resource as compliant or non_Compliant based on resource violations."""
from datetime import datetime, timedelta
from dateutil.tz import tzutc
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_evaluate import AbstractEvaluator
from common.common_utility import CommonUtility
from common.common_constants import BotoConstants, ComplianceConstants, TagsConstants
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from active_iam_users.active_iam_users_constants import IamConstants
from common_constants.exception_constants import ExceptionMessages


class ActiveIamUsersEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """

    def __userHasLoginProfile(self, iamClient, eventItem):
        """Method checks whether user has Login profile or not."""
        try:
            loginProfile = iamClient.get_login_profile(UserName=eventItem.configItems[IamConstants.IAM_USER_NAME])
            if loginProfile:
                return bool(True)
        except Exception as e:
            LoggerUtility.logError("failed to check for login profile of user. {}".format(e))
        return False

    def __getAccessKeysLastUsedDate(self, iamClient, eventItem):
        """Method returns access keys last used date."""
        try:
            response = CommonUtility.changeDictionaryKeysToLowerCase(iamClient.list_access_keys(UserName=eventItem.configItems[IamConstants.IAM_USER_NAME]))[IamConstants.ACCESS_KEY_METADATA]  # noqa
            latestActivity = datetime(1, 1, 1, 1, tzinfo=tzutc())
            activityFound = False
            for accessKey in response:
                lastActivity = CommonUtility.changeDictionaryKeysToLowerCase(iamClient.get_access_key_last_used(AccessKeyId=accessKey[IamConstants.IAM_USER_ACCESS_KEY_ID]))[IamConstants.IAM_ACCESS_KEY_LAST_USED]  # noqa
                if IamConstants.IAM_ACCESS_KEY_LAST_USED_DATE in lastActivity.keys():
                    lastActivityDate = lastActivity[IamConstants.IAM_ACCESS_KEY_LAST_USED_DATE]
                    latestActivity = lastActivityDate if lastActivityDate > latestActivity else latestActivity
                    activityFound = True
            return latestActivity if activityFound else None
        except Exception as e:
            LoggerUtility.logError("Failed to get last activity of user. {}".format(e))
            return None

    def evaluate(self, eventItem):
        errorMessage = ''
        try:
            evaluationResult = EvaluationResult()
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            iamClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_IAM,
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName
            )
            userHasLoginPassword = self.__userHasLoginProfile(iamClient, eventItem)
            todaysDate = datetime.now(tzutc())
            lastValidActivity = todaysDate - timedelta(days=int(self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_LAST_ACTIVITY_VALIDITY]))
            warningPeriod = lastValidActivity - timedelta(days=int(self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_DISABLE_WARNINGS]))
            deletePeriod = warningPeriod - timedelta(days=int(self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_DELETE_WARNINGS]))
            response = self.__getAccessKeysLastUsedDate(iamClient, eventItem)
            accessKeyLastUsed = response if response else None
            eventItem.configItems.update({TagsConstants.TAG_LIST: [{TagsConstants.EC2_REQUIRED_TAG_KEY: 'Owner', TagsConstants.EC2_REQUIRED_TAG_VALUE: eventItem.configItems[IamConstants.IAM_USER_NAME]}]})

            if userHasLoginPassword:
                eventItem.configItems.update({IamConstants.IAM_USER_HAS_PASSWORD_DISABLED: False})
                if IamConstants.IAM_USER_PASSWORD_LAST_USED in eventItem.configItems.keys() and eventItem.configItems[IamConstants.IAM_USER_PASSWORD_LAST_USED]:
                    lastUserActivity = max(accessKeyLastUsed, eventItem.configItems[IamConstants.IAM_USER_PASSWORD_LAST_USED]) if accessKeyLastUsed else eventItem.configItems[IamConstants.IAM_USER_PASSWORD_LAST_USED]  # noqa
                    eventItem.configItems.update({IamConstants.IAM_USER_PASSWORD_LAST_USED: eventItem.configItems[IamConstants.IAM_USER_PASSWORD_LAST_USED].date().isoformat()})  # noqa
                else:
                    lastUserActivity = accessKeyLastUsed if accessKeyLastUsed else eventItem.configItems[IamConstants.IAM_USER_CREATE_DATE]
                    eventItem.configItems.update({IamConstants.IAM_USER_PASSWORD_LAST_USED: IamConstants.IAM_USER_NEVER_ACCESSED})
            else:
                lastUserActivity = accessKeyLastUsed if accessKeyLastUsed else eventItem.configItems[IamConstants.IAM_USER_CREATE_DATE]
                eventItem.configItems.update({IamConstants.IAM_USER_HAS_PASSWORD_DISABLED: True})
                eventItem.configItems.update({IamConstants.IAM_USER_PASSWORD_LAST_USED: IamConstants.IAM_USER_NEVER_ACCESSED})

            eventItem.configItems.update({IamConstants.IAM_ACCESS_KEY_LAST_USED: accessKeyLastUsed.date().isoformat() if accessKeyLastUsed else IamConstants.IAM_USER_NEVER_ACCESSED})  # noqa

            if (lastUserActivity < deletePeriod) and not userHasLoginPassword:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                eventItem.configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: IamConstants.IAM_USER_DELETE})
                evaluationResult.annotation = _("The user has reached maximum number of inactive days allowed ({} days).").format(int(self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_LAST_ACTIVITY_VALIDITY]) + int(self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_DELETE_WARNINGS]) + int(self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_DISABLE_WARNINGS]))  # noqa
                self._AbstractEvaluator__evaluatorMessage = "The user account is not enabled and inactive since last {} days.".format(int(self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_LAST_ACTIVITY_VALIDITY]) + int(self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_DELETE_WARNINGS]) + int(self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_DISABLE_WARNINGS]))  # noqa
                LoggerUtility.logInfo("The user {} has reached maximum number of inactive days allowed.".format(eventItem.configItems[IamConstants.IAM_USER_NAME]))  # noqa
                self._AbstractEvaluator__recommendationMessage = "To prevent your account from getting deleted, please login to your account or use your API Keys."  # noqa

            elif lastUserActivity < warningPeriod:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                eventItem.configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: IamConstants.IAM_USER_DELETE_WARNINGS})
                eventItem.configItems.update({IamConstants.IAM_USER_DELETE_WARNINGS: (todaysDate + timedelta(days=((lastUserActivity - deletePeriod).days if (lastUserActivity - deletePeriod).days > 0 else 1))).date().isoformat()})  # noqa
                evaluationResult.annotation = _("The user account is not enabled and inactive since last {} days.".format(self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_LAST_ACTIVITY_VALIDITY]))  # noqa
                self._AbstractEvaluator__recommendationMessage = "Please login to your account in every 10 days, to prevent your account from getting deleted in future"  # noqa
                self._AbstractEvaluator__evaluatorMessage = "The user has reached maximum number of inactive days allowed {}".format(self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_LAST_ACTIVITY_VALIDITY])  # noqa
                LoggerUtility.logInfo("The user {} account is not enabled and inactive since last {} days.".format(eventItem.configItems[IamConstants.IAM_USER_NAME], self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_LAST_ACTIVITY_VALIDITY]))  # noqa

            elif lastUserActivity < lastValidActivity:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                eventItem.configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: IamConstants.IAM_USER_DISABLE_WARNINGS})
                eventItem.configItems.update({IamConstants.IAM_USER_DISABLE_WARNINGS: (todaysDate + timedelta(days=((lastUserActivity - deletePeriod).days if (lastUserActivity - warningPeriod).days > 0 else 1))).date().isoformat()})  # noqa
                evaluationResult.annotation = _("The user {} is inactive since last {} days.".format(eventItem.configItems[IamConstants.IAM_USER_NAME],
                                                                                                     self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_LAST_ACTIVITY_VALIDITY]))  # noqa
                self._AbstractEvaluator__recommendationMessage = "To prevent your account from getting disabled, please login to your account or use your API Keys."  # noqa
                self._AbstractEvaluator__evaluatorMessage = "The user is inactive since last {} days".format(self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_LAST_ACTIVITY_VALIDITY])  # noqa
                LoggerUtility.logInfo("The user {} is inactive since last {} days.".format(eventItem.configItems[IamConstants.IAM_USER_NAME], self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_LAST_ACTIVITY_VALIDITY]))  # noqa

            else:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("The user was active within last {} days.".format(self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_LAST_ACTIVITY_VALIDITY]))  # noqa
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                LoggerUtility.logInfo("The user {} was active within last {} days.".format(eventItem.configItems[IamConstants.IAM_USER_NAME], self._AbstractEvaluator__eventParam.configParam[IamConstants.IAM_USER_LAST_ACTIVITY_VALIDITY]))  # noqa

        except ValueError as e:
            errorMessage = ExceptionMessages.VALUE_ERROR.format(e)
        except AttributeError as e:
            errorMessage = ExceptionMessages.ATTRIBUTE_ERROR.format(e)
        except TypeError as e:
            errorMessage = ExceptionMessages.TYPE_ERROR.format(e)
        except NameError as e:
            errorMessage = ExceptionMessages.NAME_ERROR.format(e)
        except ClientError as e:
            errorMessage = ExceptionMessages.CLIENT_ERROR.format(e)
        except Exception as e:
            errorMessage = "Error occured while evaluating IAM user. {}".format(e)

        if errorMessage:
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = errorMessage

        return evaluationResult
