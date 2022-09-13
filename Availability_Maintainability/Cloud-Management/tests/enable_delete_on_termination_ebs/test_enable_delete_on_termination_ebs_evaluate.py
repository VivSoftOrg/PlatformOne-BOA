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

from enable_delete_on_termination_ebs.enable_delete_on_termination_ebs_evaluate import *
# from tests.enable_delete_on_termination_ebs.test_enable_delete_on_termination_ebs_placebo_initializer import *
import common.compliance_object_factory as complianceobjectfactory
from common.abstract_evaluate import *
from common.boto_utility import *

EVENT_JSON_DELETE_ON_TERMINATION_ENABLED = {
    "version": "1.0",
    "invokingEvent": "{\"configurationItemDiff\": null,\"configurationItem\": {\"configuration\": {\"state\": {\"code\": 80,\"name\": \"running\"},\"blockDeviceMappings\": [{\"deviceName\": \"/dev/xvda\",\"ebs\": {\"attachTime\": \"2017-12-28T06:44:33.000Z\",\"deleteOnTermination\": true,\"status\": \"attached\",\"volumeId\": \"vol-0363f54fc5e3d9906\"}}]},\"awsAccountId\": \"107339370656\",\"configurationItemStatus\": \"OK\",\"resourceType\": \"AWS::EC2::Instance\",\"resourceId\": \"i-05b8ba2c066f455ec\",\"resourceName\": null,\"ARN\": \"arn:aws:ec2:us-east-1:107339370656:instance/i-05b8ba2c066f455ec\",\"awsRegion\": \"us-east-1\",\"availabilityZone\": \"us-east-1a\",\"configurationStateMd5Hash\": \"baf6a69a8c9fbb6129d758c2acb84c56\",\"resourceCreationTime\": \"2018-01-02T08:47:25.000Z\"},\"notificationCreationTime\": \"2018-01-03T09:58:11.794Z\",\"messageType\": \"ConfigurationItemChangeNotification\",\"recordVersion\": \"1.2\"}",
    "ruleParameters": "{\n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
    "resultToken": "eyJlbmNyeXB0ZWREYXRhIjpbN",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-xbqpcp",
    "configRuleName": "testRule",
    "configRuleId": "config-rule-xbqpcp",
    "accountId": "107339370656"
}

EVENT_JSON_DELETE_ON_TERMINATION_NOT_ENABLED = {
    "version": "1.0",
    "invokingEvent": "{\"configurationItemDiff\": null,\"configurationItem\": {\"configuration\": {\"state\": {\"code\": 80,\"name\": \"running\"},\"blockDeviceMappings\": [{\"deviceName\": \"/dev/xvda\",\"ebs\": {\"attachTime\": \"2017-12-28T06:44:33.000Z\",\"deleteOnTermination\": false,\"status\": \"attached\",\"volumeId\": \"vol-0363f54fc5e3d9906\"}}]},\"awsAccountId\": \"107339370656\",\"configurationItemStatus\": \"OK\",\"resourceType\": \"AWS::EC2::Instance\",\"resourceId\": \"i-05b8ba2c066f455ec\",\"resourceName\": null,\"ARN\": \"arn:aws:ec2:us-east-1:107339370656:instance/i-05b8ba2c066f455ec\",\"awsRegion\": \"us-east-1\",\"availabilityZone\": \"us-east-1a\",\"configurationStateMd5Hash\": \"baf6a69a8c9fbb6129d758c2acb84c56\",\"resourceCreationTime\": \"2018-01-02T08:47:25.000Z\"},\"notificationCreationTime\": \"2018-01-03T09:58:11.794Z\",\"messageType\": \"ConfigurationItemChangeNotification\",\"recordVersion\": \"1.2\"}",
    "ruleParameters": "{\n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
    "resultToken": "eyJlbmNyeXB0ZWREYXRhIjpbN",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-xbqpcp",
    "configRuleName": "testRule",
    "configRuleId": "config-rule-xbqpcp",
    "accountId": "107339370656"
}

EVENT_JSON_TERMINATED_RESOURCE = {
    "version": "1.0",
    "invokingEvent": "{\"configurationItemDiff\": null,\"configurationItem\": {\"configuration\": {\"state\": {\"code\": 80,\"name\": \"terminated\"},\"blockDeviceMappings\": [{\"deviceName\": \"/dev/xvda\",\"ebs\": {\"attachTime\": \"2017-12-28T06:44:33.000Z\",\"deleteOnTermination\": false,\"status\": \"attached\",\"volumeId\": \"vol-0363f54fc5e3d9906\"}}]},\"awsAccountId\": \"107339370656\",\"configurationItemStatus\": \"OK\",\"resourceType\": \"AWS::EC2::Instance\",\"resourceId\": \"i-05b8ba2c066f455ec\",\"resourceName\": null,\"ARN\": \"arn:aws:ec2:us-east-1:107339370656:instance/i-05b8ba2c066f455ec\",\"awsRegion\": \"us-east-1\",\"availabilityZone\": \"us-east-1a\",\"configurationStateMd5Hash\": \"baf6a69a8c9fbb6129d758c2acb84c56\",\"resourceCreationTime\": \"2018-01-02T08:47:25.000Z\"},\"notificationCreationTime\": \"2018-01-03T09:58:11.794Z\",\"messageType\": \"ConfigurationItemChangeNotification\",\"recordVersion\": \"1.2\"}",
    "ruleParameters": "{\n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
    "resultToken": "eyJlbmNyeXB0ZWREYXRhIjpbN",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-xbqpcp",
    "configRuleName": "testRule",
    "configRuleId": "config-rule-xbqpcp",
    "accountId": "107339370656"
}

