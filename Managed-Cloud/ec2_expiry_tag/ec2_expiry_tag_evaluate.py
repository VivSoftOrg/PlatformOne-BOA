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
""" This module checks whether EC2 instance has valid expiration tag or not """
from common.common_constants import ComplianceConstants
from common.common_constants import TagsConstants
from common.abstract_evaluate import AbstractEvaluator
from common.framework_objects import EvaluationResult
from common.logger_utility import LoggerUtility
from common.i18n import Translation as _
from common.evaluation_result_factory import EvaluationResultFactory
from ec2_expiry_tag.ec2_expiry_tag_constants import Constants


class Ec2ExpiryTagEvaluate(AbstractEvaluator):
    """ This class is responsible for evaluating resource as either Compliant or Non-compliant """

    def evaluate(self, eventItem):
        errorMessage = ""
        evaluationResult = EvaluationResult()

        if TagsConstants.EC2_INSTANCE_TAGS not in eventItem.configItems:
            eventItem.configItems.update({TagsConstants.EC2_INSTANCE_TAGS: []})
        else:
            if isinstance(eventItem.configItems[TagsConstants.EC2_INSTANCE_TAGS], dict):
                eventItem.configItems[TagsConstants.EC2_INSTANCE_TAGS] = [{'key': tagKey, 'value': eventItem.configItems[TagsConstants.EC2_INSTANCE_TAGS][tagKey]} for tagKey in eventItem.configItems[TagsConstants.EC2_INSTANCE_TAGS]]

        try:
            limit_expiration_date = int(self._AbstractEvaluator__eventParam.configParam[Constants.LIMIT_EXPIRTION_DATE_REFERENCE])
            response = EvaluationResultFactory.getEvaluationResultForExpirationDate(evaluationResult, limit_expiration_date, eventItem)
            evaluationResult = response['Result']

            if evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE:
                self._AbstractEvaluator__recommendationMessage = "It is recommended to update your EC2 instances with a valid ExpirationDate tag to avoid stopping or termination of the instances."

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while evaluating for ec2_expiry_tag rule. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.annotation = _(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE

        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
