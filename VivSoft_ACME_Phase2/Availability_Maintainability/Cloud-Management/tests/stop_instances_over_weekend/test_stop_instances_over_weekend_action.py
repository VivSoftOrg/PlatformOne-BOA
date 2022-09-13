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
import boto3
import sys
import os
from mock import MagicMock
from moto import mock_ec2

sys.path.append('../../')

import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
import stop_instances_over_weekend.stop_instances_over_weekend_action as noShutTag
# import stop_instances_over_weekend.stop_instances_over_weekend_constants as noShutTagConstants

from common.common_constants import *
from common.abstract_evaluate import *
RESOURCE_ID = "ebs-xyz"
RESOURCE_TYPE = AWSResourceClassConstants.EC2_INSTANCE
CONFIG_ITEMS = {"region": "us-east-1"}

EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-08-21T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
    "ruleParameters": "{\"performAction\":\"True\",\"notifier\":\"sns\",\"toEmail\":\"akshay.deshpande@reancloud.com\"}",
    "resultToken": "",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-zgvfqq",
    "configRuleName": "gaurav-test",
    "configRuleId": "config-rule-zgvfqq",
    "accountId": "107339370656"
}
CONTEXT = ""


class TestStopInstancesOverWeekendAction(object):

    __regions = ['us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __mockInstanceResponse = {'ResponseMetadata': {'HTTPStatusCode': 200}}
    __mockInstanceResponse_fail = {'ResponseMetadata': {'HTTPStatusCode': 500}}

    @mock_ec2
    def test_perform_action(self):
        self._AbstractAction__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        ec2Client = boto3.client('ec2', self.__regions[0])
        ec2Client.stop_instances = MagicMock(return_value=self.__mockInstanceResponse)
        noShutTag.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        return_value = noShutTag.StopInstancesOverWeekendAction.performAction(self, eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_ec2
    def testPerformActionFailure(self):
        self._AbstractAction__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__regions[0])
        noShutTag.BotoUtility.getClient = MagicMock(return_value=ec2Client)        
        ec2Client.stop_instances = MagicMock(return_value=self.__mockInstanceResponse_fail)
        return_value = noShutTag.StopInstancesOverWeekendAction.performAction(self, eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_ec2
    def testPerformActionRaisesException(self):
        self._AbstractAction__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__regions[0])
        noShutTag.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.stop_instances = MagicMock(side_effect=Exception("Failed to Stop Instance on weekend."))
        return_value = noShutTag.StopInstancesOverWeekendAction.performAction(self, eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION
