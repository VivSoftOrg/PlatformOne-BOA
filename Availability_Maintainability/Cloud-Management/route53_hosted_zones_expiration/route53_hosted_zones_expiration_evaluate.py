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
from common.abstract_evaluate import AbstractEvaluator
from common.evaluation_result_factory import EvaluationResultFactory
from common.framework_objects import EvaluationResult
from common.logger_utility import LoggerUtility
from common.i18n import Translation as _
from common.common_constants import ResourceConstants, ComplianceConstants


class HostedZoneExpirationEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """
    def evaluate(self, eventItem):
        errorMessage = ""
        evaluationResult = EvaluationResult()
        try:

            expirationDateLimit = int(self._AbstractEvaluator__eventParam.configParam[ResourceConstants.RESOURCE_EXPIRATION_DATE_LIMIT_RULE_PARAM])
            response = EvaluationResultFactory.getEvaluationResultForExpirationDate(evaluationResult, expirationDateLimit, eventItem)
            evaluationResult = response['Result']
            if evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE:
                self._AbstractEvaluator__recommendationMessage = "Please add a valid ExpirationDate tag to prevent deletion of Route53 hosted zone."

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while evaluating user account. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)
        else:
            LoggerUtility.logInfo(evaluationResult.annotation)

        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
