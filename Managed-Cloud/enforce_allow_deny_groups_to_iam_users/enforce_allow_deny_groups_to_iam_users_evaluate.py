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
"""" This module will evaluate on the basis of a user is added to the default group. """
from datetime import datetime
from dateutil.tz import tzutc
from botocore.exceptions import ClientError
from enforce_allow_deny_groups_to_iam_users.enforce_allow_deny_groups_to_iam_users_constants import IamConstants
from common.logger_utility import LoggerUtility
from common.boto_utility import BotoUtility
from common.abstract_evaluate import AbstractEvaluator
from common.common_utility import CommonUtility
from common.common_constants import ComplianceConstants, BotoConstants, TagsConstants
from common.i18n import Translation as _
from common.framework_objects import EvaluationResult


class EnforceAllowAndDenyGroupsEvaluate(AbstractEvaluator):
    """ This class will evaluate on the basis of a user is added to the default group. """

    def __userHasLoginProfile(self, iamClient, eventItem):
        """ This method will check whether a user is present or not in an account. """
        try:
            loginProfile = iamClient.get_login_profile(UserName=eventItem.configItems[IamConstants.IAM_USER_NAME])
            if loginProfile:
                return True

        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            return False
        except Exception as e:
            LoggerUtility.logError("Error occured while checking login profile. {}".format(e))
            return False

    def __getAccessKeysLastUsedDate(self, iamClient, eventItem):
        """ This method will get access key last used a date. """
        response = CommonUtility.changeDictionaryKeysToLowerCase(iamClient.list_access_keys(
            UserName=eventItem.configItems[IamConstants.IAM_USER_NAME]))[IamConstants.ACCESS_KEY_METADATA]
        latestActivity = datetime(1, 1, 1, 1, tzinfo=tzutc())
        activityFound = False
        for accessKey in response:
            lastActivity = CommonUtility.changeDictionaryKeysToLowerCase(iamClient.get_access_key_last_used(
                AccessKeyId=accessKey[IamConstants.IAM_USER_ACCESS_KEY_ID]))[IamConstants.IAM_ACCESS_KEY_LAST_USED]
            if IamConstants.IAM_ACCESS_KEY_LAST_USED_DATE in lastActivity.keys():
                lastActivityDate = lastActivity[IamConstants.IAM_ACCESS_KEY_LAST_USED_DATE]
                latestActivity = lastActivityDate if lastActivityDate > latestActivity else latestActivity
                activityFound = True

        return latestActivity if activityFound else None

    def evaluate(self, eventItem):
        """ This method will evaluate resources. """
        evaluationResult = EvaluationResult()
        errorMessage = ""
        recommendationMessage = None
        try:
            eventItem.configItems.update({TagsConstants.TAG_LIST: [{TagsConstants.EC2_REQUIRED_TAG_KEY: 'Owner', TagsConstants.EC2_REQUIRED_TAG_VALUE: eventItem.configItems[IamConstants.IAM_USER_NAME]}]})
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            if eventItem.configItems[IamConstants.IAM_USER_NAME] not in self._AbstractEvaluator__eventParam.configParam[IamConstants.EXCLUDE_USERS].split(','):
                iamClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_IAM,
                    self._AbstractEvaluator__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName
                )

                groups = self._AbstractEvaluator__eventParam.configParam['groupsName'].split(',')
                groups = [role.strip() for role in groups]
                groupList = []
                groupsUser = []

                userHasLoginPassword = self.__userHasLoginProfile(iamClient, eventItem)
                response = self.__getAccessKeysLastUsedDate(iamClient, eventItem)
                accessKeyLastUsed = response if response else None

                if userHasLoginPassword:
                    eventItem.configItems.update({IamConstants.IAM_USER_HAS_PASSWORD_DISABLED: False})
                    if IamConstants.IAM_USER_PASSWORD_LAST_USED in eventItem.configItems.keys() and \
                            eventItem.configItems[IamConstants.IAM_USER_PASSWORD_LAST_USED]:
                        eventItem.configItems.update(
                            {IamConstants.IAM_USER_PASSWORD_LAST_USED: eventItem.configItems[IamConstants.IAM_USER_PASSWORD_LAST_USED].date().isoformat()})
                    else:
                        eventItem.configItems.update({IamConstants.IAM_USER_PASSWORD_LAST_USED: IamConstants.IAM_USER_NEVER_ACCESSED})
                else:
                    eventItem.configItems.update({IamConstants.IAM_USER_HAS_PASSWORD_DISABLED: True})
                    eventItem.configItems.update({IamConstants.IAM_USER_PASSWORD_LAST_USED: IamConstants.IAM_USER_NEVER_ACCESSED})
                eventItem.configItems.update({
                    IamConstants.IAM_ACCESS_KEY_LAST_USED: accessKeyLastUsed.date().isoformat() if accessKeyLastUsed else IamConstants.IAM_USER_NEVER_ACCESSED})
                userGroupList = CommonUtility.changeDictionaryKeysToLowerCase(
                    iamClient.list_groups_for_user(UserName=eventItem.configItems[IamConstants.IAM_USER_NAME]))

                for group in userGroupList[IamConstants.IAM_USER_GROUPS]:
                    groupsUser.append(group[IamConstants.IAM_GROUP_NAME])

                groupList = list(set(groups).difference(groupsUser))

                self._AbstractEvaluator__recommendationMessage = "These are the default permissions for every user."

                if not groupList:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("The user is added to the default IAM allow and deny groups.")
                else:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("The user is not added to the default IAM allow and deny groups")
                    recommendationMessage = "To ensure every user is having all the standard IAM permissions and do not access restricted resources, they must be added to these groups. "
                    eventItem.configItems.update({'Groups': groupList})

                self._AbstractEvaluator__recommendationMessage = recommendationMessage

            else:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("User {} is excluded for allow and deny groups.".format(eventItem.configItems[IamConstants.IAM_USER_NAME]))

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
            errorMessage = "Error occured while evaluating for enforce allow deny group to IAM users. {}".format(e)

        if errorMessage != "":
            evaluationResult.annotation = errorMessage
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            LoggerUtility.logError(evaluationResult.annotation)
        else:
            LoggerUtility.logInfo(evaluationResult.annotation)

        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
