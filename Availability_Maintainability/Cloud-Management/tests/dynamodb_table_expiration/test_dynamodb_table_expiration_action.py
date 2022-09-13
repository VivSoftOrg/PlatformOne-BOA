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

from dynamodb_table_expiration.dynamodb_table_expiration_action import *
from dynamodb_table_expiration.dynamodb_table_expiration_constants import *
import common.compliance_object_factory as complianceObjectFactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.abstract_evaluate import *
from common.common_constants import *
from mock import MagicMock
from moto import mock_dynamodb2
from dynamoDB_client import *

RESOURCE_ID = "TableName"
RESOURCE_TYPE = AWSResourceClassConstants.DYNAMO_DB_RESOURCE

EVENT_JSON = {
      "configRuleId": "config-rule-1v52mx",
      "version": "1.0",
      "configRuleName": "aws-sample-rule",
      "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-1v52mx",
      "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
      "resultToken": "",
      "ruleParameters": "{\"validity\": \"5\", \n \"expirationDateLimit\": \"20\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
      "eventLeftScope": "False",
      "executionRoleArn": "arn:aws:iam::107339370656:role/awsconfig-role",
      "accountId": "107339370656"
}

CONTEXT = ""


class TestDynamoDBExpirationAction(object):

    __DynamoDBLimitDateExceeded = {
        'ARN': 'arn:aws:dynamodb:us-east-1:107339370656:table/tableName',
        'action': Constants.DYNAMO_DB_TABLE_EXPIRATION_DATE_LIMIT_EXCEEDED,
        'region': 'us-east-1'
    }

    __DynamoDBAboutToExpire = {
        'ARN': 'arn:aws:dynamodb:us-east-1:107339370656:table/tableName',
        'action': Constants.DYNAMO_DB_TABLE_ABOUT_TO_EXPIRE,
        'region': 'us-east-1'
    }

    __DynamoDBExpired = {
        'ARN': 'arn:aws:dynamodb:us-east-1:107339370656:table/tableName',
        'action': Constants.DYNAMO_DB_TABLE_VALIDITY_EXPIRED,
        'region': 'us-east-1'
    }

    __DynamoDBExpirationTagNotFound = {
        'ARN': 'arn:aws:dynamodb:us-east-1:107339370656:table/tableName',
        'action': Constants.DYNAMO_DB_TABLE_VALIDITY_EXPIRED,
        'region': 'us-east-1'
    }

    _AbstractAction__eventParam = complianceObjectFactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __awsRegion = "us-east-1"

    __dynamoDBClient = TestMockDynamoDBClient.mock()
    __dynamoDBAction = DynamoDBTableAction(_AbstractAction__eventParam)

    @mock_dynamodb2
    def testPerformActionAddExpirationTag(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__DynamoDBLimitDateExceeded)
        mockResponse = {
            Constants.DYNAMO_DB_RESPONSE_METADATA: {
                Constants.DYNAMO_DB_HTTP_STATUS_CODE: 200
                }
        }
        self.__dynamoDBClient.tag_resource = MagicMock(return_value = mockResponse)
        BotoUtility.getClient = MagicMock(return_value=self.__dynamoDBClient)
        return_value = self.__dynamoDBAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_dynamodb2
    def testPerformActionAddExpirationTagFailure(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__DynamoDBLimitDateExceeded)
        mockResponse = {
            Constants.DYNAMO_DB_RESPONSE_METADATA: {
                Constants.DYNAMO_DB_HTTP_STATUS_CODE: 400
            }
        }
        self.__dynamoDBClient.tag_resource = MagicMock(return_value=mockResponse)
        BotoUtility.getClient = MagicMock(return_value=self.__dynamoDBClient)
        return_value = self.__dynamoDBAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_dynamodb2
    def testPerformActionAddExpirationTagRaisesException(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems={})        
        BotoUtility.getClient = MagicMock(return_value=self.__dynamoDBClient)
        return_value = self.__dynamoDBAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    @mock_dynamodb2
    def testPerformActionDeleteTable(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__DynamoDBExpired)
        mockResponse = {
            Constants.DYNAMO_DB_RESPONSE_METADATA: {
                Constants.DYNAMO_DB_HTTP_STATUS_CODE: 200
            }
        }

        self.__dynamoDBClient.delete_table = MagicMock(return_value=mockResponse)
        BotoUtility.getClient = MagicMock(return_value=self.__dynamoDBClient)
        return_value = self.__dynamoDBAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_dynamodb2
    def testPerformActionDeleteTableFailure(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__DynamoDBExpired)
        mockResponse = {
            Constants.DYNAMO_DB_RESPONSE_METADATA: {
                Constants.DYNAMO_DB_HTTP_STATUS_CODE: 400
            }
        }

        self.__dynamoDBClient.delete_table = MagicMock(return_value=mockResponse)
        BotoUtility.getClient = MagicMock(return_value=self.__dynamoDBClient)
        return_value = self.__dynamoDBAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_dynamodb2
    def testPerformActionDeleteTableRaiseException(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems={})
        self.__dynamoDBClient.delete_table = MagicMock(side_effect=Exception("Error deleting Table"))
        BotoUtility.getClient = MagicMock(return_value=self.__dynamoDBClient)
        return_value = self.__dynamoDBAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION