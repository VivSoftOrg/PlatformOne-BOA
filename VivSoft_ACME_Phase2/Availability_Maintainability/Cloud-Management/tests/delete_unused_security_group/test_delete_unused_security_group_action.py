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
from common.common_constants import *
from mock import MagicMock
from moto import mock_ec2
from botocore.exceptions import ClientError
import delete_unused_security_group.delete_unused_security_group_action as sgAction


EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-12-07T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
    "ruleParameters": "{\n  \"toEmail\": \"ankush.tehele@reancloud.com\", \"forbiddenPorts\": \"0-65535\",\n  \"performAction\": \"True\",\n  \"excludedPorts\": \"80, 443\",\n  \"excludedGroupsName\": \"abc\",\n  \"notifier\": \"email\" \n}",
    "resultToken": "eyJlbmNyeXB0ZWREYXRhIjpbNTAsNzgsNTIsMjksMTEyLDEwLDIwLDk2LC03Niw4OCwtODYsLTEyMywtODEsLTc3LDkxLC0xMTIsMzcsLTcwLDEwMSwtNTMsOTEsLTEwLDEyMiwzLDk5LC00MSwyMSw5OSw1NywxMDcsLTEyMSwtNDEsLTMsOTksLTU5LDQxLDIxLC0yMywxNSw1MSwtNjgsNTksLTM3LDEwNSwtOSwtMTQsMTI0LDg0LC00OSwzNiwxMCwzOCwtNzMsMTI0LDQ1LC0xLC0yNiwzMCw0Myw4NCwxMiwtNDIsLTc2LC0zLDMsMTEwLDU2LC01OCwtMzMsLTQwLDIwLC03OCwtODgsNywxMDUsLTM1LC0zOCwtODIsLTUwLDQ1LDM0LDExLDExNCwtODYsLTEsLTExNiwtOTIsLTMsMTUsLTczLDU5LDU3LC03OSwtMTIsLTEwMyw3NSwtNjIsLTMzLC0xMDMsLTIsLTUyLDM2LC0xMDUsLTEwOCwtNDcsNzQsMywtNCw5MCwzLDExNiwtOTMsOTAsMTE1LC03MCw1NSwtNTgsNzgsNDYsNjcsMjksLTg1LC01MSwzNSwtMTI2LDc3LDk2LC0yMiwtMTUsNjUsMTUsMjgsNjIsLTU0LC00NiwtNDgsLTUwLDc3LC0zNywtNjYsLTEyMSwtMzgsLTQsMTE4LC03LDE5LC02MSwtMTIzLDIwLDYyLC04Myw0NSwyOSwtMTAsMTI0LC02NSw3NSwtMTI0LDQ0LC02MywtMjcsMjcsLTMxLDk5LDY3LDAsMTIxLC05NywtMjEsLTcxLDMzLDg1LC0xMTQsLTUxLDEyNyw1NCwtMTAyLDcwLC03NCw4LDc0LC0xMjYsNDIsLTIzLDU2LC05OCwtMTA4LDgxLC0xMjgsMTEyLDE5LC03Myw3NCwtODgsLTY1LDc4LDc2LC0xMjYsLTE2LDExOCwtMTEyLDIsLTUyLDY3LC01Myw3NCwxMTYsLTc3LDcyLDk5LC0xNiwtMTAwLC05OSwtMTksOTEsNDksNSwtNzEsLTgsLTYyLDEyNywtMTEsLTQ0LDEyNywtODksNTEsODIsNjEsLTgxLDk4LDU2LC00Miw5MSw2LDI4LC0xNSwyMSwxOSw0MCwxMDgsMTA5LC04LDEyNCwzOSwtNjUsLTU3LDkwLC0xMDEsMTA2LC0yMSwxMTEsLTExOSw2NSw2LC01NSw5MSwtMzUsMTYsLTExOCwtMTA1LDgzLDQ0LDgwXSwibWF0ZXJpYWxTZXRTZXJpYWxOdW1iZXIiOjEsIml2UGFyYW1ldGVyU3BlYyI6eyJpdiI6WzkxLDc1LC03MywtMzEsNCw4LC0yMyw3OSwtODUsLTg1LDIsMTI3LDEyMywtNDksNCw4NV19fQ==eyJlbmNyeXB0ZWREYXRhIjpbNTAsNzgsNTIsMjksMTEyLDEwLDIwLDk2LC03Niw4OCwtODYsLTEyMywtODEsLTc3LDkxLC0xMTIsMzcsLTcwLDEwMSwtNTMsOTEsLTEwLDEyMiwzLDk5LC00MSwyMSw5OSw1NywxMDcsLTEyMSwtNDEsLTMsOTksLTU5LDQxLDIxLC0yMywxNSw1MSwtNjgsNTksLTM3LDEwNSwtOSwtMTQsMTI0LDg0LC00OSwzNiwxMCwzOCwtNzMsMTI0LDQ1LC0xLC0yNiwzMCw0Myw4NCwxMiwtNDIsLTc2LC0zLDMsMTEwLDU2LC01OCwtMzMsLTQwLDIwLC03OCwtODgsNywxMDUsLTM1LC0zOCwtODIsLTUwLDQ1LDM0LDExLDExNCwtODYsLTEsLTExNiwtOTIsLTMsMTUsLTczLDU5LDU3LC03OSwtMTIsLTEwMyw3NSwtNjIsLTMzLC0xMDMsLTIsLTUyLDM2LC0xMDUsLTEwOCwtNDcsNzQsMywtNCw5MCwzLDExNiwtOTMsOTAsMTE1LC03MCw1NSwtNTgsNzgsNDYsNjcsMjksLTg1LC01MSwzNSwtMTI2LDc3LDk2LC0yMiwtMTUsNjUsMTUsMjgsNjIsLTU0LC00NiwtNDgsLTUwLDc3LC0zNywtNjYsLTEyMSwtMzgsLTQsMTE4LC03LDE5LC02MSwtMTIzLDIwLDYyLC04Myw0NSwyOSwtMTAsMTI0LC02NSw3NSwtMTI0LDQ0LC02MywtMjcsMjcsLTMxLDk5LDY3LDAsMTIxLC05NywtMjEsLTcxLDMzLDg1LC0xMTQsLTUxLDEyNyw1NCwtMTAyLDcwLC03NCw4LDc0LC0xMjYsNDIsLTIzLDU2LC05OCwtMTA4LDgxLC0xMjgsMTEyLDE5LC03Myw3NCwtODgsLTY1LDc4LDc2LC0xMjYsLTE2LDExOCwtMTEyLDIsLTUyLDY3LC01Myw3NCwxMTYsLTc3LDcyLDk5LC0xNiwtMTAwLC05OSwtMTksOTEsNDksNSwtNzEsLTgsLTYyLDEyNywtMTEsLTQ0LDEyNywtODksNTEsODIsNjEsLTgxLDk4LDU2LC00Miw5MSw2LDI4LC0xNSwyMSwxOSw0MCwxMDgsMTA5LC04LDEyNCwzOSwtNjUsLTU3LDkwLC0xMDEsMTA2LC0yMSwxMTEsLTExOSw2NSw2LC01NSw5MSwtMzUsMTYsLTExOCwtMTA1LDgzLDQ0LDgwXSwibWF0ZXJpYWxTZXRTZXJpYWxOdW1iZXIiOjEsIml2UGFyYW1ldGVyU3BlYyI6eyJpdiI6WzkxLDc1LC03MywtMzEsNCw4LC0yMyw3OSwtODUsLTg1LDIsMTI3LDEyMywtNDksNCw4NV19fQ==eyJlbmNyeXB0ZWREYXRhIjpbNTAsNzgsNTIsMjksMTEyLDEwLDIwLDk2LC03Niw4OCwtODYsLTEyMywtODEsLTc3LDkxLC0xMTIsMzcsLTcwLDEwMSwtNTMsOTEsLTEwLDEyMiwzLDk5LC00MSwyMSw5OSw1NywxMDcsLTEyMSwtNDEsLTMsOTksLTU5LDQxLDIxLC0yMywxNSw1MSwtNjgsNTksLTM3LDEwNSwtOSwtMTQsMTI0LDg0LC00OSwzNiwxMCwzOCwtNzMsMTI0LDQ1LC0xLC0yNiwzMCw0Myw4NCwxMiwtNDIsLTc2LC0zLDMsMTEwLDU2LC01OCwtMzMsLTQwLDIwLC03OCwtODgsNywxMDUsLTM1LC0zOCwtODIsLTUwLDQ1LDM0LDExLDExNCwtODYsLTEsLTExNiwtOTIsLTMsMTUsLTczLDU5LDU3LC03OSwtMTIsLTEwMyw3NSwtNjIsLTMzLC0xMDMsLTIsLTUyLDM2LC0xMDUsLTEwOCwtNDcsNzQsMywtNCw5MCwzLDExNiwtOTMsOTAsMTE1LC03MCw1NSwtNTgsNzgsNDYsNjcsMjksLTg1LC01MSwzNSwtMTI2LDc3LDk2LC0yMiwtMTUsNjUsMTUsMjgsNjIsLTU0LC00NiwtNDgsLTUwLDc3LC0zNywtNjYsLTEyMSwtMzgsLTQsMTE4LC03LDE5LC02MSwtMTIzLDIwLDYyLC04Myw0NSwyOSwtMTAsMTI0LC02NSw3NSwtMTI0LDQ0LC02MywtMjcsMjcsLTMxLDk5LDY3LDAsMTIxLC05NywtMjEsLTcxLDMzLDg1LC0xMTQsLTUxLDEyNyw1NCwtMTAyLDcwLC03NCw4LDc0LC0xMjYsNDIsLTIzLDU2LC05OCwtMTA4LDgxLC0xMjgsMTEyLDE5LC03Myw3NCwtODgsLTY1LDc4LDc2LC0xMjYsLTE2LDExOCwtMTEyLDIsLTUyLDY3LC01Myw3NCwxMTYsLTc3LDcyLDk5LC0xNiwtMTAwLC05OSwtMTksOTEsNDksNSwtNzEsLTgsLTYyLDEyNywtMTEsLTQ0LDEyNywtODksNTEsODIsNjEsLTgxLDk4LDU2LC00Miw5MSw2LDI4LC0xNSwyMSwxOSw0MCwxMDgsMTA5LC04LDEyNCwzOSwtNjUsLTU3LDkwLC0xMDEsMTA2LC0yMSwxMTEsLTExOSw2NSw2LC01NSw5MSwtMzUsMTYsLTExOCwtMTA1LDgzLDQ0LDgwXSwibWF0ZXJpYWxTZXRTZXJpYWxOdW1iZXIiOjEsIml2UGFyYW1ldGVyU3BlYyI6eyJpdiI6WzkxLDc1LC03MywtMzEsNCw4LC0yMyw3OSwtODUsLTg1LDIsMTI3LDEyMywtNDksNCw4NV19fQ==",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-zgvfqq",
    "configRuleName": "gaurav-test",
    "configRuleId": "config-rule-zgvfqq",
    "accountId": "107339370656"
}

