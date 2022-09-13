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
""" This module will evaluate the elastic IP addresses as either Complaint or Non-compliant """
from botocore.exceptions import ClientError
from common.abstract_evaluate import AbstractEvaluator
from common.framework_objects import EvaluationResult
from common.logger_utility import LoggerUtility
from common.common_constants import ComplianceConstants
from check_ec2_unused_eip_values.check_ec2_unused_eip_values_constants import Constants


class CheckEc2UnusedEIPValuesEvaluate(AbstractEvaluator):
    """ This class will be responsible for evaluating the resources. """
    def evaluate(self, eventItem):
        errorMessage = ""
        evaluationResult = EvaluationResult()
        try:
            if Constants.ASSOCIATION_ID_REFERENCE in eventItem.configItems:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = "Elastic IP is associated to an instance."
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                LoggerUtility.logInfo("Elastic IP is associated to an instance.")
            else:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "The Elastic IP address is not attached to any EC2 instance."
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                LoggerUtility.logInfo("Elastic IP is not associated to an instance.")

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while evaluating user account. {}".format(e)
        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = errorMessage
        return evaluationResult
