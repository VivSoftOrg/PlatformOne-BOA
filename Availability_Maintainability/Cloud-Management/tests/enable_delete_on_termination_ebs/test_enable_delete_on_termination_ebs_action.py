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
from enable_delete_on_termination_ebs.enable_delete_on_termination_ebs_action import *
from tests.enable_delete_on_termination_ebs.test_enable_delete_on_termination_ebs_placebo_initializer import *
import common.compliance_object_factory as complianceObjectFactory

EVENT_JSON_DELETE_ON_TERMINATION_NOT_ENABLED = {
    "version": "1.0",
    "invokingEvent": "{\"configurationItemDiff\": null,\"configurationItem\": {\"configuration\": {\"Region\": \"us-east-1\", \"state\": {\"code\": 80,\"name\": \"running\"},\"blockDeviceMappings\": [{\"deviceName\": \"/dev/xvda\",\"ebs\": {\"attachTime\": \"2017-12-28T06:44:33.000Z\",\"deleteOnTermination\": false,\"status\": \"attached\",\"volumeId\": \"vol-0363f54fc5e3d9906\"}}]},\"awsAccountId\": \"107339370656\",\"configurationItemStatus\": \"OK\",\"resourceType\": \"AWS::EC2::Instance\",\"resourceId\": \"i-05b8ba2c066f455ec\",\"resourceName\": null,\"ARN\": \"arn:aws:ec2:us-east-1:107339370656:instance/i-05b8ba2c066f455ec\",\"awsRegion\": \"us-east-1\",\"availabilityZone\": \"us-east-1a\",\"configurationStateMd5Hash\": \"baf6a69a8c9fbb6129d758c2acb84c56\",\"resourceCreationTime\": \"2018-01-02T08:47:25.000Z\"},\"notificationCreationTime\": \"2018-01-03T09:58:11.794Z\",\"messageType\": \"ConfigurationItemChangeNotification\",\"recordVersion\": \"1.2\"}",
    "ruleParameters": "{\n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
    "resultToken": "eyJlbmNyeXB0ZWREYXRhIjpbN",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-xbqpcp",
    "configRuleName": "testRule",
    "configRuleId": "config-rule-xbqpcp",
    "accountId": "107339370656"
}

CONTEXT = ''


class TestEnableDeleteOnTerminationEBSAction:

    _AbstractAction__eventParam = complianceObjectFactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON_DELETE_ON_TERMINATION_NOT_ENABLED,
        CONTEXT
    )

    __ec2InstanceAction = EnableDeleteOnTerminationEBSAction(_AbstractAction__eventParam)

    __eventItem = complianceObjectFactory.ComplianceObjectFactory.createEventItemFrom(EVENT_JSON_DELETE_ON_TERMINATION_NOT_ENABLED, CONTEXT, _AbstractAction__eventParam)

    def testPerformActionModifyInstanceAttribute(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('modify_instance_attribute/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__ec2InstanceAction.performAction(self.__eventItem[0])
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testPerformActionModifyInstanceAttributeFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('modify_instance_attribute/failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__ec2InstanceAction.performAction(self.__eventItem[0])
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformActionModifyInstanceAttributeException(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('modify_instance_attribute/exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__ec2InstanceAction.performAction(self.__eventItem[0])
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

