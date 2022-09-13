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

import delete_ec2_unused_enis.delete_ec2_unused_enis_action as unusedENIs
import delete_ec2_unused_enis.delete_ec2_unused_enis_constants as unusedENIsConstants
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.abstract_evaluate import *
from common.common_constants import *
from mock import MagicMock
from moto import mock_ec2

RESOURCE_ID = "eni-xyz"
RESOURCE_TYPE = AWSResourceClassConstants.ENI_RESOURCE
CONFIG_ITEMS = [{"status": "in-use"}, {"status": "available"}]

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


class TestUnusedNetworkInterfacesAction(object):

    __awsRegion = "us-east-1"
    __mockInstanceResponse_fail = {'ResponseMetadata': {'HTTPStatusCode': "500", 'RetryAttempts': "0"}}

    @mock_ec2
    def testPerformAction(self):
        self._AbstractAction__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[1])
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__awsRegion)
        unusedENIs.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        mockResponse = {
            unusedENIsConstants.Constants.ENI_STATUS_CODE_RESPONSE_METADATA: {
                unusedENIsConstants.Constants.ENI_HTTP_STATUS_CODE: 200
            }
        }
        ec2Client.delete_network_interface = MagicMock(return_value=mockResponse)
        return_value = unusedENIs.DeleteEC2UnusedENIsAction.performAction(self, eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_ec2
    def testPerformActionFailure(self):
        self._AbstractAction__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[1])
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__awsRegion)
        unusedENIs.BotoUtility.getClient = MagicMock(return_value=ec2Client)

        ec2Client.delete_network_interface = MagicMock(return_value=self.__mockInstanceResponse_fail)
        return_value = unusedENIs.DeleteEC2UnusedENIsAction.performAction(self, eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_ec2
    def testPerformActionRaisesException(self):
        self._AbstractAction__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[1])
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__awsRegion)
        unusedENIs.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.delete_network_interface = MagicMock(side_effect=Exception("Failed to delete ENI"))
        return_value = unusedENIs.DeleteEC2UnusedENIsAction.performAction(self, eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION
