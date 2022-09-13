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

from active_iam_users.active_iam_users_action import *
from tests.active_iam_users.test_active_iam_users_placebo_initializer import *
import common.compliance_object_factory as complianceObjectFactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import *
from common.common_utility import CommonUtility

RESOURCE_ID = "AIDSDFISDFSDF"

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

CONTEXT = ''

class TestActiveIamUsersAction:

    _AbstractAction__eventParam = complianceObjectFactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __DISABLE_USER_CONFIG_ITEM = {
        "NON_COMPLAINT_RESOURCE_ACTION": "deleteWarnings",
        "username": "devendra.suthar",
        "passworddisabled": False
    }

    __DELETE_USER_CONFIG_ITEM = {
        "NON_COMPLAINT_RESOURCE_ACTION": "deleteuser",
        "username": "devendra.suthar",
        "passworddisabled": False
    }

    __FAILED_TO_GET_LOGING_PROFILE_USER_CONFIG_ITEM = {
        "NON_COMPLAINT_RESOURCE_ACTION": "deleteWarnings",
        "username": "devendra.suthar",
        "passworddisabled": True
    }
    __DISABLE_WARNING_USER_CONFIG_ITEM = {
        "NON_COMPLAINT_RESOURCE_ACTION": "disableWarnings",
        "username": "devendra.suthar",
        "passworddisabled": False
    }


    __activeIamUsersAction = ActiveIamUsersAction(_AbstractAction__eventParam)

    def testPerformDeleteUserSuccess(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_user/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=self.__DELETE_USER_CONFIG_ITEM)
        return_value = self.__activeIamUsersAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testPerformDeleteUserFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_user/failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=self.__DELETE_USER_CONFIG_ITEM)
        return_value = self.__activeIamUsersAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformDeleteUserProfileSuccess(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('disable_user/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=self.__DISABLE_USER_CONFIG_ITEM)
        return_value = self.__activeIamUsersAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformDeleteUserProfileFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('disable_user/failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=self.__DISABLE_USER_CONFIG_ITEM)
        return_value = self.__activeIamUsersAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformGetUserProfileFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('disable_user/failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=self.__FAILED_TO_GET_LOGING_PROFILE_USER_CONFIG_ITEM)
        return_value = self.__activeIamUsersAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformDeleteUserProfileException(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('disable_user/exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=CommonUtility.changeDictionaryKeysToLowerCase(self.__DISABLE_USER_CONFIG_ITEM))
        return_value = self.__activeIamUsersAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    def testPerformDisbaleWarningSucess(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('disable_user/exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=self.__DISABLE_WARNING_USER_CONFIG_ITEM)
        return_value = self.__activeIamUsersAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
