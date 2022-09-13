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

from delete_unused_ebs.delete_unused_ebs_action import *
from common.common_constants import AWSResourceClassConstants, ComplianceConstants
from tests.delete_unused_ebs.test_delete_unused_ebs_placebo_initializer import *
import common.compliance_object_factory as complianceObjectFactory
from common.compliance_object_factory import ComplianceObjectFactory

RESOURCE_ID = "VolumeId"
RESOURCE_TYPE = AWSResourceClassConstants.EBS_VOLUME

EVENT_JSON = {
      "configRuleId": "config-rule-1v52mx",
      "version": "1.0",
      "configRuleName": "aws-sample-rule",
      "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-1v52mx",
      "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
      "resultToken": "",
      "ruleParameters": "{\"age\": \"0\", \n \"expirationDateLimit\": \"20\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
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

    __unsedEBSAction = DeleteUnusedEBSAction(_AbstractAction__eventParam)

    __configItems = {
        'tags':[{
           'key':'Name', 'value':'Volume Name'
        }],
        'region': 'us-east-1'
    }

    def testPerformActionCreateSnapshotSuccess(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('create_snapshot/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__unsedEBSAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testPerformActionCreateSnapshotFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('create_snapshot/failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__unsedEBSAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    def testPerformActionCreateSnapshotException(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('create_snapshot/exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__unsedEBSAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    def testPerformActionDeleteVolumeSuccess(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_volume/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__unsedEBSAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testPerformActionDeleteVolumeFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_volume/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__unsedEBSAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testPerformActionDeleteVolumeException(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_volume/failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__unsedEBSAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

