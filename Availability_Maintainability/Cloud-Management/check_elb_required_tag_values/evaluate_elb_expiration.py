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
""" Module for evaluating ELB expiration """
from common.common_constants import ComplianceConstants
from common.common_constants import ResourceConstants
from common.common_constants import EvaluationMessages
from common.logger_utility import LoggerUtility
from common.i18n import Translation as _
from common.abstract_evaluate import AbstractEvaluator
from common.date_validation_util import DateValidationUtil


class EvaluateELBExpiration(AbstractEvaluator):  # pylint: disable=W0223
    """ Class for evaluating ELB expiration """
    @staticmethod
    def getEvaluationResult(evaluationResult, expirationDateLimit, eventItem, tagKey):
        """ Method for getting evaluation result based on the given parameters """
        response = DateValidationUtil.updateEventActionBasedOnDate(eventItem, expirationDateLimit, tagKey)

        if response == ResourceConstants.RESOURCE_EXPIRATION_DATE_LIMIT_EXCEEDED:
            evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
            LoggerUtility.logInfo(EvaluationMessages.RESOURCE_EXPIRATION_TAG_REPLACED.format(expirationDateLimit))
            evaluationResult.annotation = _(EvaluationMessages.RESOURCE_EXPIRATION_TAG_REPLACED.format(expirationDateLimit))

        elif response == ResourceConstants.RESOURCE_ABOUT_TO_EXPIRE or \
                response == ResourceConstants.RESOURCE_HAS_VALIDITY:
            evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
            LoggerUtility.logInfo(EvaluationMessages.RESOURCE_ABOUT_TO_EXPIRE.format(
                eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME],
                eventItem.resourceId,
                eventItem.configItems[ResourceConstants.RESOURCE_REMAINING_VALIDITY]
            ))
            evaluationResult.annotation = _(EvaluationMessages.RESOURCE_ABOUT_TO_EXPIRE.format(
                eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME], '',
                eventItem.configItems[ResourceConstants.RESOURCE_REMAINING_VALIDITY]
            ))

        elif response == ResourceConstants.RESOURCE_VALIDITY_EXPIRED:
            evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
            LoggerUtility.logInfo(EvaluationMessages.RESOURCE_EXPIRED.format(eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME], eventItem.resourceId))
            evaluationResult.annotation = _(EvaluationMessages.RESOURCE_EXPIRED.format(eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME], ""))

        elif response == ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND:
            evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
            LoggerUtility.logInfo(EvaluationMessages.RESOURCE_REQUIRED_TAG_NOT_FOUND.format(eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME],
                                                                                            eventItem.resourceId))
            evaluationResult.annotation = _(
                EvaluationMessages.RESOURCE_REQUIRED_TAG_NOT_FOUND.format(eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME], ''))

        elif response == ResourceConstants.RESOURCE_EXPIRATION_DATE_INVALID:
            evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
            LoggerUtility.logInfo(EvaluationMessages.RESOURCE_EXPIRATION_DATE_INVALID.format(eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME],
                                                                                             eventItem.resourceId))
            evaluationResult.annotation = _(
                EvaluationMessages.RESOURCE_EXPIRATION_DATE_INVALID.format(eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME], ''))
        else:
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_RESOURCE_COMPLIANCE
            LoggerUtility.logInfo(EvaluationMessages.UNABLE_TO_CHECK_COMPLIANCE.format(eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME]))
            evaluationResult.annotation = _(EvaluationMessages.UNABLE_TO_CHECK_COMPLIANCE.format(eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME]))

        result = {
            'Result': evaluationResult,
            'Violation': response
        }

        return result
