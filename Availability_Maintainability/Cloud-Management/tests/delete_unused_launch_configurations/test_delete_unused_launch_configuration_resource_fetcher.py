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
from mock import MagicMock
from moto import *
from botocore.exceptions import ClientError
from common.common_constants import *
import common.compliance_object_factory as complianceobjectfactory
import delete_unused_launch_configurations.delete_unused_launch_configurations_resource_fetcher as launchConfigurationFetcher


EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-08-21T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
    "ruleParameters": "{\"performAction\": \"True\",\"notifier\": \"sns\",\"toEmail\": \"priyanka.khairnar@reancloud.com\"}",
    "resultToken": "eyJlbmNyeXB0ZWREYXRhIjpbNTAsNzgsNTIsMjksMTEyLDEwLDIwLDk2LC03Niw4OCwtODYsLTEyMywtODEsLTc3LDkxLC0xMTIsMzcsLTcwLDEwMSwtNTMsOTEsLTEwLDEyMiwzLDk5LC00MSwyMSw5OSw1NywxMDcsLTEyMSwtNDEsLTMsOTksLTU5LDQxLDIxLC0yMywxNSw1MSwtNjgsNTksLTM3LDEwNSwtOSwtMTQsMTI0LDg0LC00OSwzNiwxMCwzOCwtNzMsMTI0LDQ1LC0xLC0yNiwzMCw0Myw4NCwxMiwtNDIsLTc2LC0zLDMsMTEwLDU2LC01OCwtMzMsLTQwLDIwLC03OCwtODgsNywxMDUsLTM1LC0zOCwtODIsLTUwLDQ1LDM0LDExLDExNCwtODYsLTEsLTExNiwtOTIsLTMsMTUsLTczLDU5LDU3LC03OSwtMTIsLTEwMyw3NSwtNjIsLTMzLC0xMDMsLTIsLTUyLDM2LC0xMDUsLTEwOCwtNDcsNzQsMywtNCw5MCwzLDExNiwtOTMsOTAsMTE1LC03MCw1NSwtNTgsNzgsNDYsNjcsMjksLTg1LC01MSwzNSwtMTI2LDc3LDk2LC0yMiwtMTUsNjUsMTUsMjgsNjIsLTU0LC00NiwtNDgsLTUwLDc3LC0zNywtNjYsLTEyMSwtMzgsLTQsMTE4LC03LDE5LC02MSwtMTIzLDIwLDYyLC04Myw0NSwyOSwtMTAsMTI0LC02NSw3NSwtMTI0LDQ0LC02MywtMjcsMjcsLTMxLDk5LDY3LDAsMTIxLC05NywtMjEsLTcxLDMzLDg1LC0xMTQsLTUxLDEyNyw1NCwtMTAyLDcwLC03NCw4LDc0LC0xMjYsNDIsLTIzLDU2LC05OCwtMTA4LDgxLC0xMjgsMTEyLDE5LC03Myw3NCwtODgsLTY1LDc4LDc2LC0xMjYsLTE2LDExOCwtMTEyLDIsLTUyLDY3LC01Myw3NCwxMTYsLTc3LDcyLDk5LC0xNiwtMTAwLC05OSwtMTksOTEsNDksNSwtNzEsLTgsLTYyLDEyNywtMTEsLTQ0LDEyNywtODksNTEsODIsNjEsLTgxLDk4LDU2LC00Miw5MSw2LDI4LC0xNSwyMSwxOSw0MCwxMDgsMTA5LC04LDEyNCwzOSwtNjUsLTU3LDkwLC0xMDEsMTA2LC0yMSwxMTEsLTExOSw2NSw2LC01NSw5MSwtMzUsMTYsLTExOCwtMTA1LDgzLDQ0LDgwXSwibWF0ZXJpYWxTZXRTZXJpYWxOdW1iZXIiOjEsIml2UGFyYW1ldGVyU3BlYyI6eyJpdiI6WzkxLDc1LC03MywtMzEsNCw4LC0yMyw3OSwtODUsLTg1LDIsMTI3LDEyMywtNDksNCw4NV19fQ==eyJlbmNyeXB0ZWREYXRhIjpbNTAsNzgsNTIsMjksMTEyLDEwLDIwLDk2LC03Niw4OCwtODYsLTEyMywtODEsLTc3LDkxLC0xMTIsMzcsLTcwLDEwMSwtNTMsOTEsLTEwLDEyMiwzLDk5LC00MSwyMSw5OSw1NywxMDcsLTEyMSwtNDEsLTMsOTksLTU5LDQxLDIxLC0yMywxNSw1MSwtNjgsNTksLTM3LDEwNSwtOSwtMTQsMTI0LDg0LC00OSwzNiwxMCwzOCwtNzMsMTI0LDQ1LC0xLC0yNiwzMCw0Myw4NCwxMiwtNDIsLTc2LC0zLDMsMTEwLDU2LC01OCwtMzMsLTQwLDIwLC03OCwtODgsNywxMDUsLTM1LC0zOCwtODIsLTUwLDQ1LDM0LDExLDExNCwtODYsLTEsLTExNiwtOTIsLTMsMTUsLTczLDU5LDU3LC03OSwtMTIsLTEwMyw3NSwtNjIsLTMzLC0xMDMsLTIsLTUyLDM2LC0xMDUsLTEwOCwtNDcsNzQsMywtNCw5MCwzLDExNiwtOTMsOTAsMTE1LC03MCw1NSwtNTgsNzgsNDYsNjcsMjksLTg1LC01MSwzNSwtMTI2LDc3LDk2LC0yMiwtMTUsNjUsMTUsMjgsNjIsLTU0LC00NiwtNDgsLTUwLDc3LC0zNywtNjYsLTEyMSwtMzgsLTQsMTE4LC03LDE5LC02MSwtMTIzLDIwLDYyLC04Myw0NSwyOSwtMTAsMTI0LC02NSw3NSwtMTI0LDQ0LC02MywtMjcsMjcsLTMxLDk5LDY3LDAsMTIxLC05NywtMjEsLTcxLDMzLDg1LC0xMTQsLTUxLDEyNyw1NCwtMTAyLDcwLC03NCw4LDc0LC0xMjYsNDIsLTIzLDU2LC05OCwtMTA4LDgxLC0xMjgsMTEyLDE5LC03Myw3NCwtODgsLTY1LDc4LDc2LC0xMjYsLTE2LDExOCwtMTEyLDIsLTUyLDY3LC01Myw3NCwxMTYsLTc3LDcyLDk5LC0xNiwtMTAwLC05OSwtMTksOTEsNDksNSwtNzEsLTgsLTYyLDEyNywtMTEsLTQ0LDEyNywtODksNTEsODIsNjEsLTgxLDk4LDU2LC00Miw5MSw2LDI4LC0xNSwyMSwxOSw0MCwxMDgsMTA5LC04LDEyNCwzOSwtNjUsLTU3LDkwLC0xMDEsMTA2LC0yMSwxMTEsLTExOSw2NSw2LC01NSw5MSwtMzUsMTYsLTExOCwtMTA1LDgzLDQ0LDgwXSwibWF0ZXJpYWxTZXRTZXJpYWxOdW1iZXIiOjEsIml2UGFyYW1ldGVyU3BlYyI6eyJpdiI6WzkxLDc1LC03MywtMzEsNCw4LC0yMyw3OSwtODUsLTg1LDIsMTI3LDEyMywtNDksNCw4NV19fQ==eyJlbmNyeXB0ZWREYXRhIjpbNTAsNzgsNTIsMjksMTEyLDEwLDIwLDk2LC03Niw4OCwtODYsLTEyMywtODEsLTc3LDkxLC0xMTIsMzcsLTcwLDEwMSwtNTMsOTEsLTEwLDEyMiwzLDk5LC00MSwyMSw5OSw1NywxMDcsLTEyMSwtNDEsLTMsOTksLTU5LDQxLDIxLC0yMywxNSw1MSwtNjgsNTksLTM3LDEwNSwtOSwtMTQsMTI0LDg0LC00OSwzNiwxMCwzOCwtNzMsMTI0LDQ1LC0xLC0yNiwzMCw0Myw4NCwxMiwtNDIsLTc2LC0zLDMsMTEwLDU2LC01OCwtMzMsLTQwLDIwLC03OCwtODgsNywxMDUsLTM1LC0zOCwtODIsLTUwLDQ1LDM0LDExLDExNCwtODYsLTEsLTExNiwtOTIsLTMsMTUsLTczLDU5LDU3LC03OSwtMTIsLTEwMyw3NSwtNjIsLTMzLC0xMDMsLTIsLTUyLDM2LC0xMDUsLTEwOCwtNDcsNzQsMywtNCw5MCwzLDExNiwtOTMsOTAsMTE1LC03MCw1NSwtNTgsNzgsNDYsNjcsMjksLTg1LC01MSwzNSwtMTI2LDc3LDk2LC0yMiwtMTUsNjUsMTUsMjgsNjIsLTU0LC00NiwtNDgsLTUwLDc3LC0zNywtNjYsLTEyMSwtMzgsLTQsMTE4LC03LDE5LC02MSwtMTIzLDIwLDYyLC04Myw0NSwyOSwtMTAsMTI0LC02NSw3NSwtMTI0LDQ0LC02MywtMjcsMjcsLTMxLDk5LDY3LDAsMTIxLC05NywtMjEsLTcxLDMzLDg1LC0xMTQsLTUxLDEyNyw1NCwtMTAyLDcwLC03NCw4LDc0LC0xMjYsNDIsLTIzLDU2LC05OCwtMTA4LDgxLC0xMjgsMTEyLDE5LC03Myw3NCwtODgsLTY1LDc4LDc2LC0xMjYsLTE2LDExOCwtMTEyLDIsLTUyLDY3LC01Myw3NCwxMTYsLTc3LDcyLDk5LC0xNiwtMTAwLC05OSwtMTksOTEsNDksNSwtNzEsLTgsLTYyLDEyNywtMTEsLTQ0LDEyNywtODksNTEsODIsNjEsLTgxLDk4LDU2LC00Miw5MSw2LDI4LC0xNSwyMSwxOSw0MCwxMDgsMTA5LC04LDEyNCwzOSwtNjUsLTU3LDkwLC0xMDEsMTA2LC0yMSwxMTEsLTExOSw2NSw2LC01NSw5MSwtMzUsMTYsLTExOCwtMTA1LDgzLDQ0LDgwXSwibWF0ZXJpYWxTZXRTZXJpYWxOdW1iZXIiOjEsIml2UGFyYW1ldGVyU3BlYyI6eyJpdiI6WzkxLDc1LC03MywtMzEsNCw4LC0yMyw3OSwtODUsLTg1LDIsMTI3LDEyMywtNDksNCw4NV19fQ==",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-zgvfqq",
    "configRuleName": "gaurav-test",
    "configRuleId": "config-rule-zgvfqq",
    "accountId": "107339370656"
}

