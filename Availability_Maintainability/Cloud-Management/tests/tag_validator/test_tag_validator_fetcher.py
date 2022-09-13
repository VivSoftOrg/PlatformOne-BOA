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

from tag_validator.tag_validator_resource_fetcher import TagValidatorResourceFetcher
from utility.placebo_utility import PlaceboMockResponseInitializer
from common.compliance_object_factory import ComplianceObjectFactory
import unittest
import os


EVENT_JSON = {
  "version": "1.0",
  "invokingEvent": "{\"awsAccountId\":\"693265998683\",\"notificationCreationTime\":\"2017-08-21T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
  "ruleParameters": "{\n  \"actionName\": \"TagValidatorAction\",\n  \"evaluateName\": \"TagValidatorEvaluate\",\n  \"resourceFetcherName\": \"TagValidatorResourceFetcher\",\n  \"toEmail\": \"devendra.suthar@hitachivantara.com\",\n  \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"RetentionPeriod\": \"2\",\n  \"tagKeysToCheck\": \"Owner, Environment, Name, Project, ExpirationDate\",\n  \"Environment\": \"Development, Testing\",\n  \"Owner\": \"IAM_USERS\",\n  \"performAction\": \"true\",\n  \"notifier\": \"email\"\n}",
  "resultToken": "V19fQ==",
  "eventLeftScope": "False",
  "executionRoleArn": "arn:aws:iam::693265998683:role/svc-rean-mnc-default-config-role",
  "configRuleArn": "arn:aws:config:us-east-1:693265998683:config-rule/config-rule-zgvfqq",
  "configRuleName": "tag_validator",
  "configRuleId": "config-rule-zgvfqq",
  "accountId": "693265998683"
}


CONTEXT = ""


class TestTagValidatorFetcher(unittest.TestCase):

    __eventParam = ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    pill = PlaceboMockResponseInitializer(os.path.dirname(os.path.realpath(__file__)), __eventParam.moduleName)
    __resourceFetcher = TagValidatorResourceFetcher(__eventParam)
    os.environ['monitoringResourcesTable'] = "dummyTable"

    def testTagValidatorResourceFetcher(self):
        self.pill.replaying_pill('fetcher/success')
        return_value = self.__resourceFetcher.resourceFetcher()
        assert bool(return_value) == True

    def testTagValidatorResourceFetcherNoData(self):
        self.pill.replaying_pill('fetcher/no_data')
        return_value = self.__resourceFetcher.resourceFetcher()
        assert bool(return_value) == False

    def testTagValidatorResourceFetcherException(self):
        self.pill.replaying_pill('fetcher/exception')
        return_value = self.__resourceFetcher.resourceFetcher()
        assert bool(return_value) == False
