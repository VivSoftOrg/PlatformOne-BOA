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
""" Pefrom Action on Cloudwatch Event"""
from common.abstract_action import AbstractAction
from common.framework_objects import EvaluationResult
from common.common_constants import ComplianceConstants
from common.i18n import Translation as _


class ProcessCloudwatchEventsAction(AbstractAction):
    """ Pefrom Action on Cloudwatch Event"""
    def performAction(self, eventItem):
        """ perform action for the Cloudwatch events """
        evaluationResult = EvaluationResult()
        evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
        evaluationResult.annotation = _("This is sample action message for Cloudwatch Event")
        self._AbstractAction__actionMessage = evaluationResult.annotation

        return evaluationResult
