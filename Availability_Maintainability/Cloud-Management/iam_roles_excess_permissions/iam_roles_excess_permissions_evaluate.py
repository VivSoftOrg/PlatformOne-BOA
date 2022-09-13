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
""" This module checks whether the iam user does not have excess permissions """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_evaluate import AbstractEvaluator
from common.common_utility import CommonUtility
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants, ComplianceConstants
from common.i18n import Translation as _
from common.framework_objects import EvaluationResult
from common_constants.exception_constants import ExceptionMessages
from iam_roles_excess_permissions.iam_roles_excess_permissions_constants import IamConstants


class IamRolesAccessPermissionsEvaluate(AbstractEvaluator):
    """ This class is responsible for evaluating resource as either Compliant or Non-compliant """

    def evaluate(self, eventItem):
        try:
            errorMessage = ""
            evaluationResult = EvaluationResult()
            rolesToExclude = self._AbstractEvaluator__eventParam.configParam[IamConstants.EXCLUDE_Roles].split(',')
            rolesToExclude = [role.strip() for role in rolesToExclude]
            if eventItem.configItems[IamConstants.ROLE_NAME] not in rolesToExclude:
                iamClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_IAM,
                    self._AbstractEvaluator__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    self._AbstractEvaluator__eventParam.awsPartitionName
                )
                policiesToCheck = [policy.lower().strip() for policy in self._AbstractEvaluator__eventParam.configParam[IamConstants.POLICY_NAMES].split(',')]
                foundPolicies = []

                eventItem.configItems.update({IamConstants.AWS_MANAGED_POLICIES: []})
                eventItem.configItems.update({IamConstants.INLINE_POLICIES: []})

                paginator = iamClient.get_paginator('list_attached_role_policies')
                operation_parameters = {"RoleName": eventItem.configItems[IamConstants.ROLE_NAME]}
                page_iterator = paginator.paginate(**operation_parameters)
                for page in page_iterator:
                    policies = CommonUtility.changeDictionaryKeysToLowerCase(page)
                    for policy in policies[IamConstants.ATTACHED_POLICIES]:
                        eventItem.configItems[IamConstants.AWS_MANAGED_POLICIES].append(policy)
                        if policy[IamConstants.POLICY_NAME].lower() in policiesToCheck:
                            foundPolicies.append(policy[IamConstants.POLICY_NAME])

                paginator = iamClient.get_paginator('list_role_policies')
                operation_parameters = {"RoleName": eventItem.configItems[IamConstants.ROLE_NAME]}
                page_iterator = paginator.paginate(**operation_parameters)
                for page in page_iterator:
                    policies = CommonUtility.changeDictionaryKeysToLowerCase(page)
                    for policy in policies[IamConstants.POLICY_NAMES]:
                        eventItem.configItems[IamConstants.INLINE_POLICIES].append(policy)

                eventItem.configItems.update({IamConstants.POLICY_NAMES: foundPolicies})
                if foundPolicies:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("The IAM role has more than minimal required permissions.")
                    LoggerUtility.logInfo("The IAM role {} has more than minimal required permissions.".format(eventItem.configItems[IamConstants.ROLE_NAME]))
                    self._AbstractEvaluator__recommendationMessage = "Please associate only minimal required access to the IAM roles."
                else:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("The role is compliant.")
            else:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("The role is excluded from evaluation.")

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
            errorMessage = "Error occured while evaluating for IAM roles excess permissions. {}".format(e)

        if errorMessage:
            LoggerUtility.logError(errorMessage)
            evaluationResult.annotation = errorMessage
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE

        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
