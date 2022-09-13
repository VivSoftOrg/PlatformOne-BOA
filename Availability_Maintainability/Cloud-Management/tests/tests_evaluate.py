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
"""test module for Evaluate."""
from common.abstract_evaluate import AbstractEvaluator
from common.common_constants import ComplianceConstants
from common.framework_objects import EvaluationResult


class Evaluate(AbstractEvaluator):
    """test class for evaluate."""
    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
        evaluationResult.annotation = "This resource is not compliant with the rule."
        self._AbstractEvaluator__evaluatorMessage.message = evaluationResult.annotation
        return evaluationResult
