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
""" This module will check whether the instance is compliant or noncompliant,
 on the basis of an instance is attached  to a predefined security group or not """
from common.abstract_evaluate import AbstractEvaluator
from common.common_utility import MappingsEncoder
from common.common_constants import ComplianceConstants, ManagedCloudConstants
from common.i18n import Translation as _
from common.framework_objects import EvaluationResult
from common.logger_utility import LoggerUtility
from attach_security_group_to_all_instances.attach_security_group_to_all_instances_constants import Constants


class AttachSecurityGroupToInstancesEvaluate(AbstractEvaluator):
    """ This class will check for whether the instance is compliant or not and return evaluation result """

    def evaluate(self, eventItem):
        errorMessage = ""
        try:
            evaluationResult = EvaluationResult()

            mappings = MappingsEncoder.getMappings(self._AbstractEvaluator__eventParam.configParam[Constants.INPUT_MAPPINGS])
            mustHaveSecurityGroups = mappings[eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]][eventItem.configItems[Constants.VPC_ID]]
            mustHaveSecurityGroups = list(set(mustHaveSecurityGroups))
            currentSecurityGroups = [securityGroup[Constants.GROUP_ID] for securityGroup in eventItem.configItems[Constants.SECURITY_GROUPS]]

            for securityGroup in mustHaveSecurityGroups:
                if securityGroup not in currentSecurityGroups:
                    groupsToAttach = list(set(mustHaveSecurityGroups) - set(currentSecurityGroups))
                    groupsNotFound = list(set(groupsToAttach) - set(eventItem.configItems[Constants.ALL_SECURITY_GROUPS]))
                    groupsToAttach = list(set(groupsToAttach) - set(groupsNotFound))
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    if groupsToAttach:
                        eventItem.configItems.update({Constants.ATTACH_GROUPS: ', '.join(group for group in groupsToAttach)})
                    if groupsNotFound:
                        eventItem.configItems.update({Constants.GROUPS_NOT_FOUND: ', '.join(group for group in groupsNotFound)})
                    evaluationResult.annotation = _("The instance does not have all the defined security groups attached to it.")
                    self._AbstractEvaluator__recommendationMessage = "Please ensure all your instances are attached to predefined compliance security groups."
                    self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                    return evaluationResult

            evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
            evaluationResult.annotation = _("The instance have all the defined security groups attached to it.")

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type doesn't possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while evaluating for attaching secuity group to all instances. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)

        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
