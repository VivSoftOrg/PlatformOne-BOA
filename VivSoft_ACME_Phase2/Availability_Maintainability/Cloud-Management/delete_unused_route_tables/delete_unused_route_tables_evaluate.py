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
""" This module will mark route table as Non-Compliant if they are not attached to any of the subnets. """
from common.abstract_evaluate import AbstractEvaluator
from common.common_constants import ResourceConstants
from common.common_constants import ComplianceConstants
from common.i18n import Translation as _
from common.framework_objects import EvaluationResult
from common.logger_utility import LoggerUtility


class DeleteUnusedRouteTablesEvaluate(AbstractEvaluator):
    """ This class will be responsible for evaluating the resources. """
    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        routeTableAssociations = eventItem.configItems[ResourceConstants.RESOURCE_ROUTE_TABLE_ASSOCIATIONS]

        if not routeTableAssociations:
            LoggerUtility.logInfo("Route table '{}' is not in use.".format(eventItem.resourceId))
            evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
            evaluationResult.annotation = _("Route table is not in use.")
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        else:
            LoggerUtility.logInfo("Route table '{}' is in use.".format(eventItem.resourceId))
            evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
            evaluationResult.annotation = _("Route table is in use.")
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        return evaluationResult
