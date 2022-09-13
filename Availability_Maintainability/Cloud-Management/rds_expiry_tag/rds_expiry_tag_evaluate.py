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
""" This module evaluates RDS instances """
from botocore.exceptions import ClientError
from common.common_constants import ComplianceConstants
from common.abstract_evaluate import AbstractEvaluator
from common.framework_objects import EvaluationResult
from common.logger_utility import LoggerUtility
from common.i18n import Translation as _
from common.evaluation_result_factory import EvaluationResultFactory
from rds_expiry_tag.rds_expiry_tag_constants import Constants


class RdsExpiryTagEvaluate(AbstractEvaluator):
    """ This class is responsible for evaluating resource as either Compliant or Non-compliant """

    def evaluate(self, eventItem):
        """ This method is used to evaluate the resources """
        evaluationResult = EvaluationResult()

        try:
            limit_expiration_date = int(self._AbstractEvaluator__eventParam.configParam[Constants.LIMIT_EXPIRTION_DATE_REFERENCE])
            response = EvaluationResultFactory.getEvaluationResultForExpirationDate(evaluationResult, limit_expiration_date, eventItem)
            evaluationResult = response['Result']
            self._AbstractEvaluator__recommendationMessage = 'Kindly make sure that the expiration date is under valid no of days to avoid stopping of your instance.'
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        except ValueError as e:
            LoggerUtility.logError("The content of the object you tried to assign the value is invalid. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("The content of the object you tried to assign the value is invalid. {}".format(e))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except AttributeError as e:
            LoggerUtility.logError("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except TypeError as e:
            LoggerUtility.logError("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except NameError as e:
            LoggerUtility.logError("Trying to access a variable that you have not defined properly. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Trying to access a variable that you have not defined properly. {}".format(e))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Boto client error occured. {}".format(e))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except Exception as e:
            LoggerUtility.logError("Error occured. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Error occured. {}".format(e))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        return evaluationResult
