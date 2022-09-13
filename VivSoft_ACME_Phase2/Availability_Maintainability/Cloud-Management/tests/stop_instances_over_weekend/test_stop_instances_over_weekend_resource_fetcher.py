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
import datetime
from dateutil.tz import tzutc
import pytest
import boto3
import sys
import unittest
import os

sys.path.append('../../')

import stop_instances_over_weekend.stop_instances_over_weekend_resource_fetcher as siowFetcher
from common.common_constants import *
from mock import MagicMock
from moto import mock_ec2
import common.compliance_object_factory as complianceobjectfactory
from common.boto_utility import BotoUtility

EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-08-21T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
    "ruleParameters": "{\"performAction\": \"True\",\"notifier\": \"sns\",\"toEmail\": \"akshay.deshpande@reancloud.com\"}",
    "resultToken": "",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-zgvfqq",
    "configRuleName": "gaurav-test",
    "configRuleId": "config-rule-zgvfqq",
    "accountId": "107339370656"
}
CONTEXT = ""


class TestStopInstancesOverWeekend(object):
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __regions = ['us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __StopInstancesOverWeekendFetcher = siowFetcher.StopInstancesOverWeekendResourceFetcher(__eventParam)
    __mockResponse = {
        "Reservations": [
            {
                "OwnerId": "107339370656",
                "Groups": [],
                "Instances": [
                    {
                        "RootDeviceType": "ebs",
                        "InstanceType": "t2.micro",
                        "InstanceId": "i-0537551fea1ff5111",
                        "VpcId": "vpc-a04c01d8",
                        "KeyName": "MyKeyPair",
                        "ProductCodes": [],
                        "EbsOptimized": False,
                        "PrivateIpAddress": "172.30.2.46",
                        "SecurityGroups": [
                            {
                                "GroupName": "default",
                                "GroupId": "sg-afbb8ada"
                            }
                        ],
                        "NetworkInterfaces": [
                            {
                                "Attachment": {
                                    "Status": "attached",
                                    "AttachTime": "2018-01-08T12:12:38.000Z",
                                    "AttachmentId": "eni-attach-62f5b153",
                                    "DeleteOnTermination": True,
                                    "DeviceIndex": 0
                                },
                                "VpcId": "vpc-a04c01d8",
                                "Description": "Primary network interface",
                                "PrivateIpAddress": "172.30.2.46",
                                "OwnerId": "107339370656",
                                "NetworkInterfaceId": "eni-514a66a9",
                                "SubnetId": "subnet-062f514d",
                                "MacAddress": "0a:6d:60:9d:c7:14",
                                "Status": "in-use",
                                "PrivateIpAddresses": [
                                    {
                                        "PrivateIpAddress": "172.30.2.46",
                                        "PrivateDnsName": "ip-172-30-2-46.ec2.internal",
                                        "Primary": True,
                                        "Association": {
                                            "IpOwnerId": "amazon",
                                            "PublicIp": "52.73.101.42",
                                            "PublicDnsName": "ec2-52-73-101-42.compute-1.amazonaws.com"
                                        }
                                    }
                                ],
                                "Groups": [
                                    {
                                        "GroupName": "default",
                                        "GroupId": "sg-afbb8ada"
                                    }
                                ],
                                "Ipv6Addresses": [],
                                "Association": {
                                    "IpOwnerId": "amazon",
                                    "PublicIp": "52.73.101.42",
                                    "PublicDnsName": "ec2-52-73-101-42.compute-1.amazonaws.com"
                                },
                                "SourceDestCheck": True,
                                "PrivateDnsName": "ip-172-30-2-46.ec2.internal"
                            }
                        ],
                        "PublicIpAddress": "52.73.101.42",
                        "VirtualizationType": "hvm",
                        "Monitoring": {
                            "State": "disabled"
                        },
                        "SourceDestCheck": True,
                        "Hypervisor": "xen",
                        "BlockDeviceMappings": [
                            {
                                "Ebs": {
                                    "AttachTime": "2018-01-08T12:12:38.000Z",
                                    "Status": "attached",
                                    "DeleteOnTermination": True,
                                    "VolumeId": "vol-0bfc9dcf860fa0aa4"
                                },
                                "DeviceName": "/dev/sda1"
                            }
                        ],
                        "LaunchTime": "2018-01-08T12:12:38.000Z",
                        "EnaSupport": True,
                        "PublicDnsName": "ec2-52-73-101-42.compute-1.amazonaws.com",
                        "Placement": {
                            "GroupName": "",
                            "AvailabilityZone": "us-east-1c",
                            "Tenancy": "default"
                        },
                        "SubnetId": "subnet-062f514d",
                        "StateTransitionReason": "",
                        "ImageId": "ami-aa2ea6d0",
                        "Architecture": "x86_64",
                        "ClientToken": "",
                        "State": {
                            "Name": "running",
                            "Code": 16
                        },
                        "RootDeviceName": "/dev/sda1",
                        "Tags": [
                            {
                                "Value": "akshay_test",
                                "Key": "Name"
                            }
                        ],
                        "AmiLaunchIndex": 0,
                        "PrivateDnsName": "ip-172-30-2-46.ec2.internal"
                    }
                ],
                "ReservationId": "r-00752379c4123feec"
            }
        ]
    }

    __blankMockResponse = {
        'Reservations': [{
            'Groups': [],
            'Instances': [{}],
            'ResponseMetadata': {
                'HTTPHeaders': {
                    'transfer-encoding': 'chunked',
                    'vary': 'Accept-Encoding',
                    'date': 'Mon, 08 Jan 2018 12:16:01 GMT',
                    'server': 'AmazonEC2',
                    'content-type': 'text/xml;charset=UTF-8'
                },
                'HTTPStatusCode': 200,
                'RequestId': 'ade55855-f1d2-40d2-b764-cfc16a131d34',
                'RetryAttempts': 0
            }
        }]
    }

    @mock_ec2
    def test_resource_fetcher_no_data(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        siowFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_instances = MagicMock(return_value=self.__blankMockResponse)
        return_value = self.__StopInstancesOverWeekendFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_ec2
    def test_ResourceFetcherFailure(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        siowFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_instances = MagicMock(side_effect=Exception("Failed to fetch resource details"))
        return_value = self.__StopInstancesOverWeekendFetcher.resourceFetcher()
        assert bool(return_value) == False

    @mock_ec2
    def test_ResourceFetcherWithData(self):
        self._AbstractResourceFetcher__eventParam = self.__eventParam
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        siowFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_instances = MagicMock(return_value=self.__mockResponse)
        return_value = self.__StopInstancesOverWeekendFetcher.resourceFetcher()
        assert bool(return_value) == True
