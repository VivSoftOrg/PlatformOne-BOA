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
import iam_keys_age.iam_keys_age_action as iamKeysAction
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import AWSResourceClassConstants, ComplianceConstants
from common.boto_utility import *
from mock import MagicMock
from common.abstract_action import *
from moto import mock_iam
import datetime
from dateutil.tz import tzutc
from dateutil.relativedelta import relativedelta

EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-08-21T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
    "ruleParameters": "{ \"deleteAfterValidForDays\": \"5\",\"notifyBeforeValidForDays\": \"2\",\"iamKeyValidForDays\": \"90\",\"performAction\": \"True\",\"notifier\": \"sns\",\"toEmail\": \"ankush.tehele@reancloud.com\"}",
    "resultToken": "",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-zgvfqq",
    "configRuleName": "gaurav-test",
    "configRuleId": "config-rule-zgvfqq",
    "accountId": "107339370656"
}

CONTEXT = ""

RESOURCE_ID = "TESTUSERRANDOMID"

CONFIG_ITEMS = [
{ 'keyAge':90, "NON_COMPLAINT_RESOURCE_ACTION": "disable", "Status": "Inactive",
 'CreateDate': datetime.datetime.now(tz=tzutc()) - relativedelta(days=90),
 'AccessKeyId': 'AKIAJA6PEGVJE6S6CUZQ', 'UserName': 'ankush.tehele'
},
{'NON_COMPLAINT_RESOURCE_ACTION': 'disable', 'Status': 'Active',
 'CreateDate': datetime.datetime.now(tz=tzutc()) - relativedelta(days=90),
 'AccessKeyId': 'AKIAIBQPCKYNXZOFZS7Q', 'Status': 'Active', 'UserName': 'paras.mishra'
},
{'NON_COMPLAINT_RESOURCE_ACTION': 'delete', 'Status': 'Active',
 'CreateDate': datetime.datetime.now(tz=tzutc()) - relativedelta(days=97),
 'AccessKeyId': 'AKIAIBQPCKYNXZOFZS7Q', 'Status': 'Active', 'UserName': 'paras.mishra'
},
{'NON_COMPLAINT_RESOURCE_ACTION': 'disableNotification', 'Status': 'Active',
 'CreateDate': datetime.datetime.now(tz=tzutc()) - relativedelta(days=87),
 'AccessKeyId': 'AKIAIBQPCKYNXZOFZS7Q', 'Status': 'Active', 'UserName': 'paras.mishra'
}
]

APPLICABLE_RESOURCE_TYPE=AWSResourceClassConstants.IAM_RESOURCE

class TestIamKeysAgeAction(object):
    __regions = ['us-east-1']
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __iamKeysAgeAction = iamKeysAction.IamKeysAgeAction(__eventParam)

    def getIamClient(self):
        iamClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_IAM, region_name=self.__regions[0])
        return iamClient

    __mockHttpResponseFail = {'ResponseMetadata': {'HTTPStatusCode': 500, 'RetryAttempts': 0}}
    __mockHttpResponseSuccess = {'ResponseMetadata': {'HTTPStatusCode': 200, 'RetryAttempts': 0}}

    @mock_iam
    def testDisableActionForInactiveKey(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        iamClient = self.getIamClient()
        iamKeysAction.BotoUtility.getClient = MagicMock(return_value=iamClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        iamClient.update_access_key = MagicMock(return_value=self.__mockHttpResponseSuccess)
        actionResponse = self.__iamKeysAgeAction.performAction(eventItem)
        assert actionResponse.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_iam
    def testDisableActionForActiveKey(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        iamClient = self.getIamClient()
        iamKeysAction.BotoUtility.getClient = MagicMock(return_value=iamClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[1])
        iamClient.update_access_key = MagicMock(return_value=self.__mockHttpResponseSuccess)
        actionResponse = self.__iamKeysAgeAction.performAction(eventItem)
        assert actionResponse.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_iam
    def testDeleteActionForAccessKey(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        iamClient = self.getIamClient()
        iamKeysAction.BotoUtility.getClient = MagicMock(return_value=iamClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[2])
        iamClient.update_access_key = MagicMock(return_value=self.__mockHttpResponseSuccess)
        iamClient.delete_access_key = MagicMock(return_value=self.__mockHttpResponseSuccess)
        actionResponse = self.__iamKeysAgeAction.performAction(eventItem)
        assert actionResponse.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_iam
    def testDeleteActionFailedAccessKey(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        iamClient = self.getIamClient()
        iamKeysAction.BotoUtility.getClient = MagicMock(return_value=iamClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[2])
        iamClient.update_access_key = MagicMock(return_value=self.__mockHttpResponseSuccess)
        iamClient.delete_access_key = MagicMock(return_value=self.__mockHttpResponseFail)
        actionResponse = self.__iamKeysAgeAction.performAction(eventItem)
        assert actionResponse.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE


    @mock_iam
    def testNotificationActionForAccessKey(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        iamClient = self.getIamClient()
        iamKeysAction.BotoUtility.getClient = MagicMock(return_value=iamClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[3])
        iamClient.update_access_key = MagicMock(return_value=self.__mockHttpResponseSuccess)
        iamClient.delete_access_key = MagicMock(return_value=self.__mockHttpResponseSuccess)
        actionResponse = self.__iamKeysAgeAction.performAction(eventItem)
        assert actionResponse.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_iam
    def testExcetionInDeleteAccessKey(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        iamClient = self.getIamClient()
        iamKeysAction.BotoUtility.getClient = MagicMock(return_value=iamClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[2])
        iamClient.update_access_key = MagicMock(return_value=self.__mockHttpResponseSuccess)
        iamClient.delete_access_key = MagicMock(side_effect=Exception("Mock Exception: failed to delete key"))
        actionResponse = self.__iamKeysAgeAction.performAction(eventItem)
        assert actionResponse.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION
