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
#import check_rds_owner_tag_values.test_check_rds_owner_tag_values_action as rdsAction
import check_rds_owner_tag_values.check_rds_owner_tag_values_action as rdsAction
#import check_rds_owner_tag_values.check_rds_owner_tag_values_constants as ownertagconstants
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.abstract_action import *
from common.common_constants import *
from mock import MagicMock
from moto import mock_rds
import time
from datetime import datetime, timedelta, timezone
from dateutil.tz import tzutc

EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-12-07T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
    "ruleParameters": "{\n  \"toEmail\": \"ankush.tehele@reancloud.com\", \"validity\": \"1\",\n  \"performAction\": \"True\",\n  \"notifier\": \"ses\" \n}",
    "resultToken": " ",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-zgvfqq",
    "configRuleName": "ankush-test",
    "configRuleId": "config-rule-zgvfqq",
    "accountId": "107339370656"
}

CONTEXT = ""

RESOURCE_ID = "mnc-543"
APPLICABLE_RESOURCE_TYPE = AWSResourceClassConstants.RDS_INSTANCE
 
__validityExpired = [ { "Key": "NoOwnerExpirationDate", "Value": "2018-01-02"} ]
__inValidTags = [ { "Key": "noOwner", "Value": "donand.trump"} ]

CONFIG_ITEMS = [
    {
        "dbinstancestatus": "available",
        "dbinstancearn": "arn:aws:rds:us-west-2:107339370656:db:mnc-543",
        "dbiResourceid": "db-7ZRAI5ZRYYJDOTSD45PAQZWLZE",
        "dbinstanceidentifier": "mnc-543",
        "region": "us-east-1",
        "multiaz": True,
        "engine": "mysql",
        "Tags": __inValidTags
    },
    {
        "dbinstancestatus": "available",
        "dbinstancearn": "arn:aws:rds:us-west-2:107339370656:db:mnc-543",
        "dbiResourceid": "db-7ZRAI5ZRYYJDOTSD45PAQZWLZE",
        "dbinstanceidentifier": "mnc-543",
        "region": "us-east-1",
        "multiaz": False,
        "engine": "mysql",
        "Tags": __inValidTags
    }, 
    {
        "dbinstancestatus": "stopped",
        "dbinstancearn": "arn:aws:rds:us-west-2:107339370656:db:mnc-543",
        "dbiResourceid": "db-7ZRAI5ZRYYJDOTSD45PAQZWLZE",
        "dbinstanceidentifier": "mnc-543",
        "region": "us-east-1",
        "multiaz": False,
        "engine": "mysql",
        "Tags": __inValidTags
    },
    {
        "dbinstancestatus": "stopped",
        "dbinstancearn": "arn:aws:rds:us-west-2:107339370656:db:mnc-543",
        "dbiResourceid": "db-7ZRAI5ZRYYJDOTSD45PAQZWLZE",
        "dbinstanceidentifier": "mnc-543",
        "region": "us-east-1",
        "engine": "mysql",
        "multiaz": False,
        "Tags": __validityExpired
    },
    {
        "dbinstancestatus": "terminated",
        "dbinstancearn": "arn:aws:rds:us-west-2:107339370656:db:mnc-543",
        "dbiResourceid": "db-7ZRAI5ZRYYJDOTSD45PAQZWLZE",
        "dbinstanceidentifier": "mnc-543",
        "engine": "mysql",
        "region": "us-east-1",
        "multiaz": False,
    },
    {
        "dbinstancestatus": "creating",
        "dbinstancearn": "arn:aws:rds:us-west-2:107339370656:db:mnc-543",
        "dbiResourceid": "db-7ZRAI5ZRYYJDOTSD45PAQZWLZE",
        "dbinstanceidentifier": "mnc-543",
        "DBClusterIdentifier": "samplecluster",
        "region": "us-east-1",
        "engine": "mysql",
        "multiaz": False,
        "Tags": __validityExpired
    }
]


