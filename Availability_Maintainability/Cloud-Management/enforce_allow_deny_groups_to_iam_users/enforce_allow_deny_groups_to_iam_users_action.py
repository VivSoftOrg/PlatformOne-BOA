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
""" This module will add users to default IAM group. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants, ComplianceConstants, ActionMessages
from common.framework_objects import EvaluationResult
from enforce_allow_deny_groups_to_iam_users.enforce_allow_deny_groups_to_iam_users_constants import IamConstants


class EnforceAllowAndDenyGroupsAction(AbstractAction):
    """ This class will add users to default IAM group. """
    def performAction(self, eventItem):
        errorMessage = ""
        evaluationResult = EvaluationResult()
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            iamClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_IAM,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName
            )
            failedToAddAnyGroup = False
            addedToGroup = False

            for group in eventItem.configItems["Groups"]:
                try:
                    response = iamClient.add_user_to_group(
                        GroupName=group,
                        UserName=eventItem.configItems[IamConstants.IAM_USER_NAME])
                    requestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] if \
                        BotoConstants.BOTO_RESPONSE_METADATA in response else 0
                    if requestStatus == 200:
                        LoggerUtility.logInfo("Added to group: {}".format(group))
                        addedToGroup = True
                    else:
                        actionErrorMessage = ActionMessages.RESOURCE_ACTION_ERROR_MESSAGE.format(
                            'adding user to the ', 'group', group, requestStatus)
                        LoggerUtility.logError(actionErrorMessage)
                        failedToAddAnyGroup = True
                except ClientError as e:
                    LoggerUtility.logError("Boto client error occured. {}".format(e))
                except Exception as e:
                    LoggerUtility.logError("Error occured while adding user to IAM allow and deny group. {}".format(e))

            if addedToGroup and not failedToAddAnyGroup:
                evaluationResult.annotation = _("Added user to default IAM Groups.")
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
            else:
                evaluationResult.annotation = _("Failed To Add user to Default IAM allow & deny groups.")
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE

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
            errorMessage = "Error occured while disabling IAM user account. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)
        else:
            LoggerUtility.logInfo(evaluationResult.annotation)

        self._AbstractAction__actionMessage = evaluationResult.annotation
        return evaluationResult
