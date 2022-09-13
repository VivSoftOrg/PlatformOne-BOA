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
from datetime import timedelta, datetime, timezone
from botocore.exceptions import ClientError
from common.abstract_evaluate import AbstractEvaluator
from common.common_constants import ComplianceConstants, AWSResourceClassConstants
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.framework_objects import EvaluationResult
from delete_unused_ebs.delete_unused_ebs_constants import EBSVolumeConstants


class DeleteUnusedEBSEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """

    def __getEBSVolumeAge(self, ebsCreationDate):
        """Method returns EBS volume Age"""
        try:
            today = datetime.now(timezone.utc)
            return (today - ebsCreationDate).days
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            return False
        except Exception as e:
            LoggerUtility.logError("Error occured while getting volume age. {}".format(e))
            return False

    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        try:
            if eventItem.resourceType not in AWSResourceClassConstants.EBS_VOLUME:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("This rule doesn't apply to the resources of type {type} .").format(
                    type=eventItem.resourceType
                )
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

            else:
                ebsAge = eventItem.configItems[EBSVolumeConstants.EBS_CREATION_DATE] + timedelta(
                    days=int(self._AbstractEvaluator__eventParam.configParam[EBSVolumeConstants.EBS_AGE]))
                today = datetime.now(timezone.utc)

                if ebsAge <= today:
                    LoggerUtility.logInfo('Found unused EBS volume: {} in region: {}'.format(eventItem.resourceId, eventItem.configItems[EBSVolumeConstants.AWS_REGION]))  # noqa
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    recommendationMessage = "Review the use of the unattached EBS volume. Unattached EBS volume are chargeable."
                    self._AbstractEvaluator__recommendationMessage = _(recommendationMessage)
                    evaluationResult.annotation = ('EBS volume is not attached to any stopped or running EC2 instance.')
                    self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                    eventItem.configItems.update(
                        {
                            EBSVolumeConstants.EBS_Volume_AGE: '{}'.format(self.__getEBSVolumeAge(eventItem.configItems[EBSVolumeConstants.EBS_CREATION_DATE]))
                        }
                    )

                else:
                    LoggerUtility.logInfo("Found Unused EBS Volume: {} in region: {} but is not older than {}".format(eventItem.resourceId, eventItem.configItems[EBSVolumeConstants.AWS_REGION], self._AbstractEvaluator__eventParam.configParam[EBSVolumeConstants.EBS_AGE]))
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = ('EBS volume is not attached to any instance and it is not older than {} days'.format(self._AbstractEvaluator__eventParam.configParam[EBSVolumeConstants.EBS_AGE]))
                    self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        except ValueError as e:
            LoggerUtility.logError("The content of the object you tried to assign the value is invalid. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("The content of the object you tried to assign the value is invalid. {}".format(e))
        except AttributeError as e:
            LoggerUtility.logError("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
        except TypeError as e:
            LoggerUtility.logError("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
        except NameError as e:
            LoggerUtility.logError("Trying to access a variable that you have not defined properly. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Trying to access a variable that you have not defined properly. {}".format(e))
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Boto client error occured. {}".format(e))
        except Exception as e:
            LoggerUtility.logError("Error occured while evaluating EBS volumes. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Error occured while evaluating EBS volumes. {}".format(e))

        return evaluationResult
