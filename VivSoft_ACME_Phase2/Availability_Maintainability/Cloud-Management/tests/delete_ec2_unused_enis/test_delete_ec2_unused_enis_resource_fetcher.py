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
import sys
import boto3
sys.path.append('../../')

import delete_ec2_unused_enis.delete_ec2_unused_enis_resource_fetcher as eniFetcher
import common.compliance_object_factory as complianceobjectfactory
from common.abstract_evaluate import *
from common.common_constants import *
from mock import MagicMock
from moto import mock_ec2


EVENT_JSON = {
      "configRuleId": "config-rule-1v52mx",
      "version": "1.0",
      "configRuleName": "aws-sample-rule",
      "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-1v52mx",
      "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
      "resultToken": "",
      "ruleParameters": "{\"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
      "eventLeftScope": "False",
      "executionRoleArn": "arn:aws:iam::107339370656:role/awsconfig-role",
      "accountId": "107339370656"
}


CONTEXT = ""


class TestUnusedNetworkInterfacesFetcher(object):

    __mockResponse = {'NetworkInterfaces': [{'Status': 'available', 'Groups': [{'GroupId': 'sg-c9e9e2ad', 'GroupName': 'SG for instance i-i-54329-ce872d'}], 'PrivateDnsName': 'ip-172-31-5-132.ec2.internal', 'InterfaceType': 'interface', 'TagSet': [], 'AvailabilityZone': 'us-east-1e', 'NetworkInterfaceId': 'eni-c4a66ff9', 'VpcId': 'vpc-43300b26', 'RequesterId': 'AIDAJ6RMFP4XZMTNPZRNE', 'MacAddress': '06:9d:08:0c:60:63', 'RequesterManaged': False, 'OwnerId': '107339370656', 'PrivateIpAddresses': [{'Primary': True, 'PrivateDnsName': 'ip-172-31-5-132.ec2.internal', 'PrivateIpAddress': '172.31.5.132'}], 'SourceDestCheck': True, 'PrivateIpAddress': '172.31.5.132', 'Description': 'New ENI', 'SubnetId': 'subnet-1a8b8f20', 'Ipv6Addresses': []}, {'Status': 'available', 'Groups': [{'GroupId': 'sg-c9e9e2ad', 'GroupName': 'SG for instance i-i-54329-ce872d'}], 'PrivateDnsName': 'ip-172-31-2-41.ec2.internal', 'InterfaceType': 'interface', 'TagSet': [], 'AvailabilityZone': 'us-east-1e', 'NetworkInterfaceId': 'eni-eda66fd0', 'VpcId': 'vpc-43300b26', 'RequesterId': 'AIDAJ6RMFP4XZMTNPZRNE', 'MacAddress': '06:48:8e:2f:2c:4d', 'RequesterManaged': False, 'OwnerId': '107339370656', 'PrivateIpAddresses': [{'Primary': True, 'PrivateDnsName': 'ip-172-31-2-41.ec2.internal', 'PrivateIpAddress': '172.31.2.41'}], 'SourceDestCheck': True, 'PrivateIpAddress': '172.31.2.41', 'Description': '', 'SubnetId': 'subnet-1a8b8f20', 'Ipv6Addresses': []}], 'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': 'ab495071-4ac8-4716-ac34-f7e545ec7078', 'HTTPHeaders': {'transfer-encoding': 'chunked', 'server': 'AmazonEC2', 'vary': 'Accept-Encoding', 'content-type': 'text/xml;charset=UTF-8', 'date': 'Fri, 29 Sep 2017 07:45:37 GMT'}, 'RetryAttempts': 0}}
    __regions = ['ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __deleteEC2UnusedENIsResourceFetcher = eniFetcher.DeleteEC2UnusedENIsResourceFetcher(__eventParam)

    @mock_ec2
    def testResourceFetcher(self):
        eniFetcher.regions = MagicMock(return_value = self.__regions)
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        eniFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_network_interfaces = MagicMock(return_value=self.__mockResponse)
        return_value = self.__deleteEC2UnusedENIsResourceFetcher.resourceFetcher()
        assert bool(return_value) == True

    @mock_ec2
    def testResourceFetcherNoData(self):
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        eniFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        return_value = self.__deleteEC2UnusedENIsResourceFetcher.resourceFetcher()
        assert bool(return_value) == False
