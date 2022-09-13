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
from datetime import datetime
import boto3
import iam_keys_age.iam_keys_age_resource_fetcher as iamKeysFetcher
import common.compliance_object_factory as complianceobjectfactory
from common.common_constants import *
from mock import MagicMock
from moto import mock_iam

EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-08-21T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
    "ruleParameters": "{ \"iamKeyValidity\": \"90\",\"performAction\": \"True\",\"notifier\": \"sns\",\"toEmail\": \"ankush.tehele@reancloud.com\"}",
    "resultToken": "",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-zgvfqq",
    "configRuleName": "gaurav-test",
    "configRuleId": "config-rule-zgvfqq",
    "accountId": "107339370656"
}

CONTEXT = ""


class TestIamKeysAgeResourceFetcher(object):

    __awsRegion = "us-east-1"
    __mockResponse = [
        {
            "Users": [
                {
                    "PasswordLastUsed": "2018-01-31T06:11:11Z",
                    "UserId": "AIDAJL4OU5RQKCVG4SZJ6",
                    "Arn": "arn:aws:iam::693265998683:user/ankush.tehele",
                    "CreateDate": "2017-12-20T13:58:36Z",
                    "UserName": "ankush.tehele",
                    "Path": "/"
                }
            ]
        }
    ]
    __mockResponseGetKeys = [
        {
            "AccessKeyMetadata": [
                {
                    "AccessKeyId": "AKIAJA6PEGVJE6S6CUZQ",
                    "Status": "Active",
                    "CreateDate": "2018-01-31T06:27:41Z",
                    "UserName": "ankush.tehele"
                }
            ]
        }

    ]
    __mockResponseGetUser = [
        {
            "User": {
                "PasswordLastUsed": "2018-01-31T06:11:11Z",
                "UserId": "AIDAJL4OU5RQKCVG4SZJ6",
                "Path": "/",
                "CreateDate": "2017-12-20T13:58:36Z",
                "UserName": "ankush.tehele",
                "Arn": "arn:aws:iam::693265998683:user/ankush.tehele"
            }
        }
    ]

    __mockResponseAccessKey = [    
        {
            'UserName': 'ankush.tehele',
            'AccessKeyLastUsed': {
                'LastUsedDate': datetime(2015, 1, 1),
                'ServiceName': 'EC2',
                'Region': 'us-east-1'
            }
        }
    ]
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
    __iamKeysAgeResourceFetcher = iamKeysFetcher.IamKeysAgeResourceFetcher(__eventParam)
    
    @mock_iam
    def testIamKeysResourceFetcher(self):
        iamClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_IAM, region_name=self.__awsRegion)
        iamKeysFetcher.BotoUtility.getClient = MagicMock(return_value=iamClient)
        iamClient.list_users = MagicMock(return_value=self.__mockResponse[0])
        iamClient.list_access_keys = MagicMock(return_value=self.__mockResponseGetKeys[0])
        iamClient.get_access_key_last_used = MagicMock(return_value=self.__mockResponseAccessKey[0])
        iamClient.get_user = MagicMock(return_value=self.__mockResponseGetUser[0])
        return_value = self.__iamKeysAgeResourceFetcher.resourceFetcher()
        assert bool(return_value) != False

    @mock_iam
    def testIamKeysResourceFetcherFailure(self):
        iamClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_IAM, region_name=self.__awsRegion)
        iamKeysFetcher.BotoUtility.getClient = MagicMock(return_value=iamClient)
        iamClient.list_users = MagicMock(return_value=self.__mockResponse[0])
        iamClient.list_access_keys = MagicMock(return_value=self.__mockResponseGetKeys[0])
        iamClient.get_user = MagicMock(side_effect=Exception("Mock Exception: Failed to fetch resource details"))
        return_value = self.__iamKeysAgeResourceFetcher.resourceFetcher()
        assert bool(return_value) == False