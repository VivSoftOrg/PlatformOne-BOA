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
""" This module will does not perform any action on snapshot if they are unencrypted. """
from common.abstract_action import AbstractAction
from common.framework_objects import EvaluationResult
from common.common_constants import ComplianceConstants


class UnencryptedSnapshotAction(AbstractAction):
    """ This class will be responsible for performing action if the resource is non-compliant. """
    def performAction(self, eventItem):
        evaluationResult = EvaluationResult()
        self._AbstractAction__actionMessage = None
        evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
        evaluationResult.annotation = "Please recreate the snapshot & enable encryption on it."
        return evaluationResult
        # No Action required for unencrypted Snapshots. We just need to notify the customer about the security gaps.
