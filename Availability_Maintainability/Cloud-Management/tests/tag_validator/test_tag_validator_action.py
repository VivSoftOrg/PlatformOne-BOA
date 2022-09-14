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

from tag_validator.tag_validator_action import TagValidatorAction
from common.compliance_object_factory import ComplianceObjectFactory
from utility.placebo_utility import PlaceboMockResponseInitializer
from common.common_constants import ComplianceConstants
from mock import MagicMock
import unittest
import os

EVENT_JSON = {
  "version": "1.0",
  "invokingEvent": "{\"awsAccountId\":\"693265998683\",\"notificationCreationTime\":\"2017-08-21T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
  "ruleParameters": "{\n  \"actionName\": \"TagValidatorAction\",\n  \"evaluateName\": \"TagValidatorEvaluate\",\n  \"resourceFetcherName\": \"TagValidatorResourceFetcher\",\n  \"toEmail\": \"devendra.suthar@hitachivantara.com\",\n  \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"RetentionPeriod\": \"2\",\n  \"tagKeysToCheck\": \"Owner, Environment, Name, Project, ExpirationDate\",\n  \"Environment\": \"Development, Testing\",\n  \"Owner\": \"rean\",\n  \"performAction\": \"true\",\n  \"notifier\": \"email\"\n}",
  "resultToken": "V19fQ==",
  "eventLeftScope": "False",
  "executionRoleArn": "arn:aws:iam::693265998683:role/svc-rean-mnc-default-config-role",
  "configRuleArn": "arn:aws:config:us-east-1:693265998683:config-rule/config-rule-zgvfqq",
  "configRuleName": "tag_validator",
  "configRuleId": "config-rule-zgvfqq",
  "accountId": "693265998683"
}

CONTEXT = ""
RESOURCE_ID = "i-0cd2c09e799d7fb02"
RESOURCE_TYPE = "AWS::EC2::Instance"

CONFIG_ITEMS_INVALID_TAGS = {
    "resourceId": "i-01254789351",
    "Resource Name": "EC2 environement tag",
    "state": {
        "name": "running"
    },
    "tags": [
        {
            "key": "Name",
            "value": "Test-Machine"
        },
        {
            "key": "ExpirationDate",
            "value": "expiration_date"
        },
        {
            "key": "Environment",
            "value": "Test"
        },
        {
            "key": "Owner",
            "value": "rean"
        }
    ]
}

class TestTagValidatorAction(unittest.TestCase):

    __eventParam = ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __eventItem = None
    __tagAction = TagValidatorAction(__eventParam)
    pill = PlaceboMockResponseInitializer(os.path.dirname(os.path.realpath(__file__)), __eventParam.moduleName)
    os.environ['monitoringResourcesTable'] = "dummyTable"

    # def testActionNotApplicable(self):
    #     """ This method test with the valid tags."""
    #     self.__eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS_INVALID_TAGS)
    #     self.pill.replaying_pill('action/success')
    #     self.__tagAction._TagValidator__getApplicableMonitoredResource = MagicMock(return_value=[RESOURCE_TYPE])
    #     evaluationResult = self.__tagAction.performAction(self.__eventItem)
    #     assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testActionException(self):
        """ This method test with the valid tags."""
        self.__eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS_INVALID_TAGS)
        evaluationResult = self.__tagAction.performAction(self.__eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    def testActionInsufficientData(self):
        """ This method test with the valid tags."""
        self.__eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS_INVALID_TAGS)
        self.pill.replaying_pill('action/insufficient_data')
        evaluationResult = self.__tagAction.performAction(self.__eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.INSUFFICIENT_RESOURCE_DATA