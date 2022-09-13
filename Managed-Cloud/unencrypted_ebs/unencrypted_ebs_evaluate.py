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
from common.common_constants import ComplianceConstants
from common.framework_objects import EvaluationResult
from common.logger_utility import LoggerUtility
from unencrypted_ebs.unencrypted_ebs_constants import EBSVolumeConstants


class UnencryptedEbsEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """
    def evaluate(self, eventItem):
        try:
            evaluationResult = EvaluationResult()

            if eventItem.configItems[EBSVolumeConstants.VOLUME_ENCRYPTED]:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = "The volume is encrypted"
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                LoggerUtility.logInfo("The volume {} is encrypted".format(eventItem.resourceId))

            else:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "The volume is not encrypted"
                self._AbstractEvaluator__recommendationMessage = "Please recreate the volume & enable encryption on it."
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                LoggerUtility.logInfo("The volume {} is not encrypted".format(eventItem.resourceId))

        except ValueError as e:
            LoggerUtility.logError("The content of the object you tried to assign the value is invalid. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = "The content of the object you tried to assign the value is invalid. {}".format(e)
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except AttributeError as e:
            LoggerUtility.logError("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except TypeError as e:
            LoggerUtility.logError("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except NameError as e:
            LoggerUtility.logError("Trying to access a variable that you have not defined properly. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = "Trying to access a variable that you have not defined properly. {}".format(e)
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = "Boto client error occured. {}".format(e)
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except Exception as e:
            LoggerUtility.logError("Error occured while evaluating unencrypted EBS. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = "Error occured while evaluating unencrypted EBS. {}".format(e)
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        return evaluationResult
