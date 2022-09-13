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
sys.path.append('../../')
from active_iam_users.active_iam_users_evaluate import *
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import *
from common.abstract_evaluate import *
from common.common_utility import *
from common.boto_utility import *
from datetime import datetime, timedelta
from dateutil.tz import tzutc
from mock import MagicMock

EVENT_JSON = {
  "configRuleId": "config-rule-1v52mx",
  "version": "1.0",
  "configRuleName": "active_iam_users",
  "configRuleArn": "arn:aws:config:us-east-1:693265998683:config-rule/config-rule-1v52mx",
  "invokingEvent": "{\n  \"configurationItemDiff\": null,\n   \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
  "resultToken": "",
  "ruleParameters": "{\"performAction\": \"False\", \"lastActivityValidity\": \"10\", \"deleteWarnings\": \"10\", \"disableWarnings\": \"10\", \"actionName\": \"ActiveIamUsersAction\", \"evaluateName\": \"ActiveIamUsersEvaluate\",   \"resourceFetcherName\" : \"ActiveIamUsersResourceFetcher\",  \"moduleName\": \"atice_iam_users\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\"}",
  "eventLeftScope": "False",
  "executionRoleArn": "arn:aws:iam::693265998683:role/awsconfig-role",
  "accountId": "693265998683"
}

CONTEXT = ""
RESOURCE_TYPE = AWSResourceClassConstants.IAM_RESOURCE
RESOURCE_ID = ''

class TestActiveIamUsersEvaluate(object):

    _AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __USER_ABOUT_TO_DISABLE = {
                "CreateDate": datetime(2017, 11, 20, tzinfo=tzutc()),
                "PasswordLastUsed": datetime.now(tzutc()) - timedelta(days=11),
                "UserId": "AIDAJH2KUE4BMWFYD3BNK",
                "UserName": "devendra.suthar"
            }

    __USER_ABOUT_TO_DELETE = {
                "CreateDate": datetime(2017, 11, 20, tzinfo=tzutc()),
                "PasswordLastUsed": datetime.now(tzutc()) - timedelta(days=21),
                "UserId": "AIDAJH2KUE4BMWFYD3BNK",
                "UserName": "devendra.suthar"
            }
    __USER_EXPIRED = {
                "CreateDate": datetime(2017, 11, 20, tzinfo=tzutc()),
                "PasswordLastUsed": datetime.now(tzutc()) - timedelta(days=31),
                "UserId": "AIDAJH2KUE4BMWFYD3BNK",
                "UserName": "devendra.suthar"
            }

    __USER_SAFE = {
                "CreateDate": datetime(2017, 11, 20, tzinfo=tzutc()),
                "PasswordLastUsed": datetime.now(tzutc()) - timedelta(days=3),
                "UserId": "AIDAJH2KUE4BMWFYD3BNK",
                "UserName": "devendra.suthar"
    }

    __USER_WITHOUT_CONSOLE_ACCESS = {
                "CreateDate": datetime(2017, 11, 20, tzinfo=tzutc()),
                "UserId": "AIDAJH2KUE4BMWFYD3BNK",
                "UserName": "devendra.suthar"
    }
    __activeIamUsersEvaluator = ActiveIamUsersEvaluate(_AbstractEvaluator__eventParam)

    __today = datetime.now(tzutc())

    def testEvaluateIamUserDisable(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CommonUtility.changeDictionaryKeysToLowerCase(self.__USER_ABOUT_TO_DISABLE))
        self.__activeIamUsersEvaluator._ActiveIamUsersEvaluate__getAccessKeysLastUsedDate = MagicMock(return_value =  self.__today - timedelta(days = 14))
        self.__activeIamUsersEvaluator._ActiveIamUsersEvaluate__userHasLoginProfile = MagicMock(return_value = True)
        evaluationResult = self.__activeIamUsersEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateIamUserDelete(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CommonUtility.changeDictionaryKeysToLowerCase(self.__USER_ABOUT_TO_DELETE))
        self.__activeIamUsersEvaluator._ActiveIamUsersEvaluate__getAccessKeysLastUsedDate = MagicMock(return_value=self.__today - timedelta(days=24))
        self.__activeIamUsersEvaluator._ActiveIamUsersEvaluate__userHasLoginProfile = MagicMock(return_value=True)
        evaluationResult = self.__activeIamUsersEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForIamUserExpired(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CommonUtility.changeDictionaryKeysToLowerCase(self.__USER_EXPIRED))
        self.__activeIamUsersEvaluator._ActiveIamUsersEvaluate__getAccessKeysLastUsedDate = MagicMock(return_value=self.__today - timedelta(days=34))
        self.__activeIamUsersEvaluator._ActiveIamUsersEvaluate__userHasLoginProfile = MagicMock(return_value=True)
        evaluationResult = self.__activeIamUsersEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForIamUserSafe(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CommonUtility.changeDictionaryKeysToLowerCase(self.__USER_SAFE))
        self.__activeIamUsersEvaluator._ActiveIamUsersEvaluate__getAccessKeysLastUsedDate = MagicMock(return_value=self.__today - timedelta(days=3))
        self.__activeIamUsersEvaluator._ActiveIamUsersEvaluate__userHasLoginProfile = MagicMock(return_value=True)
        evaluationResult = self.__activeIamUsersEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testEvaluateForIamUserWithoutConsoleAccess(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CommonUtility.changeDictionaryKeysToLowerCase(self.__USER_WITHOUT_CONSOLE_ACCESS))
        self.__activeIamUsersEvaluator._ActiveIamUsersEvaluate__getAccessKeysLastUsedDate = MagicMock(return_value=self.__today - timedelta(days=30))
        self.__activeIamUsersEvaluator._ActiveIamUsersEvaluate__userHasLoginProfile = MagicMock(return_value=False)
        evaluationResult = self.__activeIamUsersEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluationException(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CommonUtility.changeDictionaryKeysToLowerCase(self.__USER_WITHOUT_CONSOLE_ACCESS))
        self.__activeIamUsersEvaluator._ActiveIamUsersEvaluate__getAccessKeysLastUsedDate = MagicMock(side_effect=Exception("TestException"))
        self.__activeIamUsersEvaluator._ActiveIamUsersEvaluate__userHasLoginProfile = MagicMock(return_value=False)
        evaluationResult = self.__activeIamUsersEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
