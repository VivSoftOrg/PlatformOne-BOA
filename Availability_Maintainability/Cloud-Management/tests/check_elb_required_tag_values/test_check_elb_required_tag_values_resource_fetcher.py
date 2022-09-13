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
from moto import mock_elb
from common.common_constants import *
import common.compliance_object_factory as complianceobjectfactory
import check_elb_required_tag_values.check_elb_required_tag_values_resource_fetcher as elbFetcher
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

class TestELBRequiredTagValuesFetcher(object):
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __regions = [ 'us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __checkELBRequiredTagValuesResourceFetcher = elbFetcher.CheckELBRequiredTagValuesResourceFetcher(__eventParam)
    __mockResponse1 = {'LoadBalancerDescriptions': [{'Scheme': 'internet-facing', 'DNSName': 'testELB-180466032.us-east-1.elb.amazonaws.com', 'Policies': {'AppCookieStickinessPolicies': [], 'OtherPolicies': [], 'LBCookieStickinessPolicies': []}, 'CanonicalHostedZoneName': 'testELB-180466032.us-east-1.elb.amazonaws.com', 'HealthCheck': {'HealthyThreshold': 10, 'Target': 'HTTP:80/index.html', 'UnhealthyThreshold': 2, 'Interval': 30, 'Timeout': 5}, 'AvailabilityZones': ['us-east-1d', 'us-east-1e'], 'SecurityGroups': ['sg-5d787f29'], 'SourceSecurityGroup': {'GroupName': 'default', 'OwnerAlias': '693265998683'}, 'LoadBalancerName': 'testELB', 'ListenerDescriptions': [{'Listener': {'Protocol': 'HTTP', 'InstanceProtocol': 'HTTP', 'LoadBalancerPort': 80, 'InstancePort': 80}, 'PolicyNames': []}], 'Subnets': ['subnet-975c06f3', 'subnet-eb5a2bd4'], 'BackendServerDescriptions': [], 'CreatedTime': datetime(2018, 1, 31, 7, 44, 40, 580000, tzinfo=tzutc()), 'CanonicalHostedZoneNameID': 'Z35SXDOTRQ7X7K', 'Instances': [{'InstanceId': 'i-0b7fd9aea339f5000'}, {'InstanceId': 'i-0e94f2e85891fb45a'}], 'VPCId': 'vpc-59848c21'}], 'ResponseMetadata': {'HTTPStatusCode': 200, 'HTTPHeaders': {'vary': 'Accept-Encoding', 'content-length': '2387', 'x-amzn-requestid': 'a1906c16-065a-11e8-b007-612dac916e52', 'content-type': 'text/xml', 'date': 'Wed, 31 Jan 2018 07:44:55 GMT'}, 'RequestId': 'a1906c16-065a-11e8-b007-612dac916e52', 'RetryAttempts': 0}}
    __blankMockResponse = {'ResponseMetadata': {'HTTPStatusCode': 200, 'HTTPHeaders': {'content-length': '335', 'x-amzn-requestid': '52f7cc0c-0658-11e8-893e-195edff91d28', 'content-type': 'text/xml', 'date': 'Wed, 31 Jan 2018 07:28:24 GMT'}, 'RequestId': '52f7cc0c-0658-11e8-893e-195edff91d28', 'RetryAttempts': 0}}
    __mockResponse2 = {'LoadBalancers': [{'LoadBalancerName': 'testNElb', 'AvailabilityZones': [{'LoadBalancerAddresses': [{}], 'SubnetId': 'subnet-0f611d6b', 'ZoneName': 'us-east-1d'}, {'LoadBalancerAddresses': [{}], 'SubnetId': 'subnet-36c7b77d', 'ZoneName': 'us-east-1b'}], 'LoadBalancerArn': 'arn:aws:elasticloadbalancing:us-east-1:693265998683:loadbalancer/net/testNElb/d1de7fb288f0ab99', 'State': {'Code': 'active'}, 'DNSName': 'testNElb-d1de7fb288f0ab99.elb.us-east-1.amazonaws.com', 'Scheme': 'internet-facing', 'CanonicalHostedZoneId': 'Z26RNL4JYFTOTI', 'VpcId': 'vpc-a25216da', 'IpAddressType': 'ipv4', 'CreatedTime': datetime(2018, 2, 2, 17, 15, 55, 329000, tzinfo=tzutc()), 'Type': 'network'}, {'LoadBalancerName': 'testApp', 'AvailabilityZones': [{'SubnetId': 'subnet-0f611d6b', 'ZoneName': 'us-east-1d'}, {'SubnetId': 'subnet-3005900f', 'ZoneName': 'us-east-1e'}, {'SubnetId': 'subnet-87bc15da', 'ZoneName': 'us-east-1c'}], 'DNSName': 'testApp-1562456216.us-east-1.elb.amazonaws.com', 'Scheme': 'internet-facing', 'CanonicalHostedZoneId': 'Z35SXDOTRQ7X7K', 'State': {'Code': 'active'}, 'IpAddressType': 'ipv4', 'CreatedTime': datetime(2018, 2, 2, 17, 15, 14, 630000, tzinfo=tzutc()), 'LoadBalancerArn': 'arn:aws:elasticloadbalancing:us-east-1:693265998683:loadbalancer/app/testApp/0dd0188b39ece326', 'Type': 'application', 'VpcId': 'vpc-a25216da', 'SecurityGroups': ['sg-f8d4f18d']}]}
    __errorResponse = {'Error':{
        'Code':400,
        'Message':'AccessDenied'
    }}

    @mock_elb
    def test_resource_fetcher_no_data(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB,self.__regions[0])
        elbClientv2 = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB_V2,self.__regions[0])
        elbFetcher.BotoUtility.getClient = MagicMock(return_value = elbClient)
        elbClient.describe_load_balancers = MagicMock(return_value = self.__blankMockResponse)
        return_value = self.__checkELBRequiredTagValuesResourceFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_elb
    def test_resource_fetcher_failure(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB,self.__regions[0])
        elbClientv2 = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB_V2,self.__regions[0])
        elbFetcher.BotoUtility.getClient = MagicMock(return_value = elbClient)
        elbClient.describe_load_balancers = MagicMock(side_effect=ClientError(self.__errorResponse, "AssumeRole"))
        return_value = self.__checkELBRequiredTagValuesResourceFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_elb
    def test_resource_fetcher_with_data(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB,self.__regions[0])
        elbClientv2 = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB_V2,self.__regions[0])
        elbFetcher.BotoUtility.getClient = MagicMock(return_value=elbClient)
        elbClient.describe_load_balancers = MagicMock(return_value=self.__mockResponse2)
        return_value = self.__checkELBRequiredTagValuesResourceFetcher.resourceFetcher()
        assert bool(return_value) == True