CONTEXT = ""

class TestUnusedRouteTableFetcher(object):
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __regions = [ 'us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __deleteUnusedLaunchConfigurationsFetcher=launchConfigurationFetcher.DeleteUnusedLaunchConfigurationsFetcher(__eventParam)
    __errorResponse = {'Error':{
        'Code':400,
        'Message':'AccessDenied'
    }}

    @mock_autoscaling
    def test_resource_fetcher_with_data(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        asgClient = boto3.client('autoscaling',self.__regions[0])
        launchConfigurationFetcher.BotoUtility.getClient = MagicMock(return_value=asgClient)
        
        response = asgClient.create_launch_configuration(
            LaunchConfigurationName="testLC",
            ImageId='ami-8e1fece7',
            InstanceType='t2.micro',
        )
        return_value = self.__deleteUnusedLaunchConfigurationsFetcher.resourceFetcher()
        assert bool(return_value) == True

    @mock_autoscaling
    def test_resource_fetcher_failure_key_error(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        asgClient = boto3.client('autoscaling', self.__regions[0])
        launchConfigurationFetcher.BotoUtility.getClient = MagicMock(return_value=asgClient)
        asgClient.get_paginator = MagicMock(side_effect=KeyError("Key not found error"))
        return_value = self.__deleteUnusedLaunchConfigurationsFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_autoscaling
    def test_resource_fetcher_without_data(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        asgClient = boto3.client('autoscaling',self.__regions[0])
        launchConfigurationFetcher.BotoUtility.getClient = MagicMock(return_value=asgClient)
        return_value = self.__deleteUnusedLaunchConfigurationsFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_autoscaling
    def test_resource_fetcher_failure_value_error(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        asgClient = boto3.client('autoscaling', self.__regions[0])
        launchConfigurationFetcher.BotoUtility.getClient = MagicMock(return_value=asgClient)
        asgClient.get_paginator = MagicMock(side_effect=ValueError("Value not found error"))
        return_value = self.__deleteUnusedLaunchConfigurationsFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_autoscaling
    def test_resource_fetcher_failure_attribute_error(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        asgClient = boto3.client('autoscaling', self.__regions[0])
        launchConfigurationFetcher.BotoUtility.getClient = MagicMock(return_value=asgClient)
        asgClient.get_paginator = MagicMock(side_effect=AttributeError("Attribute not found error"))
        return_value = self.__deleteUnusedLaunchConfigurationsFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_autoscaling
    def test_resource_fetcher_failure_syntax_error(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        asgClient = boto3.client('autoscaling', self.__regions[0])
        launchConfigurationFetcher.BotoUtility.getClient = MagicMock(return_value=asgClient)
        asgClient.get_paginator = MagicMock(side_effect=SyntaxError("Incorrect syntax"))
        return_value = self.__deleteUnusedLaunchConfigurationsFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_autoscaling
    def test_resource_fetcher_failure_client_error(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        asgClient = boto3.client('autoscaling', self.__regions[0])
        launchConfigurationFetcher.BotoUtility.getClient = MagicMock(return_value=asgClient)
        asgClient.get_paginator = MagicMock(side_effect=ClientError(self.__errorResponse,"AssumeRole"))
        return_value = self.__deleteUnusedLaunchConfigurationsFetcher.resourceFetcher()
        assert bool(return_value) == False