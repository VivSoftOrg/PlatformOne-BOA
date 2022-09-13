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

from tests.enforce_allow_deny_groups_to_iam_users.test_enforce_allow_deny_groups_to_iam_users_placebo_initializer import *
from enforce_allow_deny_groups_to_iam_users.enforce_allow_deny_groups_to_iam_users_action import *
from enforce_allow_deny_groups_to_iam_users.enforce_allow_deny_groups_to_iam_users_constants import *
import common.compliance_object_factory as complianceObjectFactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import *
from common.common_utility import CommonUtility

RESOURCE_ID = "AIDSDFISDFS"

EVENT_JSON = {
  "configRuleId": "config-rule-1v52mx",
  "version": "1.0",
  "configRuleName": "enforce_allow_deny_groups_to_iam_users",
  "configRuleArn": "arn:aws:config:us-east-1:693265998683:config-rule/config-rule-1v52mx",
  "invokingEvent": "{\n  \"configurationItemDiff\": null,\n   \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
  "resultToken": "",
  "ruleParameters": "{\"performAction\": \"True\", \"groupsName\": \"DenyGroupName, AllowGroupName\", \"excludeUsers\": \"\", \"actionName\": \"EnforceAllowAndDenyGroupsAction\", \"evaluateName\": \"EnforceAllowAndDenyGroupsEvaluate\",   \"resourceFetcherName\" : \"EnforceAllowAndDenyGroupsResourceFetcher\",  \"moduleName\": \"enforce_allow_deny_groups_to_iam_users\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\"}",
  "eventLeftScope": "False",
  "executionRoleArn": "arn:aws:iam::693265998683:role/awsconfig-role",
  "accountId": "693265998683"
}

CONTEXT = ''

class TestEnforceAllowAndDenyGroupsAction:

    _AbstractAction__eventParam = complianceObjectFactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __ADD_TO_ALLOW_GROUP_CONFIG_ITEM = {
        'Groups': ['AllowGroupName']
    }

    __ADD_TO_DENY_GROUP_CONFIG_ITEM = {
        'Groups': ['DenyGroupName']
    }

    __enforceGroupsAction = EnforceAllowAndDenyGroupsAction(_AbstractAction__eventParam)

    def testAddUserToAllowGroupFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=self.__ADD_TO_ALLOW_GROUP_CONFIG_ITEM)
        return_value = self.__enforceGroupsAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testAddUserToDenyGroupFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=self.__ADD_TO_DENY_GROUP_CONFIG_ITEM)
        return_value = self.__enforceGroupsAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testAddUserToDenyGroupException(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=self.__ADD_TO_DENY_GROUP_CONFIG_ITEM)
        return_value = self.__enforceGroupsAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE