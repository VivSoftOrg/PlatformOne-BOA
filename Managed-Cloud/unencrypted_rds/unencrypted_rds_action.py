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
from common.abstract_action import AbstractAction
from common.framework_objects import EvaluationResult
from common.common_constants import ComplianceConstants


class UnencryptedRdsAction(AbstractAction):
    """This class returns action message if it is non_compliant """
    def performAction(self, eventItem):
        evaluationResult = EvaluationResult()

        evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
        evaluationResult.annotation = ("No Action required for unencrypted RDS.")
        self._AbstractAction__actionMessage = evaluationResult.annotation
        # No Action required for unencrypted RDS. We just need to notify the customer about the security gaps.
        return evaluationResult