class TestRDSOwnerTagAction(object):
    __regions = ['us-east-1']
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __mockHttpResponseFail = {'ResponseMetadata': { 'HTTPStatusCode': 500, 'RetryAttempts': 0}}
    __mockHttpResponseSuccess = {'ResponseMetadata': { 'HTTPStatusCode': 200, 'RetryAttempts': 0}}
    __checkRdsOwnerAction = rdsAction.CheckRdsOwnerTagValuesAction(__eventParam)
    
    @mock_rds
    def testMultiAZRdsAction(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsAction.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        result = self.__checkRdsOwnerAction.performAction(eventItem)
        assert result.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_rds
    def testStopRdsAction(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsAction.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractAction__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[1])
        rdsClient.stop_db_instance = MagicMock(return_value=self.__mockHttpResponseSuccess)
        rdsClient.add_tags_to_resource = MagicMock(return_value=self.__mockHttpResponseSuccess)
        result = self.__checkRdsOwnerAction.performAction(eventItem)
        assert result.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
    
    @mock_rds
    def testStopFailedRdsAction(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsAction.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractAction__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[1])
        rdsClient.stop_db_instance = MagicMock(return_value=self.__mockHttpResponseFail)
        rdsClient.add_tags_to_resource = MagicMock(return_value=self.__mockHttpResponseSuccess)
        result = self.__checkRdsOwnerAction.performAction(eventItem)
        assert result.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
 
    @mock_rds
    def testAddTagsSuccessRdsAction(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsAction.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractAction__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[2])
        rdsClient.stop_db_instance = MagicMock(return_value=self.__mockHttpResponseSuccess)
        rdsClient.add_tags_to_resource = MagicMock(return_value=self.__mockHttpResponseSuccess)
        result = self.__checkRdsOwnerAction.performAction(eventItem)
        assert result.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_rds
    def testAddTagsFailRdsAction(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsAction.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractAction__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[2])
        rdsClient.stop_db_instance = MagicMock(return_value=self.__mockHttpResponseFail)
        rdsClient.add_tags_to_resource = MagicMock(return_value=self.__mockHttpResponseFail)
        result = self.__checkRdsOwnerAction.performAction(eventItem)
        assert result.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
    
    @mock_rds
    def testDeleteInstanceSuccessAction(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsAction.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractAction__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[3])
        rdsClient.delete_db_instance = MagicMock(return_value=self.__mockHttpResponseSuccess)
        rdsClient.create_db_snapshot = MagicMock(return_value=self.__mockHttpResponseSuccess) 
        result = self.__checkRdsOwnerAction.performAction(eventItem)
        assert result.complianceType == ComplianceConstants.COMPLIANT_RESOURCE
   
    @mock_rds
    def testCreateSnapshotWithSuccessAction(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsAction.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractAction__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[5])
        rdsClient.delete_db_instance = MagicMock(return_value=self.__mockHttpResponseSuccess)
        rdsClient.create_db_snapshot = MagicMock(return_value=self.__mockHttpResponseSuccess) 
        result = self.__checkRdsOwnerAction.performAction(eventItem)
        assert result.complianceType == ComplianceConstants.COMPLIANT_RESOURCE
    
    @mock_rds
    def testCreateSnapshotWithFailAction(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsAction.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractAction__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[5])
        rdsClient.delete_db_instance = MagicMock(return_value=self.__mockHttpResponseSuccess)
        rdsClient.create_db_snapshot = MagicMock(return_value=self.__mockHttpResponseFail) 
        result = self.__checkRdsOwnerAction.performAction(eventItem)
        assert result.complianceType == ComplianceConstants.COMPLIANT_RESOURCE
    
    @mock_rds
    def testDeleteInstanceFailAction(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsAction.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractAction__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[3])
        rdsClient.delete_db_instance = MagicMock(return_value=self.__mockHttpResponseFail)
        rdsClient.create_db_snapshot = MagicMock(return_value=self.__mockHttpResponseSuccess) 
        result = self.__checkRdsOwnerAction.performAction(eventItem)
        assert result.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

