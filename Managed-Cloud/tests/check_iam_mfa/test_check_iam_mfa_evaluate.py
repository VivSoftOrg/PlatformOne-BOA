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

from common.abstract_evaluate import *
from check_iam_mfa.check_iam_mfa_evaluate import *
from common.compliance_object_factory import ComplianceObjectFactory

import check_iam_mfa.check_iam_mfa_evaluate as mfa
import common.compliance_object_factory as cof

RESOURCE_ID = ""
RESOURCE_TYPE = "AWS::IAM::User"
CONFIG_ITEMS = {"username": "test", "userid": "testId"}

INVOKING_EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\n \"configurationItemDiff\": null,\n \"configurationItem\": {\n \"relatedEvents\": [],\n \"relationships\": [{\n \"resourceId\": \"AGPAI5DSTRYR7HZKTK5NG\",\n \"resourceName\": \"PowerUsers\",\n \"resourceType\": \"AWS::IAM::Group\",\n \"name\": \"Is attached to Group\"\n }],\n \"configuration\": {\n \"path\": \" / \",\n \"userName\": \"test.user\",\n \"userId\": \"AIDAJNL63BJPIG4KUSNEC\",\n \"arn\": \"arn:aws:iam::107339370656:user/test.user\",\n \"createDate\": \"2017 - 07 - 21 T04: 15: 53.000 Z\",\n \"userPolicyList\": [],\n \"groupList\": [\n \"PowerUsers\"\n ],\n \"attachedManagedPolicies\": [{\n \"policyName\": \"AWSLambdaFullAccess\",\n \"policyArn\": \"arn: aws: iam::aws: policy / AWSLambdaFullAccess\"\n }, {\n \"policyName\": \"IAMFullAccess\",\n \"policyArn\": \"arn: aws: iam::aws: policy / IAMFullAccess\"\n }]\n },\n \"supplementaryConfiguration\": {},\n \"tags\": {},\n \"configurationItemVersion\": \"1.2 \",\n \"configurationItemCaptureTime\": \"2017 - 08 - 22 T14: 49: 58.374 Z\",\n \"configurationStateId\": 1503413398374,\n \"awsAccountId\":\n \"107339370656\",\n \"configurationItemStatus\": \"ResourceDiscovered\",\n \"resourceType\": \"AWS::IAM::User\",\n \"resourceId\": \"AIDAJZPKT5SW3N7TY7NZS\",\n \"resourceName\": \"anish.bhagwat\",\n \"ARN\": \"arn: aws: iam::107339370656: user / anish.bhagwat\",\n \"awsRegion\": \"global\",\n \"availabilityZone\": \"Not Applicable\",\n \"configurationStateMd5Hash\": \"c33ccb2c3df66b520401fe5a14344cdc\",\n \"resourceCreationTime\": \"2017 - 07 - 21 T04: 15: 53.000 Z\"\n },\n \"notificationCreationTime\": \"2017 - 09 - 18 T05: 58: 16.355 Z\",\n  \"messageType\": \"ConfigurationItemChangeNotification\",\n \"recordVersion\": 1.2\n }",
    "ruleParameters": "{\"performAction\": \"True\",\"notifier\": \"sns\"}",
    "resultToken": "",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-cb01p5",
    "configRuleName": "gaurav-test2",
    "configRuleId": "config-rule-cb01p5",
    "accountId": "107339370656"
}
CONTEXT = ""

MFA_DEVICES = {"MFADevices": [{"UserName": "test", "SerialNumber": "arn:aws:iam::107339370656:mfa/test"}], "IsTruncated": False, "ResponseMetadata": {"RequestId": "a9bb734d-9c6a-11e7-8f4a-ff1ebfbbd0e7", "RetryAttempts": 0, "HTTPStatusCode": 200, "HTTPHeaders": {"content-length": "548", "x-amzn-requestid": "a9bb734d-9c6a-11e7-8f4a-ff1ebfbbd0e7", "content-type": "text/xml", "date": "Mon, 18 Sep 2017 12:12:38 GMT"}}}
LOGIN_PROFILE = {"ResponseMetadata": {"RetryAttempts": 0, "HTTPStatusCode": 200, "RequestId": "fb38e949-a99d-11e7-8f01-0f146b5ace8a", "HTTPHeaders": {"x-amzn-requestid": "fb38e949-a99d-11e7-8f01-0f146b5ace8a", "date": "Thu, 05 Oct 2017 07:22:43 GMT", "content-length": "458", "content-type": "text/xml"}}, "LoginProfile": {"UserName": "priyanka.khairnar", "PasswordResetRequired": False}}


class TestCheckIamMfaEvaluate(object):

    __eventParam = cof.ComplianceObjectFactory.createEventParamFrom(
        INVOKING_EVENT_JSON,
        CONTEXT
    )

    __eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=CONFIG_ITEMS['userid'], resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)

    # __iamClient = TestMockIamClient.mock()

    __CheckIamMfaEvaluate = CheckIamMfaEvaluate(__eventParam)

    _AbstractEvaluator__eventParam = __eventParam

    @mock_iam
    def test_evaluate_without_password(self):
        evaluationResult = EvaluationResult()
        iamClient = boto3.client('iam', 'us-east-1')
        cloudTrailClient = boto3.client('cloudtrail', 'us-east-1')
        mfa.BotoUtility.getClient = MagicMock(side_effect=[iamClient, cloudTrailClient])
        evaluationResult = self.__CheckIamMfaEvaluate.evaluate(self.__eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

    @mock_iam
    def test_evaluate_without_mfa_exception(self):
        evaluationResult = EvaluationResult()
        iamClient = boto3.client('iam', 'us-east-1')
        cloudTrailClient = boto3.client('cloudtrail', 'us-east-1')
        mfa.BotoUtility.getClient = MagicMock(side_effect=[iamClient, cloudTrailClient])
        iamClient.get_login_profile = MagicMock(return_value=LOGIN_PROFILE)
        evaluationResult = self.__CheckIamMfaEvaluate.evaluate(self.__eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE

    @mock_iam
    def test_evaluate_with_mfa(self):
        iamClient = boto3.client('iam', 'us-east-1')
        cloudTrailClient = boto3.client('cloudtrail', 'us-east-1')
        mfa.BotoUtility.getClient = MagicMock(side_effect=[iamClient, cloudTrailClient])
        iamClient.get_login_profile = MagicMock(return_value=LOGIN_PROFILE)
        iamClient.list_mfa_devices = MagicMock(return_value=MFA_DEVICES)
        evaluationResult = self.__CheckIamMfaEvaluate.evaluate(self.__eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE
