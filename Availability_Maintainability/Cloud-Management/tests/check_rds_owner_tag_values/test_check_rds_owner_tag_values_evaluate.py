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
import check_rds_owner_tag_values.check_rds_owner_tag_values_evaluate as rdsEvaluate
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
NOT_APPLICABLE_RESOURCE_TYPE = AWSResourceClassConstants.EC2_INSTANCE
 
__validTags = [ { "Key": "Owner", "Value": "ankush.tehele"} ]
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

iamUsers = {
    "Users": [
        {
            "UserName": "ankush.tehele", 
            "PasswordLastUsed": "2018-01-05T08:29:30Z", 
            "CreateDate": "2017-11-24T18:56:29Z", 
            "Path": "/", 
            "Arn": "arn:aws:iam::107339370656:user/ankush.tehele"
        }
    ]
}
 

class TestRDSOwnerTagEvaluate(object):
    __regions = ['us-east-1']
    __iamUsers = { "ValidIamUsers": ['ankush.tehele','thenmozhy.d'] }
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __mockTagResponse = { "TagList":[ { "Key": "Owner", "Value": "ankush.tehele"} ] }
    __mockTagResponseEmpty = { "TagList":[ ] }
    
    __checkRdsOwnerEvaluate = rdsEvaluate.CheckRDSOwnerTagValuesEvaluate(__eventParam) 
     
    @mock_rds
    def testNonValidOwnerRDSEvaluate(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsEvaluate.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractEvaluator__eventParam = self.__eventParam
        
        rdsClient.list_tags_for_resource = MagicMock(return_value=self.__mockTagResponseEmpty) 
        rdsClient.remove_tags_from_resource = MagicMock(return_value=self.__mockTagResponse) 
        self._CheckRDSOwnerTagValuesEvaluate__applicableResources = [APPLICABLE_RESOURCE_TYPE]
        iam = BotoUtility.getClient(
            BotoConstants.BOTO_CLIENT_AWS_IAM,
            self._AbstractEvaluator__eventParam.accNo,
            BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE
        )
        BotoUtility.getClient = MagicMock(return_value=iam)
        iam.list_users = MagicMock(return_value=iamUsers)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[1])
        evaluationResult = self.__checkRdsOwnerEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
    
    @mock_rds
    def testTerminatedRDSEvaluate(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsEvaluate.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractEvaluator__eventParam = self.__eventParam
        
        self._CheckRDSOwnerTagValuesEvaluate__applicableResources = [APPLICABLE_RESOURCE_TYPE]
        self._CheckRDSOwnerTagValuesEvaluate__getIamUsers = MagicMock(return_value=self.__iamUsers['ValidIamUsers'])
        rdsClient.list_tags_for_resource = MagicMock(return_value=self.__mockTagResponse) 
        rdsClient.remove_tags_from_resource = MagicMock(return_value=self.__mockTagResponse) 
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[2])
        evaluationResult = rdsEvaluate.CheckRDSOwnerTagValuesEvaluate.evaluate(self, eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

    def testNonApplicableRDSEvaluate(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsEvaluate.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractEvaluator__eventParam = self.__eventParam
        self._CheckRDSOwnerTagValuesEvaluate__applicableResources = [APPLICABLE_RESOURCE_TYPE]
        self._CheckRDSOwnerTagValuesEvaluate__getIamUsers = MagicMock(return_value=self.__iamUsers['ValidIamUsers'])
        rdsClient.list_tags_for_resource = MagicMock(return_value=self.__mockTagResponse) 
        rdsClient.remove_tags_from_resource = MagicMock(return_value=self.__mockTagResponse) 
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=NOT_APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        evaluationResult = rdsEvaluate.CheckRDSOwnerTagValuesEvaluate.evaluate(self,eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
    
    def testNonApplicableRDSClusterInstancesEvaluate(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsEvaluate.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractEvaluator__eventParam = self.__eventParam
        self._CheckRDSOwnerTagValuesEvaluate__applicableResources = [APPLICABLE_RESOURCE_TYPE]
        self._CheckRDSOwnerTagValuesEvaluate__getIamUsers = MagicMock(return_value=self.__iamUsers['ValidIamUsers'])
        rdsClient.list_tags_for_resource = MagicMock(return_value=self.__mockTagResponse) 
        rdsClient.remove_tags_from_resource = MagicMock(return_value=self.__mockTagResponse) 
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[3])
        evaluationResult = rdsEvaluate.CheckRDSOwnerTagValuesEvaluate.evaluate(self,eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

    @mock_rds
    def testValidOwnerRDSEvaluate(self):
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__regions[0])
        rdsEvaluate.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        self._AbstractEvaluator__eventParam = self.__eventParam
        rdsClient.list_tags_for_resource = MagicMock(return_value=self.__mockTagResponse) 
        rdsClient.remove_tags_from_resource = MagicMock(return_value=self.__mockTagResponse) 
        self._CheckRDSOwnerTagValuesEvaluate__applicableResources = [APPLICABLE_RESOURCE_TYPE]
        self._CheckRDSOwnerTagValuesEvaluate__getIamUsers = MagicMock(return_value=self.__iamUsers['ValidIamUsers'])
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        evaluationResult = rdsEvaluate.CheckRDSOwnerTagValuesEvaluate.evaluate(self, eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

