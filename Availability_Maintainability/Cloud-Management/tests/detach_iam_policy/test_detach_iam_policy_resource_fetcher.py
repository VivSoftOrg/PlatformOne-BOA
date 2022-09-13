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
from mock import MagicMock
from moto import mock_iam
import datetime
import boto3

sys.path.append('../../')

from common.framework_objects import EvaluationResult

from common.abstract_evaluate import AbstractEvaluator
# from detach_iam_policy.detach_iam_policy_resource_fetcher import DetachIamPolicyResourceFetcher

import detach_iam_policy.detach_iam_policy_resource_fetcher as detachIAM
import common.compliance_object_factory as cof
from common.boto_utility import BotoUtility
from common.compliance_object_factory import ComplianceObjectFactory

RESOURCE_ID = ""
RESOURCE_TYPE = "AWS::IAM::User" 
CONFIG_ITEMS = {"username": "test", "userid": ""}

EVENTJSON = {
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

USERS = {
    "Users": [{
        "UserName": "test.user",
        "UserId": "AIDAJNL63BJPIG4KUSNEC",
        "Path": "/",
        "CreateDate": "2018-08-05",
        "Arn": "arn:aws:iam::107339370656:user/test.user",
    }],
    "ResponseMetadata": {
        "RequestId": "dfb003e1-9de7-11e7-a396-b1a69458d73d",
        "HTTPHeaders": {
            "x-amzn-requestid": "dfb003e1-9de7-11e7-a396-b1a69458d73d",
            "content-type": "text/xml",
            "content-length": "3267",
            "date": "Wed, 20 Sep 2017 09:41:26 GMT",
            "vary": "Accept-Encoding"
        },
        "RetryAttempts": 0,
        "HTTPStatusCode": 200
    },
    "IsTruncated": False
}


class TestDetachIamPolicyResourceFetcher(object):

    @mock_iam
    def test_fetcher_empty_list(self):
        evaluationResult = EvaluationResult()
        eventParam = cof.ComplianceObjectFactory.createEventParamFrom(
            EVENTJSON,
            CONTEXT
        )
        self._AbstractResourceFetcher__eventParam = eventParam

        iamClient = boto3.client('iam')
        detachIAM.BotoUtility.getClient = MagicMock(return_value=iamClient)
        
        usersList = detachIAM.DetachIamPolicyResourceFetcher.resourceFetcher(self)

        assert len(usersList) == 0

    @mock_iam
    def test_fetcher(self):
        evaluationResult = EvaluationResult()
        eventParam = cof.ComplianceObjectFactory.createEventParamFrom(
            EVENTJSON,
            CONTEXT
        )
        self._AbstractResourceFetcher__eventParam = eventParam

        iamClient = boto3.client('iam')
        detachIAM.BotoUtility.getClient = MagicMock(return_value=iamClient)
        iamClient.list_users = MagicMock(return_value=USERS)
        configItems = {}
        configItems.update({'username':"test.user"})
        eventItems = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId="AIDAJNL63BJPIG4KUSNEC", resourceType="AWS::IAM::User", configItems=configItems)
        self._DetachIamPolicyResourceFetcher__parseAndFetchUserDetails = MagicMock(return_value=eventItems)
        usersList = detachIAM.DetachIamPolicyResourceFetcher.resourceFetcher(self)

        assert len(usersList) != 0