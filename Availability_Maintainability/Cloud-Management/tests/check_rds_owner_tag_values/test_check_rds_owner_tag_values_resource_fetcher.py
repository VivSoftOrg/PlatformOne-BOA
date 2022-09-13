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
import check_rds_owner_tag_values.check_rds_owner_tag_values_resource_fetcher as ownerTagFetcher
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.abstract_evaluate import *
from common.common_constants import *
from mock import MagicMock
from moto import mock_rds

EVENT_JSON = {
    "configRuleId": "config-rule-1v52mx",
    "version": "1.0",
    "configRuleName": "aws-sample-rule",
    "configRuleArn": "arn:aws:config:us-east-1:411815166437:config-rule/config-rule-1v52mx",
    "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-12-07T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
    "resultToken": "",
    "eventLeftScope": "False",
    "ruleParameters": "{\n  \"toEmail\": \"ankush.tehele@reancloud.com\", \"forbiddenPorts\": \"22\",\n  \"performAction\": \"True\",\n  \"notifier\": \"ses\" \n}",
    "executionRoleArn": "arn:aws:iam::411815166437:role/awsconfig-role",
    "accountId": "411815166437"
}

CONTEXT = ""


class TestOwnerTagFetcher(object):

    __awsRegion = "us-east-1"
    __mockResponse = [
    {
        "dbinstances": [{
            "multiaz": False,
            "dbinstanceidentifier": "mnc-543",
            "dbinstancestatus": "stopped",
            "dbinstancearn": "arn:aws:rds:us-west-2:107339370656:db:mnc-543",
        }]
    },
    {
        "dbinstances": [{
            "multiaz": False,
            "dbinstanceidentifier": "mnc-543",
            "dbinstancestatus": "stopped",
            "dbinstancearn": "arn:aws:rds:us-west-2:107339370656:db:mnc-543",
            "TagList" : [ {"Key" : "Owner","Value": "ankush.tehele" } ]
        }]
    }
    ]
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
    __deleteELBResourceFetcher = ownerTagFetcher.CheckRDSOwnerTagValuesResourceFetcher(__eventParam) 
    
    @mock_rds
    def testResourceFetcher(self):
        eventItems = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId='mnc-543', resourceType=AWSResourceClassConstants.RDS_INSTANCE, configItems=self.__mockResponse[0])
        self.CheckRDSOwnerTagValuesResourceFetcher__parseAndFetchInstanceDetails = MagicMock(return_value = eventItems)
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__awsRegion)
        ownerTagFetcher.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        rdsClient.describe_db_instances = MagicMock(return_value=self.__mockResponse[0])
        return_value = self.__deleteELBResourceFetcher.resourceFetcher()
        assert bool(return_value) != False
    
    @mock_rds
    def testResourceFetcherWithTags(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__awsRegion)
        eventItems = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId='mnc-543', resourceType=AWSResourceClassConstants.RDS_INSTANCE, configItems=self.__mockResponse[1])
        self.CheckRDSOwnerTagValuesResourceFetcher__parseAndFetchInstanceDetails = MagicMock(return_value = eventItems)
        ownerTagFetcher.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        rdsClient.describe_db_instances = MagicMock(return_value=self.__mockResponse[1])
        return_value = self.__deleteELBResourceFetcher.resourceFetcher()
        assert bool(return_value) != False

    @mock_rds
    def testResourceFetcherFailure(self):
        self._AbstractResourceFetcher__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
        eventItems = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId='mnc-543', resourceType=AWSResourceClassConstants.RDS_INSTANCE, configItems=self.__mockResponse[0])
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__awsRegion)
        ownerTagFetcher.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        rdsClient.describe_db_instances = MagicMock(side_effect=Exception("Mocke exception: Failed to fetch resource details"))
        return_value = ownerTagFetcher.CheckRDSOwnerTagValuesResourceFetcher.resourceFetcher(self)
        assert bool(return_value) == False
