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

from common.abstract_action import AbstractAction
from common.boto_utility import BotoUtility
from common.common_constants import BotoConstants, ComplianceConstants
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from detach_iam_policy.detach_iam_policy_constants import Constants


class DetachIamPolicyAction(AbstractAction):
    """This class perform action if resource is non_compliant """

    def deleteInlinePolicies(self, iamClient, eventItem):
        """ This method is used to delete inline policies attached to the user """
        allInlinePoliciesDeleted = False
        anyPoliciesFailed = False

        try:
            if Constants.INLINE_POLICIES in eventItem.configItems:
                for inlinePolicy in eventItem.configItems[Constants.INLINE_POLICIES]:
                    response = iamClient.delete_user_policy(
                        UserName=self.__userName,
                        PolicyName=inlinePolicy
                    )

                    # pylint:disable= R1703
                    if response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                        allInlinePoliciesDeleted = True
                    else:
                        anyPoliciesFailed = True

                return bool(allInlinePoliciesDeleted and not anyPoliciesFailed)
            else:
                return True

        except Exception as e:
            LoggerUtility.logError(e)

    def detachManagedPolicies(self, iamClient, eventItem):
        """ This method is used to delete external managed policies attached to the user """
        allManagedPoliciesDetached = False
        anyPoliciesFailed = False

        try:
            if Constants.MANAGED_POLICIES in eventItem.configItems:
                for managedPolicy in eventItem.configItems[Constants.MANAGED_POLICIES]:
                    response = iamClient.detach_user_policy(
                        UserName=self.__userName,
                        PolicyArn=managedPolicy
                    )

                    # pylint:disable= R1703
                    if response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                        allManagedPoliciesDetached = True
                    else:
                        anyPoliciesFailed = True

                return bool(allManagedPoliciesDetached and not anyPoliciesFailed)
            else:
                return True

        except Exception as e:
            LoggerUtility.logError(e)

    def performAction(self, eventItem):
        """ This method will take action on all the NON_COMPLIANT resources """
        evaluationResult = EvaluationResult()
        self._AbstractAction__actionMessage = _("")
        self.__userName = eventItem.configItems['username']

        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            iamClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_IAM,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName
            )

            inlinePoliciesDeleted = self.deleteInlinePolicies(iamClient, eventItem)

            managedPoliciesDetached = self.detachManagedPolicies(iamClient, eventItem)

            if inlinePoliciesDeleted and managedPoliciesDetached:
                LoggerUtility.logInfo("Successfully revoked all the external policies attached to the user")
                evaluationResult.annotation = "Successfully revoked all the external policies attached to the user"
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                self._AbstractAction__actionMessage = _("All the external policies have been revoked from the user.")
            else:
                LoggerUtility.logInfo("Unable to revoke all the external policies attached to the user")
                evaluationResult.annotation = "Unable to revoke all the external policies attached to the user"
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                self._AbstractAction__actionMessage = _("Unable to revoke all the external policies attached to the user.")

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
            LoggerUtility.logError("Error occured while deleting user profile. {}".format(e))
            self._AbstractAction__actionMessage = _("Error occured while deleting user profile. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _("Error occured while deleting user profile. {}".format(e))

        return evaluationResult
