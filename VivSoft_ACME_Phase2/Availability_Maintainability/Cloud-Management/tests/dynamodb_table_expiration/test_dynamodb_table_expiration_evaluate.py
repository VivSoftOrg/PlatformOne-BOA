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
sys.path.append('../../')

from dynamodb_table_expiration.dynamodb_table_expiration_evaluate import *
from dynamodb_table_expiration.dynamodb_table_expiration_constants import *
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.abstract_evaluate import *
from common.common_constants import *
from common.boto_utility import *
from mock import MagicMock
from moto import mock_dynamodb2


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
RESOURCE_TYPE = AWSResourceClassConstants.DYNAMO_DB_RESOURCE
RESOURCE_ID = 'TableName'

class TestDynamoDBTableExpirationEvaluate(object):

    _AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems={})

    __dynamoDBEvaluator = DynamoDBTableEvaluate(_AbstractEvaluator__eventParam)

    @mock_dynamodb2
    def testEvaluateForDynamoDBTablesWithDaysRemaining(self):
        self.__dynamoDBEvaluator._DynamoDBTableEvaluate__getExpirationDate = MagicMock(return_value = True)
        self.__dynamoDBEvaluator._DynamoDBTableEvaluate__getValidity = MagicMock(return_value = 17)
        evaluationResult = self.__dynamoDBEvaluator.evaluate(self.__eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_dynamodb2
    def testEvaluateForDynamoDBTablesDateExceeded(self):
        self.__dynamoDBEvaluator._DynamoDBTableEvaluate__getExpirationDate = MagicMock(return_value=True)
        self.__dynamoDBEvaluator._DynamoDBTableEvaluate__getValidity = MagicMock(return_value=27)
        evaluationResult = self.__dynamoDBEvaluator.evaluate(self.__eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_dynamodb2
    def testEvaluateForDynamoDBTablesAboutToExpireBoundaryCondition1(self):
        self.__dynamoDBEvaluator._DynamoDBTableEvaluate__getExpirationDate = MagicMock(return_value=True)
        self.__dynamoDBEvaluator._DynamoDBTableEvaluate__getValidity = MagicMock(return_value = 3)
        evaluationResult = self.__dynamoDBEvaluator.evaluate(self.__eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForDynamoDBTablesAboutToExpireBoundaryCondition2(self):
        self.__dynamoDBEvaluator._DynamoDBTableEvaluate__getExpirationDate = MagicMock(return_value=True)
        self.__dynamoDBEvaluator._DynamoDBTableEvaluate__getValidity = MagicMock(return_value = -5)
        evaluationResult = self.__dynamoDBEvaluator.evaluate(self.__eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_dynamodb2
    def testEvaluateForDynamoDBTableExpired(self):
        self.__dynamoDBEvaluator._DynamoDBTableEvaluate__getExpirationDate = MagicMock(return_value=True)
        self.__dynamoDBEvaluator._DynamoDBTableEvaluate__getValidity = MagicMock(return_value=1)
        evaluationResult = self.__dynamoDBEvaluator.evaluate(self.__eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_dynamodb2
    def testEvaluateForDynamoDBTableTagNotFound(self):
        self.__dynamoDBEvaluator._DynamoDBTableEvaluate__getExpirationDate = MagicMock(return_value=False)
        evaluationResult = self.__dynamoDBEvaluator.evaluate(self.__eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