EVENT_JSON_RESOURCE_TYPE_NOT_APPLICABLE = {
    "version": "1.0",
    "invokingEvent": "{\"configurationItemDiff\": null,\"configurationItem\": {\"configuration\": {\"instanceType\": \"t2.micro\",\"blockDeviceMappings\": [{\"deviceName\": \"/dev/xvda\",\"ebs\": {\"attachTime\": \"2017-12-28T06:44:33.000Z\",\"deleteOnTermination\": true,\"status\": \"attached\",\"volumeId\": \"vol-0363f54fc5e3d9906\"}}]},\"resourceType\": \"AWS::EC2::Volume\",\"resourceId\": \"i-05b8ba2c066f455ec\",\"resourceName\": null,\"ARN\": \"arn:aws:ec2:us-east-1:107339370656:instance/i-05b8ba2c066f455ec\",\"awsRegion\": \"us-east-1\",\"availabilityZone\": \"us-east-1a\"},\"messageType\": \"ConfigurationItemChangeNotification\",\"recordVersion\": \"1.2\"}",
    "ruleParameters": "{\n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
    "resultToken": "eyJlbmNyeXB0ZWREYXRhIjpbN",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-xbqpcp",
    "configRuleName": "testRule",
    "configRuleId": "config-rule-xbqpcp",
    "accountId": "107339370656"
}

CONTEXT = ""

class TestEnableDeleteOnTerminationEBSEvaluate(object):

    def testEvaluateForDeleteOnTerrminationNotEnabled(self):
        self._AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON_DELETE_ON_TERMINATION_NOT_ENABLED,
            CONTEXT
        )
        eventItem = complianceobjectfactory.ComplianceObjectFactory.createEventItemFrom(EVENT_JSON_DELETE_ON_TERMINATION_NOT_ENABLED, CONTEXT, self._AbstractEvaluator__eventParam)
        self._EnableDeleteOnTerminationEBSEvaluate__applicableResources = [AWSResourceClassConstants.EC2_INSTANCE]
        evaluationResult = EnableDeleteOnTerminationEBSEvaluate.evaluate(self, eventItem[0])
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForDeleteOnTerrminationEnabled(self):
        self._AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON_DELETE_ON_TERMINATION_ENABLED,
            CONTEXT
        )
        eventItem = complianceobjectfactory.ComplianceObjectFactory.createEventItemFrom(EVENT_JSON_DELETE_ON_TERMINATION_ENABLED, CONTEXT, self._AbstractEvaluator__eventParam)
        self._EnableDeleteOnTerminationEBSEvaluate__applicableResources = [AWSResourceClassConstants.EC2_INSTANCE]
        evaluationResult = EnableDeleteOnTerminationEBSEvaluate.evaluate(self, eventItem[0])
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testEvaluateForResourceNotApplicable(self):
        self._AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON_RESOURCE_TYPE_NOT_APPLICABLE,
            CONTEXT
        )
        eventItem = complianceobjectfactory.ComplianceObjectFactory.createEventItemFrom(EVENT_JSON_RESOURCE_TYPE_NOT_APPLICABLE, CONTEXT, self._AbstractEvaluator__eventParam)
        self._EnableDeleteOnTerminationEBSEvaluate__applicableResources = [AWSResourceClassConstants.EC2_INSTANCE]
        evaluationResult = EnableDeleteOnTerminationEBSEvaluate.evaluate(self, eventItem[0])
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

    def testEvaluateForInstanceTerminated(self):
        self._AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON_TERMINATED_RESOURCE,
            CONTEXT
        )
        eventItem = complianceobjectfactory.ComplianceObjectFactory.createEventItemFrom(EVENT_JSON_TERMINATED_RESOURCE, CONTEXT, self._AbstractEvaluator__eventParam)
        self._EnableDeleteOnTerminationEBSEvaluate__applicableResources = [AWSResourceClassConstants.EC2_INSTANCE]
        evaluationResult = EnableDeleteOnTerminationEBSEvaluate.evaluate(self, eventItem[0])
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
