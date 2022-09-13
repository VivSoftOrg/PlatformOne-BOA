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
"""
    This module will Evaluates checks target groups is associated with any ALB/NLB or not
"""
from common.abstract_evaluate import AbstractEvaluator
from common.common_constants import ComplianceConstants
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from rules_common.aws_resource_utility.rules_constants import RulesConstants
from common_constants.exception_constants import ExceptionMessages


class CheckTargetGroupAssociationWithAlbNlbEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will target groups associated with alb's on the basis of tags. """

    def evaluate(self, eventItem):
        """ This method evaluates target groups on basis they are associated with ALB/NLB """
        evaluationResult = EvaluationResult()
        errorMessage = ""
        try:
            if eventItem.configItems[RulesConstants.LOAD_BALANCER_ARNS]:
                evaluationResult.annotation = _("Target group is associated with any ALB/NLB")
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
            else:
                evaluationResult.annotation = _("Target group is not associated with any ALB/NLB")
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                LoggerUtility.logInfo("{} target group is not associated with any ALB or ELB".format(eventItem.resourceId))

            recommendationMessage = "It is recommended to delete unattached target groups"
            self._AbstractEvaluator__recommendationMessage = _(recommendationMessage)
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        except ValueError as e:
            errorMessage = ExceptionMessages.VALUE_ERROR.format(e)
        except AttributeError as e:
            errorMessage = ExceptionMessages.ATTRIBUTE_ERROR.format(e)
        except TypeError as e:
            errorMessage = ExceptionMessages.TYPE_ERROR.format(e)
        except NameError as e:
            errorMessage = ExceptionMessages.NAME_ERROR.format(e)
        except Exception as e:
            errorMessage = "Error occured while evaluating target group for association with ALB/NLB. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)

        return evaluationResult
