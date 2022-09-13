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
from moto import mock_ec2
import ec2_noshutdown_tag.ec2_noshutdown_tag_action as tagAction
from botocore.exceptions import ClientError

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

RESOURCE_ID = ""
RESOURCE_TYPE = AWSResourceClassConstants.EC2_INSTANCE
CONFIG_ITEMS = {"tags": [{"key": "Name", "value": "Priyanka-Test-Machine"}, {"key": "noShutDownKey", "value":   "Yes"}]}


class TestEc2NoshutdownTagAction(object):

    __regions = ['us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __mockInstanceResponse = {'ResponseMetadata': {'HTTPStatusCode': 200, 'RetryAttempts': 0}}
    __mockInstanceResponse_fail = {'ResponseMetadata': {'HTTPStatusCode': 500, 'RetryAttempts': 0}}
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
    __ec2NoshutdownTagAction = tagAction.Ec2NoshutdownTagAction(__eventParam)
    __errorResponse = {'Error':{
        'Code':400,
        'Message':'AccessDenied'
    }}
    def __getEventItem(self):
        ec2 = boto3.resource('ec2', 'us-east-1')
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
        ec2.create_tags(Resources=[instances[0].instance_id], Tags=[{'Key': 'noShutDownKey', 'Value': 'Yes'}])
        ec2 = boto3.client('ec2', 'us-east-1')
        response = ec2.describe_instances(InstanceIds=[instances[0].instance_id])
        RESOURCE_ID = instances[0].instance_id
        instanceObject = response
        instanceObject.update({'region':'us-east-1'})
        instanceObject.update({'noShutDownKey': 'Yes'})
        CONFIG_ITEMS = instanceObject
        
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)

        return eventItem

    @mock_ec2
    def test_ec2_noshutdown_tag_success(self):
        ec2 = boto3.resource('ec2', 'us-east-1')
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
        ec2.create_tags(Resources=[instances[0].instance_id], Tags=[{'Key': 'noShutDownKey', 'Value': 'Yes'}])
        ec2 = boto3.client('ec2', 'us-east-1')
        response = ec2.describe_instances(InstanceIds=[instances[0].instance_id])
        RESOURCE_ID = instances[0].instance_id
        instanceObject = response
        instanceObject.update({'region':'us-east-1'})
        instanceObject.update({'noShutDownKey': 'Yes'})
        CONFIG_ITEMS = instanceObject
        tagAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        ec2.delete_tags = MagicMock(return_value=self.__mockInstanceResponse)
        evaluationResult = self.__ec2NoshutdownTagAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_ec2
    def test_ec2_noshutdown_tag_failure(self):
        eventItem = self.__getEventItem()
        ec2 = boto3.client('ec2', 'us-east-1')
        tagAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        ec2.delete_tags = MagicMock(return_value=self.__mockInstanceResponse_fail)
        evaluationResult = self.__ec2NoshutdownTagAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_ec2
    def test_ec2_noshutdown_tag_exception_keyerror(self):
        eventItem = self.__getEventItem()
        ec2 = boto3.client('ec2', 'us-east-1')
        tagAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        ec2.delete_tags = MagicMock(side_effect=KeyError("Mock Exception: Key not found"))
        evaluationResult = self.__ec2NoshutdownTagAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_ec2
    def test_ec2_noshutdown_tag_exception_syntaxerror(self):
        eventItem = self.__getEventItem()
        ec2 = boto3.client('ec2', 'us-east-1')
        tagAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        ec2.delete_tags = MagicMock(side_effect=SyntaxError("Mock Exception: Key not found"))
        evaluationResult = self.__ec2NoshutdownTagAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_ec2
    def test_ec2_noshutdown_tag_exception_attribute_error(self):
        eventItem = self.__getEventItem()
        ec2 = boto3.client('ec2', 'us-east-1')
        tagAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        ec2.delete_tags = MagicMock(side_effect=AttributeError("Mock Exception: Attribute not found"))
        evaluationResult = self.__ec2NoshutdownTagAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_ec2
    def test_ec2_noshutdown_tag_exception_value_error(self):
        eventItem = self.__getEventItem()
        ec2 = boto3.client('ec2', 'us-east-1')
        tagAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        ec2.delete_tags = MagicMock(side_effect=ValueError("Mock Exception: Key not found"))
        evaluationResult = self.__ec2NoshutdownTagAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_ec2
    def test_ec2_noshutdown_tag_exception_clienterror(self):
        eventItem = self.__getEventItem()
        ec2 = boto3.client('ec2', 'us-east-1')
        tagAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        ec2.delete_tags = MagicMock(side_effect=ClientError(self.__errorResponse,"AssumeRole"))
        evaluationResult = self.__ec2NoshutdownTagAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION
