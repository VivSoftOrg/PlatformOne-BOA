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
from mock import MagicMock
from moto import mock_iam
from datetime import datetime, timedelta

sys.path.append('../../')

from enforce_allow_deny_groups_to_iam_users.enforce_allow_deny_groups_to_iam_users_evaluate import *
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import AWSResourceClassConstants
from common.abstract_evaluate import *
from common.common_utility import *
from common.boto_utility import *
from dateutil.tz import tzutc

EVENT_JSON = {
  "configRuleId": "config-rule-1v52mx",
  "version": "1.0",
  "configRuleName": "enforce_allow_deny_groups_to_iam_users",
  "configRuleArn": "arn:aws:config:us-east-1:693265998683:config-rule/config-rule-1v52mx",
  "invokingEvent": "{\n  \"configurationItemDiff\": null,\n   \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
  "resultToken": "",
  "ruleParameters": "{\"performAction\": \"True\", \"groupsName\": \"DenyGroupName, AllowGroupName\", \"excludeUsers\": \"\", \"actionName\": \"EnforceAllowAndDenyGroupsAction\", \"evaluateName\": \"EnforceAllowAndDenyGroupsEvaluate\",   \"resourceFetcherName\" : \"EnforceAllowAndDenyGroupsResourceFetcher\",  \"moduleName\": \"enforce_allow_deny_groups_to_iam_users\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\"}",
  "eventLeftScope": "False",
  "executionRoleArn": "arn:aws:iam::693265998683:role/awsconfig-role",
  "accountId": "693265998683"
}

CONTEXT = ""
RESOURCE_TYPE = AWSResourceClassConstants.IAM_RESOURCE
RESOURCE_ID = ''

class TestEnforceAllowAndDenyGroupsEvaluate(object):

    _AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __CONFIG_ITEM = {
                "PasswordLastUsed": datetime.now(tzutc()) - timedelta(days=11),
                "UserId": "AIDAJH2KUE4BMWFYD3BNK",
                "UserName": "devendra.suthar"
            }

    __enforceDefaultGroupdEvaluate = EnforceAllowAndDenyGroupsEvaluate(_AbstractEvaluator__eventParam)

    __today = datetime.now(tzutc())

    @mock_iam
    def testEvaluateIamUserNotAddedToAllowGroup(self):
        iamClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_IAM)
        BotoUtility.getClient = MagicMock(return_value=iamClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CommonUtility.changeDictionaryKeysToLowerCase(self.__CONFIG_ITEM))
        mockResponse = {
            IamConstants.IAM_USER_GROUPS: [
                {IamConstants.IAM_GROUP_NAME: "DenyGroupName"}
            ]
        }
        iamClient.list_groups_for_user = MagicMock(return_value = mockResponse)
        self.__enforceDefaultGroupdEvaluate._EnforceAllowAndDenyGroupsEvaluate__getAccessKeysLastUsedDate = MagicMock(return_value =  self.__today - timedelta(days = 14))
        self.__enforceDefaultGroupdEvaluate._EnforceAllowAndDenyGroupsEvaluate__userHasLoginProfile = MagicMock(return_value = True)
        evaluationResult = self.__enforceDefaultGroupdEvaluate.evaluate(eventItem)
        LoggerUtility.logError(eventItem.configItems)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateIamUserNotAddedToDenyGroup(self):
        iamClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_IAM)
        BotoUtility.getClient = MagicMock(return_value=iamClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CommonUtility.changeDictionaryKeysToLowerCase(self.__CONFIG_ITEM))
        mockResponse = {
            IamConstants.IAM_USER_GROUPS: [
                {IamConstants.IAM_GROUP_NAME: "AllowGroupName"}
            ]
        }
        iamClient.list_groups_for_user = MagicMock(return_value=mockResponse)
        self.__enforceDefaultGroupdEvaluate._EnforceAllowAndDenyGroupsEvaluate__getAccessKeysLastUsedDate = MagicMock(return_value=self.__today - timedelta(days=14))
        self.__enforceDefaultGroupdEvaluate._EnforceAllowAndDenyGroupsEvaluate__userHasLoginProfile = MagicMock(return_value=True)
        evaluationResult = self.__enforceDefaultGroupdEvaluate.evaluate(eventItem)
        LoggerUtility.logError(eventItem.configItems)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForIamUserNotAddedToAnyGroup(self):
        iamClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_IAM)
        BotoUtility.getClient = MagicMock(return_value=iamClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CommonUtility.changeDictionaryKeysToLowerCase(self.__CONFIG_ITEM))
        mockResponse = {
            IamConstants.IAM_USER_GROUPS: [
                {IamConstants.IAM_GROUP_NAME: "someOtherGroup"}
            ]
        }
        iamClient.list_groups_for_user = MagicMock(return_value=mockResponse)
        self.__enforceDefaultGroupdEvaluate._EnforceAllowAndDenyGroupsEvaluate__getAccessKeysLastUsedDate = MagicMock(return_value=self.__today - timedelta(days=14))
        self.__enforceDefaultGroupdEvaluate._EnforceAllowAndDenyGroupsEvaluate__userHasLoginProfile = MagicMock(return_value=True)
        evaluationResult = self.__enforceDefaultGroupdEvaluate.evaluate(eventItem)
        LoggerUtility.logError(eventItem.configItems)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForIamUserAddedToBothGroups(self):
        iamClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_IAM)
        BotoUtility.getClient = MagicMock(return_value=iamClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CommonUtility.changeDictionaryKeysToLowerCase(self.__CONFIG_ITEM))
        mockResponse = {
            IamConstants.IAM_USER_GROUPS: [
                {IamConstants.IAM_GROUP_NAME: "DenyGroupName"},
                {IamConstants.IAM_GROUP_NAME: "AllowGroupName"}
            ]
        }
        iamClient.list_groups_for_user = MagicMock(return_value=mockResponse)
        self.__enforceDefaultGroupdEvaluate._EnforceAllowAndDenyGroupsEvaluate__getAccessKeysLastUsedDate = MagicMock(return_value=self.__today - timedelta(days=14))
        self.__enforceDefaultGroupdEvaluate._EnforceAllowAndDenyGroupsEvaluate__userHasLoginProfile = MagicMock(return_value=True)
        evaluationResult = self.__enforceDefaultGroupdEvaluate.evaluate(eventItem)
        LoggerUtility.logError(eventItem.configItems)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE
