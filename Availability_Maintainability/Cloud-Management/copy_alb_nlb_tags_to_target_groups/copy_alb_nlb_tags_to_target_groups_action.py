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
from common.common_constants import ComplianceConstants
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from rules_common.aws_resource_utilities.elbv2_utility import Elbv2Utility
from copy_alb_nlb_tags_to_target_groups.copy_alb_nlb_tags_to_target_groups_constants import ALBConstants


class CopyAlbNlbTagsToTargetGroupsAction(AbstractAction):
    """This class will copy tags from ALB or NLB to there target groups if it is non_compliant """

    def performAction(self, eventItem):
        """ This method add tags to target groups which are missing. """

        errorMessage = ""
        try:
            evaluationResult = EvaluationResult()
            evaluationResult = Elbv2Utility.addTagsToResource(eventParam=self._AbstractAction__eventParam, eventItem=eventItem, resourceListWithTags=eventItem.configItems[ALBConstants.MISSING_TAGS_TARGET_GROUPS])
            self._AbstractAction__actionMessage = evaluationResult.annotation

        except Exception as e:
            errorMessage = "Error occured while adding tags. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)

        return evaluationResult
