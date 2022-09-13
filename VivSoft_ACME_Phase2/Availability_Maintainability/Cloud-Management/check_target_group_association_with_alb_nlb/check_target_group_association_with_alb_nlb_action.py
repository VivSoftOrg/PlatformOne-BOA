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
from rules_common.aws_resource_utility.elbv2_utility import Elbv2Utility


class CheckTargetGroupAssociationWithAlbNlbAction(AbstractAction):
    """This class delete target group if it is non_compliant """

    def performAction(self, eventItem):
        """ This method will delete non compliant target group. """

        eventParam = self._AbstractAction__eventParam
        evaluationResult = Elbv2Utility.deleteTargetGroup(eventParam, eventItem)

        self._AbstractAction__actionMessage = evaluationResult.annotation
        return evaluationResult
