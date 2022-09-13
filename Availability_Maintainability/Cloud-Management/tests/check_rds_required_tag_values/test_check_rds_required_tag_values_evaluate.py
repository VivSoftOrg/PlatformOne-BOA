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
import check_rds_required_tag_values.check_rds_required_tag_values_evaluate as rdsEvaluate
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.abstract_evaluate import *
from common.common_constants import *
from common.boto_utility import *
from mock import MagicMock
from moto import mock_rds

EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-12-07T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
    "ruleParameters": "{\n  \"toEmail\": \"ankush.tehele@reancloud.com\", \"validity\": \"1\",\n  \"performAction\": \"True\",\n  \"notifier\": \"ses\", \"RequiredTags\":\"Owner, Project, Environment, ExpirationDate\" \n}",
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
NOT_APPLICABLE_RESOURCE_TYPE = AWSResourceClassConstants.EC2_INSTANCE
 
__validTags = [ { "Key": "Owner", "Value": "ankush.tehele"},{ "Key": "Project", "Value": "MNC"},{ "Key": "Environment", "Value": "test"},{ "Key": "ExpirationDate", "Value": ""} ]
__inValidTags = [ { "Key": "Owner", "Value": "donand.trump"} ]

CONFIG_ITEMS = [
    {
        "dbinstancestatus": "available",
        "dbinstancearn": "arn:aws:rds:us-west-2:107339370656:db:mnc-543",
        "dbiResourceid": "db-7ZRAI5ZRYYJDOTSD45PAQZWLZE",
        "dbinstanceidentifier": "mnc-543",
        "region": "us-east-1",
        "multiaz": False,
        "Tags": __validTags
    },
    {
        "dbinstancestatus": "stopped",
        "dbinstancearn": "arn:aws:rds:us-west-2:107339370656:db:mnc-543",
        "dbiResourceid": "db-7ZRAI5ZRYYJDOTSD45PAQZWLZE",
        "dbinstanceidentifier": "mnc-543",
        "region": "us-east-1",
        "multiaz": False,
        "Tags": __inValidTags
    },
    {
        "dbinstancestatus": "terminated",
        "dbinstancearn": "arn:aws:rds:us-west-2:107339370656:db:mnc-543",
        "dbiresourceid": "db-7ZRAI5ZRYYJDOTSD45PAQZWLZE",
        "dbinstanceidentifier": "mnc-543",
        "region": "us-east-1",
        "multiaz": False,
        "Tags": __validTags
    },
    {
        "dbinstancestatus": "available",
        "dbinstancearn": "arn:aws:rds:us-west-2:107339370656:db:mnc-543",
        "dbiResourceid": "db-7ZRAI5ZRYYJDOTSD45PAQZWLZE",
        "dbinstanceidentifier": "mnc-543",
        "dbclusteridentifier": "mnc-543",
        "region": "us-east-1",
        "multiaz": False,
        "Tags": __validTags
    }
]


class TestRDSRequiredTagEvaluate(object):
    __regions = ['us-east-1']
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __mockTagResponse = { "TagList":[ { "Key": "Owner", "Value": "ankush.tehele"},{ "Key": "Project", "Value": "MNC"},{ "Key": "Environment", "Value": "test"},{ "Key": "ExpirationDate", "Value": "2018-20-01"}] }
    __mockTagResponseEmpty = { "TagList":[ ] }
    
    __checkRdsRequiredEvaluate = rdsEvaluate.CheckRDSRequiredTagValuesEvaluate(__eventParam) 
     
    @mock_rds
    def testNonValidRequiredRDSEvaluate(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsEvaluate.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractEvaluator__eventParam = self.__eventParam
        rdsClient.list_tags_for_resource = MagicMock(return_value=self.__mockTagResponseEmpty) 
        rdsClient.remove_tags_from_resource = MagicMock(return_value=self.__mockTagResponse) 
        self._CheckRDSRequiredTagValuesEvaluate__applicableResources = [APPLICABLE_RESOURCE_TYPE]
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[1])
        evaluationResult = self.__checkRdsRequiredEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
    
    @mock_rds
    def testTerminatedRDSEvaluate(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsEvaluate.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractEvaluator__eventParam = self.__eventParam
        self._CheckRDSOwnerTagValuesEvaluate__applicableResources = [APPLICABLE_RESOURCE_TYPE]
        rdsClient.list_tags_for_resource = MagicMock(return_value=self.__mockTagResponse) 
        rdsClient.remove_tags_from_resource = MagicMock(return_value=self.__mockTagResponse) 
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[2])
        evaluationResult = self.__checkRdsRequiredEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

    @mock_rds
    def testNonApplicableRDSEvaluate(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsEvaluate.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractEvaluator__eventParam = self.__eventParam
        self._CheckRDSOwnerTagValuesEvaluate__applicableResources = [APPLICABLE_RESOURCE_TYPE]
        rdsClient.list_tags_for_resource = MagicMock(return_value=self.__mockTagResponse) 
        rdsClient.remove_tags_from_resource = MagicMock(return_value=self.__mockTagResponse) 
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=NOT_APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        evaluationResult = self.__checkRdsRequiredEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
    
    @mock_rds
    def testNonApplicableRDSClusterInstancesEvaluate(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsEvaluate.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractEvaluator__eventParam = self.__eventParam
        self._CheckRDSOwnerTagValuesEvaluate__applicableResources = [APPLICABLE_RESOURCE_TYPE]
        rdsClient.list_tags_for_resource = MagicMock(return_value=self.__mockTagResponse) 
        rdsClient.remove_tags_from_resource = MagicMock(return_value=self.__mockTagResponse) 
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[3])
        evaluationResult = self.__checkRdsRequiredEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

    @mock_rds
    def testValidRequiredTagsRDSEvaluate(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsEvaluate.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractEvaluator__eventParam = self.__eventParam
        rdsClient.list_tags_for_resource = MagicMock(return_value=self.__mockTagResponse) 
        rdsClient.remove_tags_from_resource = MagicMock(return_value=self.__mockTagResponse) 
        self._CheckRDSOwnerTagValuesEvaluate__applicableResources = [APPLICABLE_RESOURCE_TYPE]
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        evaluationResult = self.__checkRdsRequiredEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