CONTEXT = ""

RESOURCE_ID = ""
RESOURCE_TYPE = AWSResourceClassConstants.SG_RESOURCE
CONFIGITEMS = {"region": "us-east-1"}


class TestDeleteUnusedSecurityGroupAction(object):
    """ Class for testing delete unused security groups """

    __regions = ['us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __mockInstanceResponse = {'ResponseMetadata': {'HTTPStatusCode': 200, 'RetryAttempts': 0}}
    __mockInstanceResponse_fail = {'ResponseMetadata': {'HTTPStatusCode': 500, 'RetryAttempts': 0}}
    __errorResponse = {'Error': {
        'Code': 400,
        'Message': 'AccessDenied'
    }}

    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __deleteUnusedSGAction = sgAction.DeleteUnusedSGAction(__eventParam)

    @mock_ec2
    def test_SGDeleteSuccess(self):
        """ Method for testing success """
        ec2 = boto3.resource('ec2', 'us-east-1')
        vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
        sg = ec2.create_security_group(GroupName='sg1', Description='Test security group sg1', VpcId=vpc.id)
        ip_permissions = [
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{"CidrIp": "0.0.0.0/0"}]
            },
        ]
        sg.authorize_ingress(IpPermissions=ip_permissions)
        ec2 = boto3.client('ec2', 'us-east-1')
        response = ec2.describe_security_groups(GroupIds=[sg.id])
        CONFIGITEMS['region'] = 'us-east-1'
        RESOURCE_ID = response['SecurityGroups'][0]['GroupId']

        sgAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIGITEMS)
        ec2.delete_security_group = MagicMock(return_value=self.__mockInstanceResponse)
        evaluationResult = self.__deleteUnusedSGAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

    @mock_ec2
    def test_SGDeleteFailure(self):
        """ Method for testing failure """
        ec2 = boto3.resource('ec2', 'us-east-1')
        vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
        sg = ec2.create_security_group(GroupName='sg1', Description='Test security group sg1', VpcId=vpc.id)
        ip_permissions = [
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{"CidrIp": "0.0.0.0/0"}]
            },
        ]
        sg.authorize_ingress(IpPermissions=ip_permissions)
        ec2 = boto3.client('ec2', 'us-east-1')
        response = ec2.describe_security_groups(GroupIds=[sg.id])
        CONFIGITEMS['region'] = 'us-east-1'
        RESOURCE_ID = response['SecurityGroups'][0]['GroupId']

        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__regions[0])
        sgAction.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIGITEMS)
        ec2Client.delete_security_group = MagicMock(return_value=self.__mockInstanceResponse_fail)
        evaluationResult = self.__deleteUnusedSGAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_ec2
    def test_SGDeleteException_keyError(self):
        """ Method for testing with key error """
        ec2 = boto3.resource('ec2', 'us-east-1')
        vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
        sg = ec2.create_security_group(GroupName='sg1', Description='Test security group sg1', VpcId=vpc.id)
        ip_permissions = [
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{"CidrIp": "0.0.0.0/0"}]
            },
        ]
        sg.authorize_ingress(IpPermissions=ip_permissions)
        ec2 = boto3.client('ec2', 'us-east-1')
        response = ec2.describe_security_groups(GroupIds=[sg.id])
        CONFIGITEMS['region'] = 'us-east-1'
        RESOURCE_ID = response['SecurityGroups'][0]['GroupId']

        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__regions[0])
        sgAction.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIGITEMS)
        ec2Client.delete_security_group = MagicMock(side_effect=KeyError("Mock Exception: Key not found error"))
        evaluationResult = self.__deleteUnusedSGAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_ec2
    def test_SGDeleteException_valueError(self):
        """ Method for testing with value error """
        ec2 = boto3.resource('ec2', 'us-east-1')
        vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
        sg = ec2.create_security_group(GroupName='sg1', Description='Test security group sg1', VpcId=vpc.id)
        ip_permissions = [
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{"CidrIp": "0.0.0.0/0"}]
            },
        ]
        sg.authorize_ingress(IpPermissions=ip_permissions)
        ec2 = boto3.client('ec2', 'us-east-1')
        response = ec2.describe_security_groups(GroupIds=[sg.id])
        CONFIGITEMS['region'] = 'us-east-1'
        RESOURCE_ID = response['SecurityGroups'][0]['GroupId']

        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__regions[0])
        sgAction.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIGITEMS)
        ec2Client.delete_security_group = MagicMock(side_effect=ValueError("Mock Exception: Value not found error"))
        evaluationResult = self.__deleteUnusedSGAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_ec2
    def test_SGDeleteException_exceptionError(self):
        """ Method for testing with exeception """
        ec2 = boto3.resource('ec2', 'us-east-1')
        vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
        sg = ec2.create_security_group(GroupName='sg1', Description='Test security group sg1', VpcId=vpc.id)
        ip_permissions = [
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{"CidrIp": "0.0.0.0/0"}]
            },
        ]
        sg.authorize_ingress(IpPermissions=ip_permissions)
        ec2 = boto3.client('ec2', 'us-east-1')
        response = ec2.describe_security_groups(GroupIds=[sg.id])
        CONFIGITEMS['region'] = 'us-east-1'
        RESOURCE_ID = response['SecurityGroups'][0]['GroupId']

        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__regions[0])
        sgAction.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIGITEMS)
        ec2Client.delete_security_group = MagicMock(side_effect=Exception("Mock Exception: Incorrect syntax"))
        evaluationResult = self.__deleteUnusedSGAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_ec2
    def test_SGDeleteException_attributeError(self):
        """ Method for testing with attribute error """
        ec2 = boto3.resource('ec2', 'us-east-1')
        vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
        sg = ec2.create_security_group(GroupName='sg1', Description='Test security group sg1', VpcId=vpc.id)
        ip_permissions = [
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{"CidrIp": "0.0.0.0/0"}]
            },
        ]
        sg.authorize_ingress(IpPermissions=ip_permissions)
        ec2 = boto3.client('ec2', 'us-east-1')
        response = ec2.describe_security_groups(GroupIds=[sg.id])
        CONFIGITEMS['region'] = 'us-east-1'
        RESOURCE_ID = response['SecurityGroups'][0]['GroupId']

        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__regions[0])
        sgAction.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIGITEMS)
        ec2Client.delete_security_group = MagicMock(side_effect=AttributeError("Mock Exception: Attribute not found error"))
        evaluationResult = self.__deleteUnusedSGAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_ec2
    def test_SGDeleteException_clientError(self):
        """ Method for testing with client error """
        ec2 = boto3.resource('ec2', 'us-east-1')
        vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
        sg = ec2.create_security_group(GroupName='sg1', Description='Test security group sg1', VpcId=vpc.id)
        ip_permissions = [
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{"CidrIp": "0.0.0.0/0"}]
            },
        ]
        sg.authorize_ingress(IpPermissions=ip_permissions)
        ec2 = boto3.client('ec2', 'us-east-1')
        response = ec2.describe_security_groups(GroupIds=[sg.id])
        CONFIGITEMS['region'] = 'us-east-1'
        RESOURCE_ID = response['SecurityGroups'][0]['GroupId']

        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__regions[0])
        sgAction.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIGITEMS)
        ec2Client.delete_security_group = MagicMock(side_effect=ClientError(self.__errorResponse, "AssumeRole"))
        evaluationResult = self.__deleteUnusedSGAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION
