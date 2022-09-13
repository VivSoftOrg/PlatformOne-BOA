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

import delete_unused_security_group.delete_unused_security_group_evaluate as sgEvaluate
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.abstract_evaluate import *
from common.common_constants import *
from mock import MagicMock
from moto import mock_ec2
from moto import mock_rds
from moto import mock_elb
from moto import mock_lambda


EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-12-07T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
    "ruleParameters": "{\n  \"toEmail\": \"ankush.tehele@reancloud.com\", \"forbiddenPorts\": \"22\",\n  \"performAction\": \"True\",\n  \"notifier\": \"ses\" \n}",
    "resultToken": "eyJlbmNyeXB0ZWREYXRhIjpbNTAsNzgsNTIsMjksMTEyLDEwLDIwLDk2LC03Niw4OCwtODYsLTEyMywtODEsLTc3LDkxLC0xMTIsMzcsLTcwLDEwMSwtNTMsOTEsLTEwLDEyMiwzLDk5LC00MSwyMSw5OSw1NywxMDcsLTEyMSwtNDEsLTMsOTksLTU5LDQxLDIxLC0yMywxNSw1MSwtNjgsNTksLTM3LDEwNSwtOSwtMTQsMTI0LDg0LC00OSwzNiwxMCwzOCwtNzMsMTI0LDQ1LC0xLC0yNiwzMCw0Myw4NCwxMiwtNDIsLTc2LC0zLDMsMTEwLDU2LC01OCwtMzMsLTQwLDIwLC03OCwtODgsNywxMDUsLTM1LC0zOCwtODIsLTUwLDQ1LDM0LDExLDExNCwtODYsLTEsLTExNiwtOTIsLTMsMTUsLTczLDU5LDU3LC03OSwtMTIsLTEwMyw3NSwtNjIsLTMzLC0xMDMsLTIsLTUyLDM2LC0xMDUsLTEwOCwtNDcsNzQsMywtNCw5MCwzLDExNiwtOTMsOTAsMTE1LC03MCw1NSwtNTgsNzgsNDYsNjcsMjksLTg1LC01MSwzNSwtMTI2LDc3LDk2LC0yMiwtMTUsNjUsMTUsMjgsNjIsLTU0LC00NiwtNDgsLTUwLDc3LC0zNywtNjYsLTEyMSwtMzgsLTQsMTE4LC03LDE5LC02MSwtMTIzLDIwLDYyLC04Myw0NSwyOSwtMTAsMTI0LC02NSw3NSwtMTI0LDQ0LC02MywtMjcsMjcsLTMxLDk5LDY3LDAsMTIxLC05NywtMjEsLTcxLDMzLDg1LC0xMTQsLTUxLDEyNyw1NCwtMTAyLDcwLC03NCw4LDc0LC0xMjYsNDIsLTIzLDU2LC05OCwtMTA4LDgxLC0xMjgsMTEyLDE5LC03Myw3NCwtODgsLTY1LDc4LDc2LC0xMjYsLTE2LDExOCwtMTEyLDIsLTUyLDY3LC01Myw3NCwxMTYsLTc3LDcyLDk5LC0xNiwtMTAwLC05OSwtMTksOTEsNDksNSwtNzEsLTgsLTYyLDEyNywtMTEsLTQ0LDEyNywtODksNTEsODIsNjEsLTgxLDk4LDU2LC00Miw5MSw2LDI4LC0xNSwyMSwxOSw0MCwxMDgsMTA5LC04LDEyNCwzOSwtNjUsLTU3LDkwLC0xMDEsMTA2LC0yMSwxMTEsLTExOSw2NSw2LC01NSw5MSwtMzUsMTYsLTExOCwtMTA1LDgzLDQ0LDgwXSwibWF0ZXJpYWxTZXRTZXJpYWxOdW1iZXIiOjEsIml2UGFyYW1ldGVyU3BlYyI6eyJpdiI6WzkxLDc1LC03MywtMzEsNCw4LC0yMyw3OSwtODUsLTg1LDIsMTI3LDEyMywtNDksNCw4NV19fQ==eyJlbmNyeXB0ZWREYXRhIjpbNTAsNzgsNTIsMjksMTEyLDEwLDIwLDk2LC03Niw4OCwtODYsLTEyMywtODEsLTc3LDkxLC0xMTIsMzcsLTcwLDEwMSwtNTMsOTEsLTEwLDEyMiwzLDk5LC00MSwyMSw5OSw1NywxMDcsLTEyMSwtNDEsLTMsOTksLTU5LDQxLDIxLC0yMywxNSw1MSwtNjgsNTksLTM3LDEwNSwtOSwtMTQsMTI0LDg0LC00OSwzNiwxMCwzOCwtNzMsMTI0LDQ1LC0xLC0yNiwzMCw0Myw4NCwxMiwtNDIsLTc2LC0zLDMsMTEwLDU2LC01OCwtMzMsLTQwLDIwLC03OCwtODgsNywxMDUsLTM1LC0zOCwtODIsLTUwLDQ1LDM0LDExLDExNCwtODYsLTEsLTExNiwtOTIsLTMsMTUsLTczLDU5LDU3LC03OSwtMTIsLTEwMyw3NSwtNjIsLTMzLC0xMDMsLTIsLTUyLDM2LC0xMDUsLTEwOCwtNDcsNzQsMywtNCw5MCwzLDExNiwtOTMsOTAsMTE1LC03MCw1NSwtNTgsNzgsNDYsNjcsMjksLTg1LC01MSwzNSwtMTI2LDc3LDk2LC0yMiwtMTUsNjUsMTUsMjgsNjIsLTU0LC00NiwtNDgsLTUwLDc3LC0zNywtNjYsLTEyMSwtMzgsLTQsMTE4LC03LDE5LC02MSwtMTIzLDIwLDYyLC04Myw0NSwyOSwtMTAsMTI0LC02NSw3NSwtMTI0LDQ0LC02MywtMjcsMjcsLTMxLDk5LDY3LDAsMTIxLC05NywtMjEsLTcxLDMzLDg1LC0xMTQsLTUxLDEyNyw1NCwtMTAyLDcwLC03NCw4LDc0LC0xMjYsNDIsLTIzLDU2LC05OCwtMTA4LDgxLC0xMjgsMTEyLDE5LC03Myw3NCwtODgsLTY1LDc4LDc2LC0xMjYsLTE2LDExOCwtMTEyLDIsLTUyLDY3LC01Myw3NCwxMTYsLTc3LDcyLDk5LC0xNiwtMTAwLC05OSwtMTksOTEsNDksNSwtNzEsLTgsLTYyLDEyNywtMTEsLTQ0LDEyNywtODksNTEsODIsNjEsLTgxLDk4LDU2LC00Miw5MSw2LDI4LC0xNSwyMSwxOSw0MCwxMDgsMTA5LC04LDEyNCwzOSwtNjUsLTU3LDkwLC0xMDEsMTA2LC0yMSwxMTEsLTExOSw2NSw2LC01NSw5MSwtMzUsMTYsLTExOCwtMTA1LDgzLDQ0LDgwXSwibWF0ZXJpYWxTZXRTZXJpYWxOdW1iZXIiOjEsIml2UGFyYW1ldGVyU3BlYyI6eyJpdiI6WzkxLDc1LC03MywtMzEsNCw4LC0yMyw3OSwtODUsLTg1LDIsMTI3LDEyMywtNDksNCw4NV19fQ==eyJlbmNyeXB0ZWREYXRhIjpbNTAsNzgsNTIsMjksMTEyLDEwLDIwLDk2LC03Niw4OCwtODYsLTEyMywtODEsLTc3LDkxLC0xMTIsMzcsLTcwLDEwMSwtNTMsOTEsLTEwLDEyMiwzLDk5LC00MSwyMSw5OSw1NywxMDcsLTEyMSwtNDEsLTMsOTksLTU5LDQxLDIxLC0yMywxNSw1MSwtNjgsNTksLTM3LDEwNSwtOSwtMTQsMTI0LDg0LC00OSwzNiwxMCwzOCwtNzMsMTI0LDQ1LC0xLC0yNiwzMCw0Myw4NCwxMiwtNDIsLTc2LC0zLDMsMTEwLDU2LC01OCwtMzMsLTQwLDIwLC03OCwtODgsNywxMDUsLTM1LC0zOCwtODIsLTUwLDQ1LDM0LDExLDExNCwtODYsLTEsLTExNiwtOTIsLTMsMTUsLTczLDU5LDU3LC03OSwtMTIsLTEwMyw3NSwtNjIsLTMzLC0xMDMsLTIsLTUyLDM2LC0xMDUsLTEwOCwtNDcsNzQsMywtNCw5MCwzLDExNiwtOTMsOTAsMTE1LC03MCw1NSwtNTgsNzgsNDYsNjcsMjksLTg1LC01MSwzNSwtMTI2LDc3LDk2LC0yMiwtMTUsNjUsMTUsMjgsNjIsLTU0LC00NiwtNDgsLTUwLDc3LC0zNywtNjYsLTEyMSwtMzgsLTQsMTE4LC03LDE5LC02MSwtMTIzLDIwLDYyLC04Myw0NSwyOSwtMTAsMTI0LC02NSw3NSwtMTI0LDQ0LC02MywtMjcsMjcsLTMxLDk5LDY3LDAsMTIxLC05NywtMjEsLTcxLDMzLDg1LC0xMTQsLTUxLDEyNyw1NCwtMTAyLDcwLC03NCw4LDc0LC0xMjYsNDIsLTIzLDU2LC05OCwtMTA4LDgxLC0xMjgsMTEyLDE5LC03Myw3NCwtODgsLTY1LDc4LDc2LC0xMjYsLTE2LDExOCwtMTEyLDIsLTUyLDY3LC01Myw3NCwxMTYsLTc3LDcyLDk5LC0xNiwtMTAwLC05OSwtMTksOTEsNDksNSwtNzEsLTgsLTYyLDEyNywtMTEsLTQ0LDEyNywtODksNTEsODIsNjEsLTgxLDk4LDU2LC00Miw5MSw2LDI4LC0xNSwyMSwxOSw0MCwxMDgsMTA5LC04LDEyNCwzOSwtNjUsLTU3LDkwLC0xMDEsMTA2LC0yMSwxMTEsLTExOSw2NSw2LC01NSw5MSwtMzUsMTYsLTExOCwtMTA1LDgzLDQ0LDgwXSwibWF0ZXJpYWxTZXRTZXJpYWxOdW1iZXIiOjEsIml2UGFyYW1ldGVyU3BlYyI6eyJpdiI6WzkxLDc1LC03MywtMzEsNCw4LC0yMyw3OSwtODUsLTg1LDIsMTI3LDEyMywtNDksNCw4NV19fQ==",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-zgvfqq",
    "configRuleName": "gaurav-test",
    "configRuleId": "config-rule-zgvfqq",
    "accountId": "107339370656"
}
CONTEXT = ""
CONFIGITEMS = {'region': 'us-east-1'}
RESOURCE_ID = ''
RESOURCE_TYPE = AWSResourceClassConstants.SG_RESOURCE


class TestDeleteUnusedSGEvaluate(object):

    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __deleteUnusedSGEvaluate = sgEvaluate.DeleteUnusedSGEvaluate(__eventParam)

    __regions = ['us-east-1', 'us-west-2', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-2']

    @mock_rds
    @mock_ec2
    @mock_elb
    def test_NonCompliantSGEvaluate(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        ec2 = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__regions[0])
        rds = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        elb = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB, region_name=self.__regions[0])

        sg = ec2.create_security_group(GroupName='sg1', Description='Test security group sg1')
        response = ec2.describe_security_groups(GroupIds=[sg['GroupId']])
        CONFIGITEMS['region'] = 'us-east-1'
        RESOURCE_ID = response['SecurityGroups'][0]['GroupId']

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIGITEMS)

        sgEvaluate.BotoUtility.getClient = MagicMock(side_effect=[ec2, rds, elb])

        evaluationResult = self.__deleteUnusedSGEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_elb
    @mock_ec2
    @mock_rds
    @mock_lambda
    def test_CompliantSGEvaluate(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        ec2 = boto3.resource('ec2', region_name='us-west-1')
        vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
        vpc.create_tags(Tags=[{"Key": "Name", "Value": "default_vpc"}])
        ig = ec2.create_internet_gateway()
        vpc.attach_internet_gateway(InternetGatewayId=ig.id)
        route_table = vpc.create_route_table()
        route = route_table.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=ig.id
        )
        subnet = ec2.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc.id)
        sg = ec2.create_security_group(
            GroupName='v-sg1', Description='moto sg', VpcId=vpc.id)
        sg.authorize_ingress(
            CidrIp='0.0.0.0/0',
            IpProtocol='icmp',
            FromPort=-1,
            ToPort=-1
        )
        instances = ec2.create_instances(
            ImageId='ami-835b4efa', InstanceType='t2.micro', MaxCount=1, MinCount=1,
            NetworkInterfaces=[{'SubnetId': subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sg.group_id]}])
        ec2 = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[1])
        lambdaClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_LAMBDA, self.__regions[1])
        response = ec2.describe_security_groups()
        CONFIGITEMS['region'] = 'us-west-2'
        RESOURCE_ID = response['SecurityGroups'][0]['GroupId']
        sgEvaluate.BotoUtility.getClient = MagicMock(side_effect=[ec2, lambdaClient])
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIGITEMS)
        evaluationResult = self.__deleteUnusedSGEvaluate.evaluate(eventItem)

        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE
