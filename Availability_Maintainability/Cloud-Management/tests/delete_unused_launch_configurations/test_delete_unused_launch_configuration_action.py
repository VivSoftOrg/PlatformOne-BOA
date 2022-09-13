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
sys.path.append('../../')
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.abstract_evaluate import *
from common.abstract_action import *
from common.common_constants import *
from mock import MagicMock
from moto import *
from botocore.exceptions import ClientError
import delete_unused_launch_configurations.delete_unused_launch_configurations_action as launchConfigurationAction
from datetime import datetime
from datetime import timedelta
from dateutil.tz import tzutc

EVENT_JSON = {
  "version": "1.0",
  "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-12-07T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
  "ruleParameters": "{\n  \"toEmail\": \"ankush.tehele@reancloud.com\", \"forbiddenPorts\": \"22\",\n  \"performAction\": \"True\",\n  \"notifier\": \"ses\" \n}",
  "resultToken": " ",
  "eventLeftScope": "False",
  "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
  "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-zgvfqq",
  "configRuleName": "gaurav-test",
  "configRuleId": "config-rule-zgvfqq",
  "accountId": "107339370656"
}

CONTEXT = ""

RESOURCE_ID = 'testLaunchConfig'
RESOURCE_TYPE = "AWS::AutoScaling::LaunchConfiguration"
CONFIG_ITEMS = {'classiclinkvpcsecuritygroups': [], 'region': 'us-east-2', 'securitygroups': ['sg-e38dce8b'], 'blockdevicemappings': [{'ebs': {'volumetype': 'gp2', 'volumesize': 8, 'deleteontermination': True, 'snapshotid': 'snap-04a508523b761d796'}, 'devicename': '/dev/sda1'}], 'createdtime': datetime(2017, 11, 15, 10, 41, 56, 834000, tzinfo=tzutc()), 'keyname': 'datta_key', 'imageid': 'ami-43391926', 'launchconfigurationname': 'useful', 'instancemonitoring': {'enabled': False}, 'kernelid': '', 'userdata': '', 'ramdiskid': '', 'launchconfigurationarn': 'arn:aws:autoscaling:us-east-2:107339370656:launchConfiguration:fd14dcf9-f8f7-4bc9-b65a-306346b35e0f:launchConfigurationName/useful', 'ebsoptimized': False, 'instancetype': 't2.micro'}


class TestEc2NoshutdownTagAction(object):

    __regions = ['us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __mockInstanceResponse = {'ResponseMetadata': {'HTTPStatusCode': 200, 'RetryAttempts': 0}}
    __mockInstanceResponse_fail = {'ResponseMetadata': {'HTTPStatusCode': 500, 'RetryAttempts': 0}}
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
    __deleteUnusedLaunchConfigurationsAction = launchConfigurationAction.DeleteUnusedLaunchConfigurationsAction(__eventParam)
    __errorResponse = {'Error':{
        'Code':400,
        'Message':'AccessDenied'
    }}

    @mock_autoscaling
    def test_delete_launch_configuration_success(self):
        asgClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ASC,self.__regions[0])
        launchConfigurationAction.BotoUtility.getClient = MagicMock(return_value=asgClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        asgClient.delete_launch_configuration = MagicMock(return_value=self.__mockInstanceResponse)
        evaluationResult = self.__deleteUnusedLaunchConfigurationsAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

    @mock_autoscaling
    def test_delete_launch_configuration_failure(self):
        asgClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ASC,self.__regions[0])
        launchConfigurationAction.BotoUtility.getClient = MagicMock(return_value=asgClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        asgClient.delete_launch_configuration = MagicMock(return_value=self.__mockInstanceResponse_fail)
        evaluationResult = self.__deleteUnusedLaunchConfigurationsAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_autoscaling
    def test_delete_launch_configuration_exception_key_error(self):
        asgClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ASC,self.__regions[0])
        launchConfigurationAction.BotoUtility.getClient = MagicMock(return_value=asgClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        asgClient.delete_launch_configuration = MagicMock(side_effect=KeyError("Mock Exception: Key not found error"))
        evaluationResult = self.__deleteUnusedLaunchConfigurationsAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_autoscaling
    def test_delete_launch_configuration_exception_value_error(self):
        asgClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ASC,self.__regions[0])
        launchConfigurationAction.BotoUtility.getClient = MagicMock(return_value=asgClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        asgClient.delete_launch_configuration = MagicMock(side_effect=ValueError("Mock Exception: Value not found error"))
        evaluationResult = self.__deleteUnusedLaunchConfigurationsAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_autoscaling
    def test_delete_launch_configuration_exception_attribute_error(self):
        asgClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ASC,self.__regions[0])
        launchConfigurationAction.BotoUtility.getClient = MagicMock(return_value=asgClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        asgClient.delete_launch_configuration = MagicMock(side_effect=AttributeError("Mock Exception: Attribute not found error"))
        evaluationResult = self.__deleteUnusedLaunchConfigurationsAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_autoscaling
    def test_delete_launch_configuration_exception_client_error(self):
        asgClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ASC,self.__regions[0])
        launchConfigurationAction.BotoUtility.getClient = MagicMock(return_value=asgClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        asgClient.delete_launch_configuration = MagicMock(side_effect=ClientError(self.__errorResponse,"AssumeRole"))
        evaluationResult = self.__deleteUnusedLaunchConfigurationsAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_autoscaling
    def test_delete_launch_configuration_exception_error(self):
        asgClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ASC,self.__regions[0])
        launchConfigurationAction.BotoUtility.getClient = MagicMock(return_value=asgClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        asgClient.delete_launch_configuration = MagicMock(side_effect=Exception("Mock Exception: Resource not found error"))
        evaluationResult = self.__deleteUnusedLaunchConfigurationsAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION
