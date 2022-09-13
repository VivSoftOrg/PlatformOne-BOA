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
import delete_unused_elb.delete_unused_elb_evaluate as elbEvaluate
import common.compliance_object_factory as complianceobjectfactory
from common.abstract_evaluate import *
from common.common_constants import *
from mock import MagicMock
from moto import mock_ec2
from moto import mock_elbv2
import time
from datetime import datetime, timedelta, timezone
from dateutil.tz import tzutc
from common.common_constants import AWSResourceClassConstants
from common.compliance_object_factory import ComplianceObjectFactory

EVENT_JSON = {
  "version": "1.0",
  "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-12-07T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
  "ruleParameters": "{\n  \"newELBSpareTimeHours\": \"0\", \"forbiddenPorts\": \"22\",\n  \"performAction\": \"True\",\n  \"notifier\": \"ses\" \n}",
  "resultToken": " ",
  "eventLeftScope": "False",
  "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
  "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-zgvfqq",
  "configRuleName": "gaurav-test",
  "configRuleId": "config-rule-zgvfqq",
  "accountId": "107339370656"
}

CONTEXT = ""

RESOURCE_ID = "test-load-balancer"
RESOURCE_TYPE = AWSResourceClassConstants.ELB_RESOURCE
RESOURCE_TYPE_ALB = AWSResourceClassConstants.ELB_V2_RESOURCE
NOT_APPLICABLE_RESOURCE_TYPE = AWSResourceClassConstants.EC2_INSTANCE
CONFIG_ITEMS = [
            {
            "instances": [],
            "DNSName": "ankush-test-mnc-438-948123782.us-east-1.elb.amazonaws.com",
            "loadbalancername": "ankush-test-mnc-438",
            "createdtime": datetime(2017, 12, 8, 6, 26, 57, 730000, tzinfo=tzutc()),
            "region": "us-west-2"
            },
            {
            "instances": [ { "instanceid" : "i-0d3d9d22c306f61e6" } ],
            "loadbalancername": "ankush-test-mnc-438",
            "createdtime": datetime(2017, 12, 8, 6, 26, 57, 730000, tzinfo=tzutc()),
            "region" : "us-west-2"
            },
            {
            'createdtime': datetime(2017, 12, 8, 6, 26, 57, 730000, tzinfo=tzutc()),
            'loadbalancerarn': 'demo',
            "loadbalancername": "ankush-test-mnc-438",
            'TargetGroups': [
                {
                    'TargetGroupArn': 'demo',
                    'TargetGroupName': 'string',
                    'Protocol': 'HTTP',
                    'Port': 123,
                    'VpcId': 'string',
                    'HealthCheckProtocol': 'HTTP',
                    'HealthCheckPort': 'string',
                    'HealthCheckIntervalSeconds': 123,
                    'HealthCheckTimeoutSeconds': 123,
                    'HealthyThresholdCount': 123,
                    'UnhealthyThresholdCount': 123,
                    'HealthCheckPath': 'string',
                    'Matcher': {
                        'HttpCode': 'string'
                    },
                    'Loadbalancerarn': [
                        'demo`',
                    ],
                    'TargetType': 'instance'
                },
            ],
            'NextMarker': 'string'
        }
            ]

class TestDeleteUnusedELBEvaluate(object):

    __regions = [ 'us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __mockInstanceResponse = {
    "Reservations": [
        {
            "Instances": [
                {
                    "StateTransitionReason": "User initiated (2017-09-30 05:25:09 GMT)",
                    "InstanceId": "i-0d3d9d22c306f61e6",
                    "PrivateDnsName": "ip-172-31-43-190.ec2.internal",
                }
             ]
        }
      ]
    }

    __mockELBResponseFail = {
    'TargetHealthDescriptions': [

    ],
    'ResponseMetadata': {
        '...': '...',
    },
}

    __mockELBResponsePass = {
    'TargetHealthDescriptions': [
        {
            'HealthCheckPort': '80',
            'Target': {
                'Id': 'i-0f76fade',
                'Port': 80,
            },
            'TargetHealth': {
                'State': 'healthy',
            },
        },
    ],
    'ResponseMetadata': {
        '...': '...',
    },
}

    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
    __deleteELBResourceEvaluate = elbEvaluate.ELBUnusedLoadBalancersEvaluate(__eventParam)


    @mock_elbv2
    def testCompliantALBEvaluate(self):
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB_V2, region_name=self.__regions[0])
        elbEvaluate.BotoUtility.getClient = MagicMock(return_value=elbClient)
        elbClient.describe_target_groups = MagicMock(return_value=CONFIG_ITEMS[2])
        elbClient.describe_target_health = MagicMock(return_value=self.__mockELBResponsePass)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE_ALB, configItems=CONFIG_ITEMS[2])
        evaluationResult = self.__deleteELBResourceEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_elbv2
    def testNonCompliantALBEvaluate(self):
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB_V2, region_name=self.__regions[0])
        elbEvaluate.BotoUtility.getClient = MagicMock(return_value=elbClient)
        elbClient.describe_target_groups = MagicMock(return_value=CONFIG_ITEMS[2])
        elbClient.describe_target_health = MagicMock(return_value=self.__mockELBResponseFail)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE_ALB, configItems=CONFIG_ITEMS[2])
        evaluationResult = self.__deleteELBResourceEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_ec2
    def testNonCompliantELBEvaluate(self):
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__regions[0])
        elbEvaluate.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_instances = MagicMock(return_value=self.__mockInstanceResponse)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        evaluationResult = self.__deleteELBResourceEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_ec2
    def testCompliantELBEvaluate(self):
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__regions[0])
        elbEvaluate.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_instances = MagicMock(return_value=self.__mockInstanceResponse)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[1])
        evaluationResult = self.__deleteELBResourceEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testNonApplicableELBEvaluate(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=NOT_APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[1])
        evaluationResult = self.__deleteELBResourceEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
