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
import common.compliance_object_factory as complianceobjectfactory
from common.abstract_evaluate import *
from common.common_constants import *
from mock import MagicMock
from moto import mock_elb
from moto import mock_elbv2
import time
from datetime import datetime, timedelta, timezone
from dateutil.tz import tzutc
import delete_unused_elb.delete_unused_elb_action as elbAction
from common.common_constants import AWSResourceClassConstants
from common.compliance_object_factory import ComplianceObjectFactory


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

RESOURCE_ID = "ankush-test-mnc-438"
RESOURCE_TYPE = AWSResourceClassConstants.ELB_RESOURCE
CONFIG_ITEMS = [
            {
            "instances": [],
            "DNSName": "ankush-test-mnc-438-948123782.us-east-1.elb.amazonaws.com",
            "loadbalancername": "ankush-test-mnc-438",
            "createdtime": datetime(2017, 12, 8, 6, 26, 57, 730000, tzinfo=tzutc()),
            "region" : "us-east-1"
            }
          ]

class TestDeleteUnusedELBAction(object):

    __regions = [ 'us-east-1']
    __mockInstanceResponse = {'ResponseMetadata': { 'HTTPStatusCode': 200, 'RetryAttempts': 0}}
    __mockInstanceResponse_fail = {'ResponseMetadata': { 'HTTPStatusCode': 500, 'RetryAttempts': 0}}
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
    __deleteELBResourceAction = elbAction.UnusedELBAction(__eventParam)


    @mock_elbv2
    def testALBDeletSuccess(self):
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB_V2, region_name=self.__regions[0])
        elbAction.BotoUtility.getClient = MagicMock(return_value=elbClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        elbClient.delete_load_balancer = MagicMock(return_value=self.__mockInstanceResponse)
        return_value = self.__deleteELBResourceAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_elbv2
    def testALBDeletFail(self):
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB_V2, region_name=self.__regions[0])
        elbAction.BotoUtility.getClient = MagicMock(return_value=elbClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        elbClient.delete_load_balancer = MagicMock(return_value=self.__mockInstanceResponse_fail)
        return_value = self.__deleteELBResourceAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE


    @mock_elbv2
    def testALBDeletException(self):
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB_V2, region_name=self.__regions[0])
        elbAction.BotoUtility.getClient = MagicMock(return_value=elbClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        elbClient.delete_load_balancer = MagicMock(side_effect=Exception("Mock Exception: Failed to detete resource"))
        return_value = self.__deleteELBResourceAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION


    @mock_elb
    def testELBDeletSuccess(self):
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB, region_name=self.__regions[0])
        elbAction.BotoUtility.getClient = MagicMock(return_value=elbClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        elbClient.delete_load_balancer = MagicMock(return_value=self.__mockInstanceResponse)
        return_value = self.__deleteELBResourceAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_elb
    def testELBDeletFail(self):
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB, region_name=self.__regions[0])
        elbAction.BotoUtility.getClient = MagicMock(return_value=elbClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        elbClient.delete_load_balancer = MagicMock(return_value=self.__mockInstanceResponse_fail)
        return_value = self.__deleteELBResourceAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_elb
    def testELBDeletException(self):
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB, region_name=self.__regions[0])
        elbAction.BotoUtility.getClient = MagicMock(return_value=elbClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        elbClient.delete_load_balancer = MagicMock(side_effect=Exception("Mock Exception: Failed to detete resource"))
        return_value = self.__deleteELBResourceAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

