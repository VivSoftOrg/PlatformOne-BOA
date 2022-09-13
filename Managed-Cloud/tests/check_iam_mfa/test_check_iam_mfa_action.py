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
import sys
from datetime import datetime

import boto3
import pytest
from mock import MagicMock
from tests.check_iam_mfa.test_check_iam_mfa_placebo_initializer import *

import check_iam_mfa.check_iam_mfa_action as mfa
import common.compliance_object_factory as cof
from check_iam_mfa.check_iam_mfa_action import *
from common.abstract_action import *
from common.compliance_object_factory import ComplianceObjectFactory
from moto import mock_iam

sys.path.append('../../')


RESOURCE_ID = ""
RESOURCE_TYPE = "AWS::IAM::User"
CONFIG_ITEMS = [
    {"username": "test", "userid": "", "CreateDate": datetime(2018, 5, 25), "DeactivationDate": "2018-05-10"},
    {"username": "test", "userid": "", "CreateDate": datetime(2018, 5, 25), "DeactivationDate": None},
    {"username": "test", "userid": "", "CreateDate":  datetime.now().date(), "DeactivationDate": None},
    {"username": "test", "userid": "", "CreateDate": datetime.now().date(), "DeactivationDate": datetime.now().isoformat()},
    {"username": "test", "userid": "", "DeactivationDate": None}
]

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


class TestCheckIamMfaAction(object):

    __eventParam = cof.ComplianceObjectFactory.createEventParamFrom(
        INVOKING_EVENT_JSON,
        CONTEXT
    )

    __checkIamMfaAction = CheckIamMfaAction(__eventParam)

    _AbstractAction__eventParam = __eventParam

    def test_perform_action(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__checkIamMfaAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def test_perform_action_existing_user(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[1])
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__checkIamMfaAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def test_perform_action_new_user(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[2])
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__checkIamMfaAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def test_perform_action_existing_non_compliant_user(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[3])
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__checkIamMfaAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def test_perform_action_failure(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__checkIamMfaAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def test_perform_action_method_exception(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[4])
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__checkIamMfaAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    def test_perform_action_exception(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__checkIamMfaAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
