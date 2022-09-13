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
sys.path.append('../../')

from enforce_allow_deny_groups_to_iam_users.enforce_allow_deny_groups_to_iam_users_resource_fetcher import *
from tests.enforce_allow_deny_groups_to_iam_users.test_enforce_allow_deny_groups_to_iam_users_placebo_initializer import *
import common.compliance_object_factory as complianceobjectfactory
import unittest


EVENT_JSON = {
  "configRuleId": "config-rule-1v52mx",
  "version": "1.0",
  "configRuleName": "enforce_allow_deny_groups_to_iam_users",
  "configRuleArn": "arn:aws:config:us-east-1:693265998683:config-rule/config-rule-1v52mx",
  "invokingEvent": "{\n  \"configurationItemDiff\": null,\n   \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
  "resultToken": "",
  "ruleParameters": "{\"performAction\": \"True\", \"allowGroup\": \"AllowGroupName\", \"denyGroup\": \"DenyGroupName\", \"actionName\": \"EnforceAllowAndDenyGroupsAction\", \"evaluateName\": \"EnforceAllowAndDenyGroupsEvaluate\",   \"resourceFetcherName\" : \"EnforceAllowAndDenyGroupsResourceFetcher\",  \"moduleName\": \"enforce_allow_deny_groups_to_iam_users\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\"}",
  "eventLeftScope": "False",
  "executionRoleArn": "arn:aws:iam::693265998683:role/awsconfig-role",
  "accountId": "693265998683"
}

CONTEXT = ""


class TestEnforceAllowAndDenyGroupsFetcher(unittest.TestCase):
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __enforceGroups = EnforceAllowAndDenyGroupsResourceFetcher(__eventParam)

    def testIamUsersResourceFetcher(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getResourceFetcherMock('fetch_users')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__enforceGroups.resourceFetcher()
        assert bool(return_value) == False

    def testIamUsersResourceFetcherNoData(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getResourceFetcherMock('fetch_users_blank_response')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__enforceGroups.resourceFetcher()
        assert bool(return_value) == False
