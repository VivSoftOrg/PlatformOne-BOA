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
import pytest
import sys
import boto3
from mock import MagicMock
from moto import mock_iam

sys.path.append('../../')

from common.abstract_evaluate import AbstractEvaluator
from common.framework_objects import EvaluationResult
import detach_iam_policy.detach_iam_policy_action as detachIAM
import common.compliance_object_factory as cof
from common.common_constants import AWSResourceClassConstants, ComplianceConstants, BotoConstants
from common.compliance_object_factory import ComplianceObjectFactory

RESOURCE_ID = ""
RESOURCE_TYPE = "AWS::IAM::User"
CONFIG_ITEMS = {
    "username": "anish.bhagwat",
    "userid": "",
    "managedPolicies": ['test', 'test'],
    "inlinePolicies": ['test1', 'test2']
}

INVOKING_EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\n \"configurationItemDiff\": null,\n \"configurationItem\": {\n \"relatedEvents\": [],\n \"relationships\": [{\n \"resourceId\": \"AGPAI5DSTRYR7HZKTK5NG\",\n \"resourceName\": \"PowerUsers\",\n \"resourceType\": \"AWS::IAM::Group\",\n \"name\": \"Is attached to Group\"\n }],\n \"configuration\": {\n \"path\": \" / \",\n \"userName\": \"test.user\",\n \"userId\": \"AIDAJNL63BJPIG4KUSNEC\",\n \"arn\": \"arn:aws:iam::107339370656:user/test.user\",\n \"createDate\": \"2017 - 07 - 21 T04: 15: 53.000 Z\",\n \"userPolicyList\": [],\n \"groupList\": [\n \"PowerUsers\"\n ],\n \"attachedManagedPolicies\": [{\n \"policyName\": \"AWSLambdaFullAccess\",\n \"policyArn\": \"arn: aws: iam::aws: policy / AWSLambdaFullAccess\"\n }, {\n \"policyName\": \"IAMFullAccess\",\n \"policyArn\": \"arn: aws: iam::aws: policy / IAMFullAccess\"\n }]\n },\n \"supplementaryConfiguration\": {},\n \"tags\": {},\n \"configurationItemVersion\": \"1.2 \",\n \"configurationItemCaptureTime\": \"2017 - 08 - 22 T14: 49: 58.374 Z\",\n \"configurationStateId\": 1503413398374,\n \"awsAccountId\":\n \"107339370656\",\n \"configurationItemStatus\": \"ResourceDiscovered\",\n \"resourceType\": \"AWS::IAM::User\",\n \"resourceId\": \"AIDAJZPKT5SW3N7TY7NZS\",\n \"resourceName\": \"anish.bhagwat\",\n \"ARN\": \"arn: aws: iam::107339370656: user / anish.bhagwat\",\n \"awsRegion\": \"global\",\n \"availabilityZone\": \"Not Applicable\",\n \"configurationStateMd5Hash\": \"c33ccb2c3df66b520401fe5a14344cdc\",\n \"resourceCreationTime\": \"2017 - 07 - 21 T04: 15: 53.000 Z\"\n },\n \"notificationCreationTime\": \"2017 - 09 - 18 T05: 58: 16.355 Z\",\n  \"messageType\": \"ConfigurationItemChangeNotification\",\n \"recordVersion\": 1.2\n }",
    "ruleParameters": "{\"performAction\": \"True\",\"excludeUser\": \"\",\"notifier\": \"sns\"}",
    "resultToken": "",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-cb01p5",
    "configRuleName": "gaurav-test2",
    "configRuleId": "config-rule-cb01p5",
    "accountId": "107339370656"
}
CONTEXT = ""

inlinePolicies = []
managedPolicies = []
responseInlinePolicies = {
    'PolicyNames': [
        'test',
    ]
}
responsePolicies = {
    'AttachedPolicies': [
        {
            'PolicyName': 'stsdsdring',
            'PolicyArn': 'sdsdsd'
        },
    ]
}


class TestDetachIamPolicyAction(object):
    __regions = [ 'us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']

    __mockInstanceResponse = {'ResponseMetadata': { 'HTTPStatusCode': 200, 'RetryAttempts': 0}}
    __mockInstanceResponse_fail = {'ResponseMetadata': { 'HTTPStatusCode': 500, 'RetryAttempts': 0}}

    __eventParam = cof.ComplianceObjectFactory.createEventParamFrom(
            INVOKING_EVENT_JSON,
            CONTEXT
        )
    __detachIam = detachIAM.DetachIamPolicyAction(__eventParam)

    @mock_iam
    def test_action_success(self):
        """ This method is for testing Action class """
        evaluationResult = EvaluationResult()
        iamClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_IAM, region_name=self.__regions[0])
        detachIAM.DetachIamPolicyAction.deleteInlinePolicies = MagicMock(return_value=True)
        detachIAM.DetachIamPolicyAction.detachManagedPolicies = MagicMock(return_value=True)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)

        return_value = self.__detachIam.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_iam
    def test_action_non_compliant(self):
        """ This method is for testing Action class """
        evaluationResult = EvaluationResult()
        iamClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_IAM, region_name=self.__regions[0])
        detachIAM.BotoUtility.getClient = MagicMock(return_value=iamClient)
        # self.deleteInlinePolicies = MagicMock(return_value=self.__mockInstanceResponse_fail)
        # self.detachManagedPolicies = MagicMock(return_value=self.__mockInstanceResponse_fail)
        detachIAM.DetachIamPolicyAction.deleteInlinePolicies = MagicMock(return_value=False)
        detachIAM.DetachIamPolicyAction.detachManagedPolicies = MagicMock(return_value=False)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)

        return_value = self.__detachIam.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
