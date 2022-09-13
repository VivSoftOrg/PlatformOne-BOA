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

from rules_common.aws_resource_utility.ec2_utility import Ec2Utility
from utility.placebo_utility import PlaceboMockResponseInitializer
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import ComplianceConstants
from common.framework_objects import EvaluationResult
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
RESOURCE_ID = "i-0cd2c09e799d7fb02"
RESOURCE_TYPE = "AWS::EC2::Instance"

CONFIG_ITEMS = {
    "resourceId": "i-01254789351",
    "Resource Name": "EC2 environement tag",
    "state": {
        "name": "running"
    },
    "blockdevicemappings": [
                            {
                                "devicename": "/dev/sda1",
                                "ebs": {
                                    "AttachTime": {
                                        "__class__": "datetime",
                                        "year": 2018,
                                        "month": 11,
                                        "day": 5,
                                        "hour": 4,
                                        "minute": 56,
                                        "second": 29,
                                        "microsecond": 0
                                    },
                                    "deleteontermination": "true",
                                    "status": "attached",
                                    "volumeid": "vol-0b4f7dda0edf65353"
                                }
                            }
                        ],
     "tags":{"RetentionPeriod" : "2018-11-01"}
}
CONFIG_ITEMS_NO_RETENTION_PERIOD_TAG = {
    "resourceId": "i-01254789351",
    "Resource Name": "EC2 environement tag",
    "state": {
        "name": "running"
    },
    "tags": {}
}


class TestEC2Utility(unittest.TestCase):

    __eventParam = ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    pill = PlaceboMockResponseInitializer(os.path.dirname(os.path.realpath(__file__)), 'ec2_utility')
    __ec2Utility = Ec2Utility(__eventParam)

    def testEc2UtilityResourceFetcher(self):
        self.pill.replaying_pill('fetcher/success')
        return_value = self.__ec2Utility.fetchResources()
        assert bool(return_value) == True

    def testEc2UtilityResourceFetcherNoData(self):
        self.pill.replaying_pill('fetcher/no_data')
        return_value = self.__ec2Utility.fetchResources()
        assert bool(return_value) == False

    def testEc2UtilityexecuteTagNonComplianceActionNoRetentionPeriodTag(self):
        self.evaluationResult = EvaluationResult()
        self.pill.replaying_pill('action/instance_termination_success')
        self.__eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS_NO_RETENTION_PERIOD_TAG)
        self.evaluationResult, self._AbstractAction__actionMessage = self.__ec2Utility.executeTagNonComplianceAction(self.evaluationResult, self.__eventItem)
        assert self.evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEc2UtilityexecuteTagNonComplianceActionNoRetentionPeriodTagFailure(self):
        self.evaluationResult = EvaluationResult()
        self.pill.replaying_pill('action/add_tag_failure')
        self.__eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS_NO_RETENTION_PERIOD_TAG)
        self.evaluationResult, self._AbstractAction__actionMessage = self.__ec2Utility.executeTagNonComplianceAction(self.evaluationResult, self.__eventItem)
        assert self.evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEc2UtilityexecuteTagNonComplianceActionSuccess(self):
        self.evaluationResult = EvaluationResult()
        self.pill.replaying_pill('action/instance_termination_success')
        self.__eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        self.evaluationResult, self._AbstractAction__actionMessage = self.__ec2Utility.executeTagNonComplianceAction(self.evaluationResult, self.__eventItem)
        assert self.evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testEc2UtilityexecuteTagNonComplianceActionFailureStageOne(self):
        self.evaluationResult = EvaluationResult()
        self.pill.replaying_pill('action/failure_stage_one')
        self.__eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        self.evaluationResult, self._AbstractAction__actionMessage = self.__ec2Utility.executeTagNonComplianceAction(self.evaluationResult, self.__eventItem)
        assert self.evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEc2UtilityexecuteTagNonComplianceActionExceptionStageOne(self):
        self.evaluationResult = EvaluationResult()
        self.pill.replaying_pill('action/exception_stage_one')
        self.__eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        self.evaluationResult, self._AbstractAction__actionMessage = self.__ec2Utility.executeTagNonComplianceAction(self.evaluationResult, self.__eventItem)
        assert self.evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    def testEc2UtilityexecuteTagNonComplianceActionFailureStageTwo(self):
        self.evaluationResult = EvaluationResult()
        self.pill.replaying_pill('action/failure_stage_two')
        self.__eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        self.evaluationResult, self._AbstractAction__actionMessage = self.__ec2Utility.executeTagNonComplianceAction(self.evaluationResult, self.__eventItem)
        assert self.evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEc2UtilityexecuteTagNonComplianceActionExceptionStageTwo(self):
        self.evaluationResult = EvaluationResult()
        self.pill.replaying_pill('action/exception_stage_two')
        self.__eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        self.evaluationResult, self._AbstractAction__actionMessage = self.__ec2Utility.executeTagNonComplianceAction(self.evaluationResult, self.__eventItem)
        assert self.evaluationResult.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    def testEc2UtilityRemoveTagsSuccess(self):
        self.pill.replaying_pill('remove_tags/success')
        return_value = self.__ec2Utility.removeInstanceTag("dummyInstance", "us-east-1", 'RetentionPeriod')
        assert bool(return_value) == True

    def testEc2UtilityRemoveTagsFailure(self):
        self.pill.replaying_pill('remove_tags/failure')
        return_value = self.__ec2Utility.removeInstanceTag("dummyInstance", "us-east-1", 'RetentionPeriod')
        assert bool(return_value) == False
