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

from active_iam_users.active_iam_users_resource_fetcher import *
from tests.active_iam_users.test_active_iam_users_placebo_initializer import *
import common.compliance_object_factory as complianceobjectfactory
import unittest


EVENT_JSON = {
  "configRuleId": "config-rule-1v52mx",
  "version": "1.0",
  "configRuleName": "active_iam_users",
  "configRuleArn": "arn:aws:config:us-east-1:693265998683:config-rule/config-rule-1v52mx",
  "invokingEvent": "{\n  \"configurationItemDiff\": null,\n   \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
  "resultToken": "",
  "ruleParameters": "{\"performAction\": \"True\", \"lastActivityValidity\": \"10\", \"deleteWarnings\": \"10\", \"disableWarnings\": \"10\", \"actionName\": \"ActiveIamUsersAction\", \"evaluateName\": \"ActiveIamUsersEvaluate\",   \"resourceFetcherName\" : \"ActiveIamUsersResourceFetcher\",  \"moduleName\": \"atice_iam_users\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\"}",
  "eventLeftScope": "False",
  "executionRoleArn": "arn:aws:iam::693265998683:role/awsconfig-role",
  "accountId": "693265998683"
}

CONTEXT = ""


class TestActiveIamUsersFetcher(unittest.TestCase):
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __activeIamUsers = ActiveIamUsersResourceFetcher(__eventParam)

    def testIamUsersResourceFetcher(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getResourceFetcherMock('fetch_users')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__activeIamUsers.resourceFetcher()
        assert bool(return_value) == True

    def testIamUsersResourceFetcherNoData(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getResourceFetcherMock('fetch_users_blank_response')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__activeIamUsers.resourceFetcher()
        assert bool(return_value) == False

    def testIamUsersResourceFetcherException(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getResourceFetcherMock('fetch_users_exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__activeIamUsers.resourceFetcher()
        assert bool(return_value) == False
