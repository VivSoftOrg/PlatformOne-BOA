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
# from workspaces_expiration.workspaces_expiration_evaluate import *
import sys 
sys.path.append('../../')
import common.compliance_object_factory as complianceobjectfactory
from common.abstract_evaluate import *
from common.compliance_object_factory import ComplianceObjectFactory
from common.boto_utility import *
from common.common_constants import AWSResourceClassConstants
from delete_unused_ebs.delete_unused_ebs_evaluate import *
from datetime import datetime, timezone

EVENT_JSON = {
      "configRuleId": "config-rule-1v52mx",
      "version": "1.0",
      "configRuleName": "aws-sample-rule",
      "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-1v52mx",
      "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
      "resultToken": "",
      "ruleParameters": "{\"age\": \"0\", \n \"expirationDateLimit\": \"20\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
      "eventLeftScope": "False",
      "executionRoleArn": "arn:aws:iam::107339370656:role/awsconfig-role",
      "accountId": "107339370656"
}

CONTEXT = ""
RESOURCE_TYPE = AWSResourceClassConstants.EBS_VOLUME
RESOURCE_ID = 'VolumeId'

class TestDeleteUnusedEBSEvaluate(object):

    _AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems={})

    __unusedEbsEvaluator = DeleteUnusedEBSEvaluate(_AbstractEvaluator__eventParam)

    def testEvaluateForEBSVolumeDelete(self):
        configItem = {
            'createtime': datetime.now(timezone.utc),
            'region': 'us-east-1'
        }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__unusedEbsEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

