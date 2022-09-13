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
"""This module will Evaluate the Rule and mark resource as compliant or non_Compliant based on behaviour."""
from botocore.exceptions import ClientError

from common.abstract_evaluate import AbstractEvaluator
from common.boto_utility import BotoUtility
from common.common_constants import BotoConstants, ComplianceConstants, TagsConstants
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from detach_iam_policy.detach_iam_policy_constants import Constants


class DetachIamPolicyEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """

    def isInlinePolicies(self, iamClient, eventItem):
        """ This method fetches the inline policies attached to the user """
        inlinePolicies = []
        try:
            response = iamClient.list_user_policies(
                UserName=self.__userName
            )

            for policy in response['PolicyNames']:
                inlinePolicies.append(policy)

            return inlinePolicies
        except Exception as e:
            LoggerUtility.logError(e)

    def isAttachedManagedPolicies(self, iamClient, eventItem):
        """ This method fetches the any attached managed policies for the user """
        managedPolicies = []
        try:
            response = iamClient.list_attached_user_policies(
                UserName=self.__userName
            )

            for attachedPolicies in response['AttachedPolicies']:
                managedPolicies.append(attachedPolicies['PolicyArn'])

            return managedPolicies
        except Exception as e:
            LoggerUtility.logError(e)

    def evaluate(self, eventItem):
        """ This method will evaluate all the IAM user policies """
        self.__userName = eventItem.configItems['username']

        evaluationResult = EvaluationResult()
        try:
            excludeUser = self._AbstractEvaluator__eventParam.configParam['excludeUser']
            excludeUser = [item.strip() for item in excludeUser.split(',')]
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            iamClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_IAM,
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName
            )

            eventItem.configItems.update({TagsConstants.TAG_LIST: [{TagsConstants.EC2_REQUIRED_TAG_KEY: 'Owner', TagsConstants.EC2_REQUIRED_TAG_VALUE: eventItem.configItems['username']}]})
            inlinePolicies = self.isInlinePolicies(iamClient, eventItem)

            managedPolicies = self.isAttachedManagedPolicies(iamClient, eventItem)

            if self.__userName not in excludeUser:
                if (inlinePolicies or managedPolicies):
                    LoggerUtility.logInfo("The user '%s' have external policies attached." % self.__userName)
                    evaluationResult.annotation = _("The user have external policies attached to it.")
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    if inlinePolicies:
                        eventItem.configItems.update({Constants.INLINE_POLICIES: inlinePolicies})

                    if managedPolicies:
                        eventItem.configItems.update({Constants.MANAGED_POLICIES: managedPolicies})
                    recommendationMessage = "As AWS best security practices,it is important that all IAM users have policy only attached through groups."
                    self._AbstractEvaluator__recommendationMessage = _(recommendationMessage)
                else:
                    LoggerUtility.logInfo("The user '%s' does not have external policies attached." % self.__userName)
                    evaluationResult.annotation = _("The user does not have external policies attached to it.")
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    recommendationMessage = "As AWS best security practices,it is important that all IAM users have policy only attached through groups."
                    self._AbstractEvaluator__recommendationMessage = _(recommendationMessage)
            else:
                LoggerUtility.logInfo("User %s is excluded from the evaluation" % self.__userName)
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The user is excluded from the evaluation.")

            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        except ValueError as e:
            LoggerUtility.logError("The content of the object you tried to assign the value is invalid. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("The content of the object you tried to assign the value is invalid. {}".format(e))
        except AttributeError as e:
            LoggerUtility.logError("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
        except TypeError as e:
            LoggerUtility.logError("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
        except NameError as e:
            LoggerUtility.logError("Trying to access a variable that you have not defined properly. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Trying to access a variable that you have not defined properly. {}".format(e))
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Boto client error occured. {}".format(e))
        except Exception as e:
            LoggerUtility.logError("Error occured while evaluating user account. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Error occured while evaluating user account. {}".format(e))

        return evaluationResult
