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
from botocore.exceptions import ClientError
import delete_unused_route_tables.delete_unused_route_tables_action as routeTableAction


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

RESOURCE_ID = 'rtb-0f89c472'
RESOURCE_TYPE = AWSResourceClassConstants.ROUTE_TABLE_RESOURCE
CONFIG_ITEMS = {'region': 'us-east-1', 'routes': [{'state': 'active', 'origin': 'CreateRouteTable', 'gatewayid': 'local', 'destinationcidrblock': '172.31.0.0/16'}, {'state': 'active', 'origin': 'CreateRoute', 'gatewayid': 'igw-c76e16be', 'destinationcidrblock': '0.0.0.0/0'}], 'tags': [], 'vpcid': 'vpc-a25216da', 'associations': [{'routetableassociationid': 'rtbassoc-6717221a', 'routetableid': 'rtb-f51cf788', 'main': True}], 'routetableid': 'rtb-f51cf788', 'propagatingvgws': []}


class TestEc2NoshutdownTagAction(object):

    __regions = ['us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __mockInstanceResponse = {'ResponseMetadata': {'HTTPStatusCode': 200, 'RetryAttempts': 0}}
    __mockInstanceResponse_fail = {'ResponseMetadata': {'HTTPStatusCode': 500, 'RetryAttempts': 0}}
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __deleteUnusedRouteTableAction = routeTableAction.DeleteUnusedRouteTablesAction(__eventParam)
    __errorResponse = {'Error': {
        'Code': 400,
        'Message': 'AccessDenied'
    }}

    @mock_ec2
    def test_ec2_noshutdown_tag_success(self):
        ec2 = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        routeTableAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        ec2.delete_route_table = MagicMock(return_value=self.__mockInstanceResponse)
        evaluationResult = self.__deleteUnusedRouteTableAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

    @mock_ec2
    def test_ec2_noshutdown_tag_failure(self):
        ec2 = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        routeTableAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        ec2.delete_route_table = MagicMock(return_value=self.__mockInstanceResponse_fail)
        evaluationResult = self.__deleteUnusedRouteTableAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_ec2
    def test_ec2_noshutdown_tag_exception(self):
        ec2 = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        routeTableAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        ec2.delete_route_table = MagicMock(side_effect=ValueError("Mock Exception: Failed to get resource"))
        evaluationResult = self.__deleteUnusedRouteTableAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_ec2
    def test_ec2_noshutdown_tag_exception_keyerror(self):
        ec2 = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        routeTableAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        ec2.delete_route_table = MagicMock(side_effect=KeyError("Mock Exception: Key not found error"))
        evaluationResult = self.__deleteUnusedRouteTableAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_ec2
    def test_ec2_noshutdown_tag_exception_attributeerror(self):
        ec2 = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        routeTableAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        ec2.delete_route_table = MagicMock(side_effect=AttributeError("Mock Exception: Attribute not found error"))
        evaluationResult = self.__deleteUnusedRouteTableAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_ec2
    def test_ec2_noshutdown_tag_exception_error(self):
        ec2 = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        routeTableAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        ec2.delete_route_table = MagicMock(side_effect=Exception("Mock Exception: syntax error"))
        evaluationResult = self.__deleteUnusedRouteTableAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_ec2
    def test_ec2_noshutdown_tag_exception_clienterror(self):
        ec2 = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
        routeTableAction.BotoUtility.getClient = MagicMock(return_value=ec2)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        ec2.delete_route_table = MagicMock(side_effect=ClientError(self.__errorResponse, "AssumeRole"))
        evaluationResult = self.__deleteUnusedRouteTableAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION
