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

from iam_roles_excess_permissions.iam_roles_excess_permissions_resource_fetcher import *
from tests.iam_roles_excess_permissions.iam_roles_excess_permissions_placebo_initializer import *
import common.compliance_object_factory as complianceobjectfactory
import unittest


EVENT_JSON = {
  "configRuleId": "config-rule-1v52mx",
  "version": "1.0",
  "configRuleName": "iam_roles_excess_permissions",
  "configRuleArn": "arn:aws:config:us-east-1:693265998683:config-rule/config-rule-1v52mx",
  "invokingEvent": "{\n \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
  "resultToken": "",
  "ruleParameters": "{\"performAction\": \"True\", \n  \"excludeRoles\": \"REANMSAdmin, svc-iam-permissions-monitor\", \n   \"policynames\": \"AdministratorAccess, IAMFullAccess, PowerUserAccess\", \n \"actionName\": \"IamRolesAccessPermissionsAction\", \"evaluateName\": \"IamRolesAccessPermissionsEvaluate\",   \"resourceFetcherName\" : \"IamRolesAccessPermissionsResourceFetcher\",  \"moduleName\": \"iam_roles_excess_permissions\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\"}",
  "eventLeftScope": "False",
  "executionRoleArn": "arn:aws:iam::693265998683:role/awsconfig-role",
  "accountId": "693265998683"
}

CONTEXT = ""


class TestIamRoleExcessPermissionsFetcher(unittest.TestCase):
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __fetchIamRoles = IamRolesAccessPermissionsResourceFetcher(__eventParam)

    def testIamRolesResourceFetcher(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getResourceFetcherMock('fetch_roles')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__fetchIamRoles.resourceFetcher()
        assert return_value

    def testIamRolesResourceFetcherNoData(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getResourceFetcherMock('fetch_roles_blank_response')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__fetchIamRoles.resourceFetcher()
        assert not return_value

    def testIamRolesResourceFetcherException(self):
        recordedMockResponsePath = 'tests/common_unit_testcase_responses/placebo_recorded_responses/exception'
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__fetchIamRoles.resourceFetcher()
        assert not return_value

    def testIamRolesResourceFetcherClientException(self):
        recordedMockResponsePath = 'tests/common_unit_testcase_responses/placebo_recorded_responses/client_exception'
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__fetchIamRoles.resourceFetcher()
        assert not return_value

    def testIamRolesResourceFetcherTypeException(self):
        recordedMockResponsePath = 'tests/common_unit_testcase_responses/placebo_recorded_responses/type_error'
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__fetchIamRoles.resourceFetcher()
        assert not return_value
