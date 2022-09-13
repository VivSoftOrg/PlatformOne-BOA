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
from moto import mock_ec2
from common.common_constants import *
import common.compliance_object_factory as complianceobjectfactory
import ec2_noshutdown_tag.ec2_noshutdown_tag_resource_fetcher as tagFetcher
import time
from botocore.exceptions import ClientError
from datetime import datetime
from dateutil.tz import tzutc



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

class TestEc2NoshutdownTagFetcher(object):
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __regions = [ 'us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __ec2NoshutdownTagFetcher=tagFetcher.Ec2NoshutdownTagFetcher(__eventParam)
    __mockResponse = {'Reservations': [{'Groups': [], 'Instances': [{'Tags': [{'Value': 'Testing', 'Key': 'Environment'}, {'Value': 'test-ec2', 'Key': 'Name'}, {'Value': '2018-01-09', 'Key': 'ExpirationDate'}, {'Value': 'vaibhav.fulsundar', 'Key': 'Owner'}, {'Value': 'MNC', 'Key': 'Project'}], 'PrivateIpAddress': '172.30.2.64', 'RootDeviceType': 'ebs', 'ImageId': 'ami-5583d42f', 'Placement': {'AvailabilityZone': 'us-east-1c', 'Tenancy': 'default', 'GroupName': ''}, 'State': {'Code': 16, 'Name': 'running'}, 'Architecture': 'x86_64', 'InstanceId': 'i-0d1a6a41f136b426f', 'PublicDnsName': 'ec2-54-175-75-87.compute-1.amazonaws.com', 'StateTransitionReason': '', 'EnaSupport': True, 'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-afbb8ada'}], 'SubnetId': 'subnet-062f514d', 'RootDeviceName': '/dev/xvda', 'NetworkInterfaces': [{'Ipv6Addresses': [], 'Association': {'PublicDnsName': 'ec2-54-175-75-87.compute-1.amazonaws.com', 'PublicIp': '54.175.75.87', 'IpOwnerId': 'amazon'}, 'Groups': [{'GroupName': 'default', 'GroupId': 'sg-afbb8ada'}], 'PrivateIpAddress': '172.30.2.64', 'PrivateIpAddresses': [{'Association': {'PublicDnsName': 'ec2-54-175-75-87.compute-1.amazonaws.com', 'PublicIp': '54.175.75.87', 'IpOwnerId': 'amazon'}, 'Primary': True, 'PrivateIpAddress': '172.30.2.64', 'PrivateDnsName': 'ip-172-30-2-64.ec2.internal'}], 'SubnetId': 'subnet-062f514d', 'MacAddress': '0a:46:a7:82:35:7e', 'Description': 'Primary network interface', 'NetworkInterfaceId': 'eni-6d4c6195', 'SourceDestCheck': True, 'Attachment': {'Status': 'attached', 'AttachmentId': 'eni-attach-f82662c9', 'DeviceIndex': 0, 'AttachTime': datetime(2018, 1, 8, 10, 36, 53, tzinfo=tzutc()), 'DeleteOnTermination': True}, 'OwnerId': '107339370656', 'VpcId': 'vpc-a04c01d8', 'PrivateDnsName': 'ip-172-30-2-64.ec2.internal', 'Status': 'in-use'}], 'AmiLaunchIndex': 0, 'Hypervisor': 'xen', 'VirtualizationType': 'hvm', 'ClientToken': '', 'Monitoring': {'State': 'disabled'}, 'SourceDestCheck': True, 'InstanceType': 't2.micro', 'PublicIpAddress': '54.175.75.87', 'BlockDeviceMappings': [{'Ebs': {'VolumeId': 'vol-0ae68997c29190f9f', 'DeleteOnTermination': True, 'Status': 'attached', 'AttachTime': datetime(2018, 1, 8, 10, 36, 54, tzinfo=tzutc())}, 'DeviceName': '/dev/xvda'}], 'VpcId': 'vpc-a04c01d8', 'LaunchTime': datetime(2018, 1, 8, 10, 36, 53, tzinfo=tzutc()), 'EbsOptimized': False, 'PrivateDnsName': 'ip-172-30-2-64.ec2.internal', 'ProductCodes': [], 'KeyName': 'ec2_keypair'}], 'OwnerId': '107339370656', 'ReservationId': 'r-0cb684a39c78862ec'}], 'ResponseMetadata': {'HTTPHeaders': {'transfer-encoding': 'chunked', 'vary': 'Accept-Encoding', 'date': 'Mon, 08 Jan 2018 12:16:01 GMT', 'server': 'AmazonEC2', 'content-type': 'text/xml;charset=UTF-8'}, 'HTTPStatusCode': 200, 'RequestId': 'ade55855-f1d2-40d2-b764-cfc16a131d34', 'RetryAttempts': 0}} 

    __blankMockResponse = {}
    __errorResponse = {'Error':{
        'Code':400,
        'Message':'AccessDenied'
    }}

    @mock_ec2
    def test_resource_fetcher_no_data(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2,self.__regions[0])
        tagFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_instances = MagicMock(return_value = self.__blankMockResponse)
        return_value = self.__ec2NoshutdownTagFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_ec2
    def test_resource_fetcher_failure_client_error(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        tagFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_instances = MagicMock(side_effect=ClientError(self.__errorResponse,"AssumeRole"))
        return_value = self.__ec2NoshutdownTagFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_ec2
    def test_resource_fetcher_with_data(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2,self.__regions[0])
        tagFetcher.BotoUtility.getClient = MagicMock(return_value = ec2Client)
        ec2Client.describe_instances = MagicMock(return_value = self.__mockResponse)
        return_value = self.__ec2NoshutdownTagFetcher.resourceFetcher()
        assert bool(return_value) == True

    @mock_ec2
    def test_resource_fetcher_failure_key_error(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        tagFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_instances = MagicMock(side_effect=KeyError("Mock Exception : Key not found!"))
        return_value = self.__ec2NoshutdownTagFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_ec2
    def test_resource_fetcher_failure_value_error(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        tagFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_instances = MagicMock(side_effect=ValueError("Mock Exception : Value not found!"))
        return_value = self.__ec2NoshutdownTagFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_ec2
    def test_resource_fetcher_failure_syntax_error(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        tagFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_instances = MagicMock(side_effect=SyntaxError("Mock Exception : Syntax error!"))
        return_value = self.__ec2NoshutdownTagFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_ec2
    def test_resource_fetcher_failure_attribute_error(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        tagFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_instances = MagicMock(side_effect=AttributeError("Mock Exception : Attribute not found error"))
        return_value = self.__ec2NoshutdownTagFetcher.resourceFetcher()
        assert bool(return_value) == False