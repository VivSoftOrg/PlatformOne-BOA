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
from botocore.exceptions import ClientError

from common.abstract_evaluate import AbstractEvaluator
from common.boto_utility import BotoUtility
from common.common_constants import (AWSResourceClassConstants, BotoConstants,
                                     ComplianceConstants,
                                     ManagedCloudConstants, ResourceConstants)
from common.common_utility import CommonUtility
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from delete_unused_elb.delete_unused_elb_constants import Constants
from common_constants.exception_constants import ExceptionMessages


class ELBUnusedLoadBalancersEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """
    __applicableResources = [AWSResourceClassConstants.ELB_RESOURCE, AWSResourceClassConstants.ELB_V2_RESOURCE]

    def __evaluateClassicELB(self, eventItem, evaluationResult):
        """  This method evaluates Classic Load Balancers """
        validInstanceCount = 0
        for instance in eventItem.configItems["instances"]:
            try:
                if instance['instanceid']:
                    validInstanceCount = validInstanceCount + 1
            except Exception as e:
                LoggerUtility.logError("Instance Id not found.")
                LoggerUtility.logError("Error occured while {}".format(e))
        spareTimeInHours = int(self._AbstractEvaluator__eventParam.configParam[Constants.NEW_ELB_SPARE_TIME])
        newELBSkipInterval = spareTimeInHours * 60 * 60
        # Amazon returns createdtime datetime object in utc format.
        createDate = eventItem.configItems['createdtime']
        if validInstanceCount == 0 and CommonUtility.checkResourceOlderBySeconds(createDate, newELBSkipInterval):
            evaluationResult.annotation = _("The {} does not have any instances associated and was created more than {} hours ago.".format(ResourceConstants.ELB_KEYWORD, spareTimeInHours))
            evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
            LoggerUtility.logInfo("The {} {} does not have any instance associated and was created more than {} hours ago.".format(ResourceConstants.ELB_KEYWORD, eventItem.configItems['loadbalancername'], spareTimeInHours))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        else:
            evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
            evaluationResult.annotation = _("The {} is compliant with the rule.".format(ResourceConstants.ELB_KEYWORD))
            LoggerUtility.logInfo("The {} {} is compliant with the rule.".format(ResourceConstants.ELB_KEYWORD, eventItem.configItems['loadbalancername']))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        return evaluationResult

    def __getElbV2Client(self, eventItem):
        """ This method will be used to get the application or network type elb client """
        awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
        elbClient = BotoUtility.getClient(
            BotoConstants.BOTO_CLIENT_AWS_ELB_V2,
            self._AbstractEvaluator__eventParam.accNo,
            BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
            awsPartitionName,
            eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE])
        return elbClient

    def __evaluateApplicationAndNetworkELB(self, eventItem, evaluationResult):
        """ This method evaluates Application Load Balancers """
        elbClient = self.__getElbV2Client(eventItem)
        spareTimeInHours = int(self._AbstractEvaluator__eventParam.configParam[Constants.NEW_ELB_SPARE_TIME])
        newELBSkipInterval = spareTimeInHours * 60 * 60
        createDate = eventItem.configItems['createdtime']
        hasTarget = False
        try:
            targetGroups = elbClient.describe_target_groups(LoadBalancerArn=eventItem.configItems['loadbalancerarn'])['TargetGroups']
            for target in targetGroups:
                if elbClient.describe_target_health(TargetGroupArn=target['TargetGroupArn'])['TargetHealthDescriptions']:
                    hasTarget = True
                    break
        except Exception as error:
            hasTarget = False
            LoggerUtility.logError(error)

        if not hasTarget and CommonUtility.checkResourceOlderBySeconds(createDate, newELBSkipInterval):
            evaluationResult.annotation = _("The {} does not have any target groups associated and was created more than {} hours ago.".format(ResourceConstants.ELB_KEYWORD, spareTimeInHours))
            evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
            LoggerUtility.logInfo("The {} {} does not have any target groups associated and was created more than {} hours ago.".format(ResourceConstants.ELB_KEYWORD, eventItem.configItems['loadbalancername'], spareTimeInHours))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        else:
            evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
            evaluationResult.annotation = _("The {} is compliant with the rule.".format(ResourceConstants.ELB_KEYWORD))
            LoggerUtility.logInfo("The {} {} is compliant with the rule.".format(ResourceConstants.ELB_KEYWORD, eventItem.configItems['loadbalancername']))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        return evaluationResult

    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        errorMessage = ""
        try:
            if eventItem.resourceType not in self.__applicableResources:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The rule doesn't apply to resources of type {type} .".format(type=eventItem.resourceType))
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            if eventItem.resourceType == AWSResourceClassConstants.ELB_RESOURCE:
                # Evaluate Classic ELB
                self.__evaluateClassicELB(eventItem, evaluationResult)
            else:
                # Evaluate Application and Network ELB
                self.__evaluateApplicationAndNetworkELB(eventItem, evaluationResult)

        except ValueError as e:
            errorMessage = ExceptionMessages.VALUE_ERROR.format(e)
        except AttributeError as e:
            errorMessage = ExceptionMessages.ATTRIBUTE_ERROR.format(e)
        except TypeError as e:
            errorMessage = ExceptionMessages.TYPE_ERROR.format(e)
        except NameError as e:
            errorMessage = ExceptionMessages.NAME_ERROR.format(e)
        except ClientError as e:
            errorMessage = ExceptionMessages.CLIENT_ERROR.format(e)
        except Exception as e:
            errorMessage = "Error occured while Evaluating Unused {}. {}".format(ResourceConstants.ELB_KEYWORD, e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)

        return evaluationResult
