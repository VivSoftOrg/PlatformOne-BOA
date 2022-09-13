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
"""This module will Evaluate the Rule and mark resource as compliant or non_Compliant based on behaviour."""
from datetime import datetime, timezone
from dateutil import parser
from botocore.exceptions import ClientError
from common.abstract_evaluate import AbstractEvaluator
from common.common_constants import ComplianceConstants
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.framework_objects import EvaluationResult
from delete_old_ami.delete_old_ami_constants import AMIConstants


class DeleteOldAMIEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate AMI on the base of age. """
    def __getAMIAge(self, amiCreationDate):
        """Method returns AMI volume Age"""
        try:
            today = datetime.now(timezone.utc)
            return (today - amiCreationDate).days
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            return False
        except Exception as e:
            LoggerUtility.logError("Error occured while getting AMI age. {}".format(e))
            return False

    def evaluate(self, eventItem):
        errorMessage = ""
        evaluationResult = EvaluationResult()
        try:
            amiAge = self.__getAMIAge(parser.parse(eventItem.configItems[AMIConstants.AMI_CREATION_DATE]))
            amiValidity = int(self._AbstractEvaluator__eventParam.configParam['amiValidForDays'])

            if amiAge <= amiValidity:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("AMI is not older than {} days.".format(amiValidity))
                LoggerUtility.logInfo(_("AMI  : {} is not older than {} days in region: {}.".format(eventItem.resourceId, amiValidity, eventItem.configItems[AMIConstants.AWS_REGION])))
            else:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("AMI is older than {} days.".format(amiValidity))
                LoggerUtility.logInfo(_("AMI  : {} is older than {} days in region: {}.".format(eventItem.resourceId, amiValidity, eventItem.configItems[AMIConstants.AWS_REGION])))
                self._AbstractEvaluator__recommendationMessage = "Review the AMI list and delete the unwanted AMIs. And also add doNotDelete tags to AMIs to prevent them from getting notified/deleted."

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type doesn't possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while performing evaluating for delete_old_ami rule. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)

        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
