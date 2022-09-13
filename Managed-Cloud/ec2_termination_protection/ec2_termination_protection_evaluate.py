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
""" This module will check whether EC2 instance has enabled termination protection or not. """
from common.common_constants import ComplianceConstants, ManagedCloudConstants, TagsConstants, ResourceConstants, BotoConstants
from common.boto_utility import BotoUtility
from common.abstract_evaluate import AbstractEvaluator
from common.framework_objects import EvaluationResult
from common.logger_utility import LoggerUtility


class Ec2TerminationProtectionEvaluate(AbstractEvaluator):
    """ This class will be responsible for evaluating the resources. """
    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        region = eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
        isRequiredTagValuePresent = False
        environmentName = ""
        awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
        ec2Client = BotoUtility.getClient(
            BotoConstants.BOTO_CLIENT_AWS_EC2,
            self._AbstractEvaluator__eventParam.accNo,
            BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
            awsPartitionName,
            region
        )
        environmentValues = self._AbstractEvaluator__eventParam.configParam[ResourceConstants.ENVIRONMENT_VALUES_REFERENCE].split(",")
        if TagsConstants.EC2_INSTANCE_TAGS in eventItem.configItems:
            for tag in eventItem.configItems[TagsConstants.EC2_INSTANCE_TAGS]:
                if tag[TagsConstants.EC2_REQUIRED_TAG_KEY] == ResourceConstants.ENVIRONMENT_TAG_REFERENCE:
                    if tag[TagsConstants.EC2_REQUIRED_TAG_VALUE] in environmentValues:
                        isRequiredTagValuePresent = True
                        environmentName = tag[TagsConstants.EC2_REQUIRED_TAG_VALUE]
                        break
        else:
            eventItem.configItems.update({TagsConstants.EC2_INSTANCE_TAGS: []})

        if isRequiredTagValuePresent is True:
            terminationProtectionResponse = ec2Client.describe_instance_attribute(
                Attribute=ResourceConstants.DISABLE_API_TERMINATION_KEYWORD,
                InstanceId=eventItem.resourceId
            )[ResourceConstants.DISABLE_API_TERMINATION][TagsConstants.TAG_VALUE_REFERENCE]
            if terminationProtectionResponse is False:
                LoggerUtility.logInfo("{} instances has not enabled termination protection.".format(environmentName))
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "{} instances has not enabled termination protection.".format(environmentName)
            else:
                LoggerUtility.logInfo("{} instances has enabled termination protection.".format(environmentName))
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = "{} instances has enabled termination protection.".format(environmentName)
        else:
            LoggerUtility.logInfo("Resource {} is not applicable.".format(eventItem.resourceId))
            evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
            evaluationResult.annotation = "Resource is not applicable."
        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        return evaluationResult
