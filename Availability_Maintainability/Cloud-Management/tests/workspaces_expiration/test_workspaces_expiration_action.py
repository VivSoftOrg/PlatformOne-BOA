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
from common.common_constants import AWSResourceClassConstants
from workspaces_expiration.workspaces_expiration_action import *
from tests.workspaces_expiration.test_workspaces_expiration_placebo_initializer import *
import common.compliance_object_factory as complianceObjectFactory
from common.compliance_object_factory import ComplianceObjectFactory

RESOURCE_ID = "Service Name"
RESOURCE_TYPE = AWSResourceClassConstants.WORKSPACES_RESOURCE

EVENT_JSON = {
      "configRuleId": "config-rule-1v52mx",
      "version": "1.0",
      "configRuleName": "aws-sample-rule",
      "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-1v52mx",
      "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
      "resultToken": "",
      "ruleParameters": "{\"validity\": \"10\", \n \"expirationDateLimit\": \"20\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
      "eventLeftScope": "False",
      "executionRoleArn": "arn:aws:iam::107339370656:role/awsconfig-role",
      "accountId": "107339370656"
}

CONTEXT = ''

class TestWorkSpaceAction:

    _AbstractAction__eventParam = complianceObjectFactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __workSpaceAction = WorkSpacesAction(_AbstractAction__eventParam)

    __configItems = {
        'resourceName': 'MockWorkSpace',
        'region': 'us-east-1'
    }

    def testPerformActionAddExpirationTag(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('add_tag/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({"State": 'AVAILABLE'})
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__workSpaceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE and return_value.annotation == "Expiration Date added to Workspace Successfully."

    def testPerformActionAddExpirationTagFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('add_tag/failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({"State": 'AVAILABLE'})
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__workSpaceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE and return_value.annotation == "Expiration Date added to Workspace Successfully."

    def testPerformActionAddExpirationTagRaisesException(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('add_tag/exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({"State": 'AVAILABLE'})
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__workSpaceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE and return_value.annotation == "Expiration Date added to Workspace Successfully."

    def testPerformActionDeleteWorkSpace(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_workspace/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({"State": 'AVAILABLE'})
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_VALIDITY_EXPIRED})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__workSpaceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE and return_value.annotation == "Workspace deleted Successfully."

    def testPerformActionDeleteWorkSpaceWhenSuspended(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_workspace/success')
        self.__configItems.update({"State": 'SUSPENDED'})
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_VALIDITY_EXPIRED})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__workSpaceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE and return_value.annotation == 'Cannot Terminate WorkSpace during SUSPENDED State.'

    def testPerformActionDeleteWorkSpaceFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_workspace/failure')
        self.__configItems.update({"State": 'AVAILABLE'})
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_VALIDITY_EXPIRED})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__workSpaceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE and return_value.annotation == "Workspace deleted Successfully."


    def testPerformActionDeleteWorkSpaceRaiseException(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_workspace/exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({"State": 'AVAILABLE'})
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_VALIDITY_EXPIRED})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__workSpaceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE and return_value.annotation == "Workspace deleted Successfully."

    def testPerformActionServiceAboutToExpire(self):
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_ABOUT_TO_EXPIRE})
        self.__configItems.update({"State": 'AVAILABLE'})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__workSpaceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE and return_value.annotation == "Workspace is about to Expire."
