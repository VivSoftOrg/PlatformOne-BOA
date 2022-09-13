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
import sys
import boto3
sys.path.append('../../')

import dynamodb_table_expiration.dynamodb_table_expiration_resource_fetcher as dynamoDBTableFetcher
import common.compliance_object_factory as complianceobjectfactory
from common.abstract_evaluate import *
from common.common_constants import *
from mock import MagicMock
from moto import mock_dynamodb2


EVENT_JSON = {
      "configRuleId": "config-rule-1v52mx",
      "version": "1.0",
      "configRuleName": "aws-sample-rule",
      "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-1v52mx",
      "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
      "resultToken": "",
      "ruleParameters": "{\"validity\": \"5\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
      "eventLeftScope": "False",
      "executionRoleArn": "arn:aws:iam::107339370656:role/awsconfig-role",
      "accountId": "107339370656"
}


CONTEXT = ""


class TestDynamoDBExpirationFetcher(object):

    __regions = ['ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __dynamoDBTableFetcher = dynamoDBTableFetcher.DynamoDBTableResourceFetcher(__eventParam)


    @mock_dynamodb2
    def testResourceFetcher(self):
        dynamoDBTableFetcher.regions = MagicMock(return_value = self.__regions)
        dynamoDBResource = boto3.resource(BotoConstants.BOTO_CLIENT_AWS_DYNAMO_DB, self.__regions[0])
        dynamoDBTableFetcher.BotoUtility.getResource = MagicMock(return_value=dynamoDBResource)
        dynamoDBResource.create_table(
                            AttributeDefinitions=[
                                {
                                    'AttributeName' : 'MockAttribute1',
                                    'AttributeType' : 'S'
                                },
                                {
                                    'AttributeName' : 'MockAttribute2',
                                    'AttributeType' : 'S'
                                }
                            ],
                            TableName='MockTable',
                            KeySchema=[
                                {
                                    'AttributeName' : 'MockAttribute1',
                                    'KeyType' : 'HASH'
                                },
                                {
                                    'AttributeName' : 'MockAttribute2',
                                    'KeyType' : 'RANGE'
                                }
                            ],
                            ProvisionedThroughput={
                                'ReadCapacityUnits' : 5,
                                'WriteCapacityUnits' : 5
                            })

        return_value = self.__dynamoDBTableFetcher.resourceFetcher()
        assert bool(return_value) == True

    @mock_dynamodb2
    def testResourceFetcherNoData(self):
        dynamoDBResource = boto3.client(BotoConstants.BOTO_CLIENT_AWS_DYNAMO_DB, self.__regions[0])
        dynamoDBTableFetcher.BotoUtility.getResource = MagicMock(return_value=dynamoDBResource)
        return_value = self.__dynamoDBTableFetcher.resourceFetcher()
        assert bool(return_value) == False
