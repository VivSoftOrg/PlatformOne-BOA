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
from botocore.exceptions import ClientError
from common.common_constants import *
import common.compliance_object_factory as complianceobjectfactory
import exposed_security_groups.exposed_security_groups_resource_fetcher as sgFetcher


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

class TestExposedSecurityGroupsResourceFetcher(object):
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __regions = [ 'us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __deleteUnusedSGFetcher=sgFetcher.ExposedSecurityGroupsResourceFetcher(__eventParam)
    __mockResponse = {'ResponseMetadata': {'RetryAttempts': 0, 'RequestId': '97333dd3-fd5c-458c-940c-d3f05e893e88', 'HTTPHeaders': {'vary': 'Accept-Encoding', 'date': 'Fri, 22 Dec 2017 05:45:49 GMT', 'transfer-encoding': 'chunked', 'server': 'AmazonEC2', 'content-type': 'text/xml;charset=UTF-8'}, 'HTTPStatusCode': 200}, 'securitygroups': [{'Description': 'test security groups', 'IpPermissionsEgress': [{'IpRanges': [{'CidrIp': '0.0.0.0/0'}], 'PrefixListIds': [], 'Ipv6Ranges': [], 'UserIdGroupPairs': [], 'IpProtocol': '-1'}], 'groupid': 'sg-b53f1cc0', 'VpcId': 'vpc-ba5f19c2', 'IpPermissions': [{'UserIdGroupPairs': [], 'ToPort': 80, 'IpRanges': [{'CidrIp': '202.149.218.202/32'}], 'IpProtocol': 'tcp', 'Ipv6Ranges': [], 'FromPort': 80, 'PrefixListIds': []}, {'UserIdGroupPairs': [], 'ToPort': 22, 'IpRanges': [{'CidrIp': '202.149.218.202/32'}], 'IpProtocol': 'tcp', 'Ipv6Ranges': [], 'FromPort': 22, 'PrefixListIds': []}, {'UserIdGroupPairs': [], 'ToPort': 443, 'IpRanges': [{'CidrIp': '202.149.218.202/32'}], 'IpProtocol': 'tcp', 'Ipv6Ranges': [], 'FromPort': 443, 'PrefixListIds': []}], 'GroupName': 'V-SG-1', 'OwnerId': '107339370656'}]}
    __blankMockResponse = {}
    __errorResponse = {'Error':{
        'Code':400,
        'Message':'AccessDenied'
    }}
    @mock_ec2
    def test_ResourceFetcherNoData(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2,self.__regions[0])
        sgFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_security_groups = MagicMock(return_value = self.__blankMockResponse)
        return_value = self.__deleteUnusedSGFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_ec2
    def test_ResourceFetcherFailure(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        sgFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_security_groups = MagicMock(side_effect=KeyError("Key not found error!"))
        return_value = self.__deleteUnusedSGFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_ec2
    def test_ResourceFetcherWithData(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2,self.__regions[0])
        sgFetcher.BotoUtility.getClient = MagicMock(return_value = ec2Client)
        ec2Client.describe_security_groups = MagicMock(return_value = self.__mockResponse)
        return_value = self.__deleteUnusedSGFetcher.resourceFetcher()
        assert bool(return_value) == True

    @mock_ec2
    def test_ResourceFetcherFailure_attributeError(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        sgFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_security_groups = MagicMock(side_effect=AttributeError("Attribute not found error!"))
        return_value = self.__deleteUnusedSGFetcher.resourceFetcher()
        assert bool(return_value) == False
    
    @mock_ec2
    def test_ResourceFetcherFailure_valueError(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        sgFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_security_groups = MagicMock(side_effect=ValueError("Value not found error!"))
        return_value = self.__deleteUnusedSGFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_ec2
    def test_ResourceFetcherFailure_syntaxError(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        sgFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_security_groups = MagicMock(side_effect=SyntaxError("Value not found error!"))
        return_value = self.__deleteUnusedSGFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_ec2
    def test_ResourceFetcherFailure_clientError(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        sgFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_security_groups = MagicMock(side_effect=ClientError(self.__errorResponse,"AssumeRole"))
        return_value = self.__deleteUnusedSGFetcher.resourceFetcher()
        assert bool(return_value) == False
