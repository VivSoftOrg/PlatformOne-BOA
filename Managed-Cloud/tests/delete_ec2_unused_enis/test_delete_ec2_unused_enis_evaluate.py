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
import sys
sys.path.append('../../')

import delete_ec2_unused_enis.delete_ec2_unused_enis_evaluate as unusedENIs
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.abstract_evaluate import *
from common.common_constants import *
from common.boto_utility import *
from mock import MagicMock
from moto import mock_ec2



RESOURCE_ID = {"ENI_IN_USE": "eni-in_use", "ENI_AVAILABLE": "eni-available"}
RESOURCE_TYPE = AWSResourceClassConstants.ENI_RESOURCE
CONFIG_ITEMS = [{"status": "in-use"}, {"status": "available"}]

EVENT_JSON = {
      "configRuleId": "config-rule-1v52mx",
      "version": "1.0",
      "configRuleName": "aws-sample-rule",
      "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-1v52mx",
      "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
      "resultToken": "",
      "ruleParameters": "{\"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
      "eventLeftScope": "False",
      "executionRoleArn": "arn:aws:iam::107339370656:role/awsconfig-role",
      "accountId": "107339370656"
}

CONTEXT = ""


class TestUnusedNetworkInterfacesEvaluate(object):

    __awsRegion = "us-east-1"

    @mock_ec2
    def testEvaluateForInUseNetworkInterfaces(self):
        self._AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        unusedENIsReference = unusedENIs.DeleteEC2UnusedENIsEvaluate(self._AbstractEvaluator__eventParam)
        unusedENIsReference.__applicableResources = [AWSResourceClassConstants.ENI_RESOURCE]
        evaluationResult = unusedENIsReference.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_ec2
    def testEvaluateForAvailableNetworkInterfaces(self):
        self._AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS[1])
        unusedENIsReference = unusedENIs.DeleteEC2UnusedENIsEvaluate(self._AbstractEvaluator__eventParam)
        unusedENIsReference.__applicableResources = [AWSResourceClassConstants.ENI_RESOURCE]
        evaluationResult = unusedENIsReference.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
