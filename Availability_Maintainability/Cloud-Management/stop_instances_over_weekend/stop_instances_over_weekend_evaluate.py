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
import datetime
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_evaluate import AbstractEvaluator
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.common_utility import CommonUtility
from common.common_constants import BotoConstants, AWSResourceClassConstants, TagsConstants, ResourceConstants, ComplianceConstants, ManagedCloudConstants


class StopInstancesOverWeekendEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """
    __applicableResources = [AWSResourceClassConstants.EC2_INSTANCE]

    def __getInstancesInAutoScalingGroup(self, asgClient):
        """Method returns instance in auto scalling group"""
        asgInstanceList = []
        asgInstancesDetails = CommonUtility.changeDictionaryKeysToLowerCase(asgClient.describe_auto_scaling_instances())
        for instance in asgInstancesDetails[BotoConstants.BOTO_CLIENT_AWS_ASC_INSTANCE]:
            asgInstanceList.append(instance[BotoConstants.BOTO_CLIENT_AWS_EC2_INSTANCE_ID])
        return asgInstanceList

    def __getAutoScalingGroupName(self, asgClient, InstanceId):
        """Method returns Autoscalling Group name"""
        asgInstancesDetails = asgClient.describe_auto_scaling_instances()
        for instance in asgInstancesDetails[BotoConstants.BOTO_CLIENT_AWS_ASC_INSTANCE]:
            if instance[BotoConstants.BOTO_CLIENT_AWS_EC2_INSTANCE_ID] == InstanceId:
                asgGroupName = instance[ResourceConstants.AUTO_SCALING_GROUPS]

        return asgGroupName

    def __isDayOfWeekend(self):
        " This method will check whether the current date is Saturday or Sunday as per both IST and EST, if yes it will return True. "
        istDay = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).isoweekday()
        estDay = (datetime.datetime.utcnow() + datetime.timedelta(hours=-4)).isoweekday()
        if istDay is ResourceConstants.SIXTH_DAY_OF_WEEK or istDay is ResourceConstants.SEVENTH_DAY_OF_WEEK:
            if estDay is ResourceConstants.SIXTH_DAY_OF_WEEK or estDay is ResourceConstants.SEVENTH_DAY_OF_WEEK:
                return True
        return False

    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        try:
            tagValues = {}
            DAY_OF_WEEKEND = self.__isDayOfWeekend()

            if DAY_OF_WEEKEND:
                awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
                asgClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_ASC,
                    self._AbstractEvaluator__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
                )
                if eventItem.resourceType not in self.__applicableResources:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                    evaluationResult.annotation = _("The rule doesn't apply to resources of type {type} .").format(
                        type=eventItem.resourceType
                    )
                    self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                    return evaluationResult

                for tag in eventItem.configItems[TagsConstants.EC2_INSTANCE_TAGS]:
                    tagValues.update({tag[TagsConstants.EC2_REQUIRED_TAG_KEY]: tag[TagsConstants.EC2_REQUIRED_TAG_VALUE]})

                if TagsConstants.EC2_NOSHUTDOWN_TAG_REFERENCE in tagValues:
                    LoggerUtility.logInfo("Resource has '%s' tag" % (TagsConstants.EC2_NOSHUTDOWN_TAG_REFERENCE))

                    if tagValues[TagsConstants.EC2_NOSHUTDOWN_TAG_REFERENCE] == TagsConstants.EC2_REQUIRED_TAG_VALUE_YES:

                        LoggerUtility.logInfo("The value of NoShutdown tag attribute is valid")
                        evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                        evaluationResult.annotation = _("Resource has valid %s tag" % (TagsConstants.EC2_NOSHUTDOWN_TAG_REFERENCE))
                    else:
                        LoggerUtility.logInfo("The value of NoShutdown tag attribute is not valid")
                        evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                        evaluationResult.annotation = _("Resource does not have valid %s tag" % (TagsConstants.EC2_NOSHUTDOWN_TAG_REFERENCE))
                        recommendationMessage = "Please add NoShutdown tag if you dont want to stop your Instance."
                        self._AbstractEvaluator__recommendationMessage = _(recommendationMessage)
                else:
                    instancesInASG = self.__getInstancesInAutoScalingGroup(asgClient)

                    if eventItem.resourceId in instancesInASG:
                        AsgName = self.__getAutoScalingGroupName(asgClient, eventItem.resourceId)
                        LoggerUtility.logInfo("Instance is in AutoScaling Group." + format(AsgName))
                        evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                        evaluationResult.annotation = _("The instance is in AutoScaling Group '{}'.\n".format(AsgName))
                        instancesInASG = asgClient.update_auto_scaling_group(AutoScalingGroupName=AsgName, MinSize=0, DesiredCapacity=0)
                    else:
                        LoggerUtility.logInfo("Resource does not have %s tag" % (TagsConstants.EC2_NOSHUTDOWN_TAG_REFERENCE))
                        evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                        evaluationResult.annotation = _("Resource does not have valid %s tag" % (TagsConstants.EC2_NOSHUTDOWN_TAG_REFERENCE))
                        recommendationMessage = "Please add  Correct NoShutdown tag if you dont want to stop your Instance."
                        self._AbstractEvaluator__recommendationMessage = _(recommendationMessage)
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

            else:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                LoggerUtility.logInfo("The rule doesn't apply on weekdays.")
                evaluationResult.annotation = _("This Rule is periodic and runs on Saturday.")
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        except ValueError as e:
            LoggerUtility.logError("The content of the object you tried to assign the value is Invalid. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("The content of the object you tried to assign the value is Invalid. {}".format(e))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except AttributeError as e:
            LoggerUtility.logError("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except TypeError as e:
            LoggerUtility.logError("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except NameError as e:
            LoggerUtility.logError("Trying to access a variable that you have not defined properly. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Trying to access a variable that you have not defined properly. {}".format(e))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Boto client error occured. {}".format(e))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except Exception as e:
            LoggerUtility.logError("Error occured while Evaluating Instances. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Error occured while Evaluating Instances. {}".format(e))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        return evaluationResult
