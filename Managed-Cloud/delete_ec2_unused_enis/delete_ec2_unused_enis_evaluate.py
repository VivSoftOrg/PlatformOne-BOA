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
from common.common_constants import ComplianceConstants, AWSResourceClassConstants
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from delete_ec2_unused_enis.delete_ec2_unused_enis_constants import Constants


class DeleteEC2UnusedENIsEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """

    def evaluate(self, eventItem):
        errorMessage = ""
        evaluationResult = EvaluationResult()
        try:
            if eventItem.resourceType not in AWSResourceClassConstants.ENI_RESOURCE:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The rule doesn't apply to resources of type {type} .").format(
                    type=eventItem.resourceType
                )
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

            elif eventItem.configItems['status'] == Constants.ENI_IN_USE_STATE_REFERENCE:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("The ENI is being used by some instance.")
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

            elif eventItem.configItems['status'] == Constants.ENI_AVAILABLE_STATE_REFERENCE:
                if 'RDSNetworkInterface' not in eventItem.configItems['description']:
                    LoggerUtility.logInfo('Found Unused ENI {}'.format(eventItem.resourceId))
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = ('This ENI is not being used by any instance')
                    recommendationMessage = "Since the ENI is not being used by any instance, associate it with any instance or it will get deleted."
                    self._AbstractEvaluator__recommendationMessage = _(recommendationMessage)
                    self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                else:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("The ENI is being used by some instance.")
                    self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

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
            errorMessage = "Error occured while evaluating unused ENIs. {}".format(e)
        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)
        return evaluationResult