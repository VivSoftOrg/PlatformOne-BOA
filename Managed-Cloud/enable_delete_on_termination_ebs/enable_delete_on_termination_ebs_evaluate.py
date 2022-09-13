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
""" This module will check if delete on termination is enabled or not on EBS Volumes. """
from common.abstract_evaluate import AbstractEvaluator
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.common_constants import EC2Constants, ComplianceConstants, AWSResourceClassConstants
from common.framework_objects import EvaluationResult
from enable_delete_on_termination_ebs.enable_delete_on_termination_ebs_constants import Constants


class EnableDeleteOnTerminationEBSEvaluate(AbstractEvaluator):
    """ This module will check if delete on termination is enabled or not on EBS Volumes. """
    __applicableResources = [AWSResourceClassConstants.EC2_INSTANCE]

    def evaluate(self, eventItem):

        evaluationResult = EvaluationResult()
        hasViolation = False
        errorMessage = ""
        try:
            if eventItem.resourceType not in self.__applicableResources:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The rule doesn't apply to resources of type {type} .").format(
                    type=eventItem.resourceType
                )

            elif eventItem.configItems[EC2Constants.EC2_INSTANCE_STATE_REFERENCE][EC2Constants.EC2_INSTANCE_STATE_NAME_REFERENCE] \
                    == EC2Constants.EC2_TERMINATED_STATE_REFERENCE:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The configurationItem was deleted and therefore cannot be validated")

            elif eventItem.configItems[EC2Constants.EC2_INSTANCE_STATE_REFERENCE][EC2Constants.EC2_INSTANCE_STATE_NAME_REFERENCE] \
                == EC2Constants.EC2_RUNNING_STATE_REFERENCE \
                or eventItem.configItems[EC2Constants.EC2_INSTANCE_STATE_REFERENCE][EC2Constants.EC2_INSTANCE_STATE_NAME_REFERENCE] \
                == EC2Constants.EC2_PENDING_STATE_REFERENCE or \
                eventItem.configItems[EC2Constants.EC2_INSTANCE_STATE_REFERENCE][EC2Constants.EC2_INSTANCE_STATE_NAME_REFERENCE] \
                    == EC2Constants.EC2_STOPPED_STATE_REFERENCE:

                for mappings in eventItem.configItems[Constants.EC2_BLOCK_DEVICE_MAPPINGS]:
                    if not mappings[Constants.EBS_VOLUME][Constants.EBS_DELETE_ON_TERMINATION]:
                        LoggerUtility.logInfo("Delete on termination is not enabled for volume - {} attached to instance - {}"
                                              .format(mappings[Constants.EBS_VOLUME][EC2Constants.EBS_VOLUME_ID], eventItem.resourceId))
                        hasViolation = True

                if hasViolation:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Delete on termination is not enabled.")
                else:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Delete on termination is enabled on all volumes for instance - {}".format(eventItem.resourceId))

            else:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("This resource is compliant with the rule.")

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type which it doesn't possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except Exception as e:
            errorMessage = "Error occurred while evaluating for enabling delete on termination of EBS. {}".format(e)

        if errorMessage != "":
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)
            LoggerUtility.logError(errorMessage)
        else:
            LoggerUtility.logInfo(evaluationResult.annotation)

        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
