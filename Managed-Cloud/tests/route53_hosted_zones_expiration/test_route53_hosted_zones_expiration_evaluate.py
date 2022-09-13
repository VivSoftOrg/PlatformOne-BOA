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
from route53_hosted_zones_expiration.route53_hosted_zones_expiration_evaluate import *
import common.compliance_object_factory as complianceobjectfactory
from common.abstract_evaluate import *
from common.boto_utility import *
from common.common_constants import AWSResourceClassConstants
from common.compliance_object_factory import ComplianceObjectFactory
from datetime import datetime, timedelta

EVENT_JSON = {
    "configRuleId": "config-rule-1v52mx",
    "version": "1.0",
    "configRuleName": "aws-sample-rule",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-1v52mx",
    "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
    "resultToken": "",
    "ruleParameters": "{\"validity\": \"10\", \n \"expirationDateLimit\": \"20\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/awsconfig-role",
    "accountId": "107339370656"
}

CONTEXT = ""
RESOURCE_TYPE = AWSResourceClassConstants.WORKSPACES_RESOURCE
RESOURCE_ID = 'Route53 Hosted Zone'

class TestHostedZoneEvaluate(object):

    _AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems={})

    __hostedZoneEvaluator = HostedZoneExpirationEvaluate(_AbstractEvaluator__eventParam)

    __ResourceName = 'Route53 Hosted Zone'

    def testEvaluateForHostedZonesWithDaysRemaining(self):
        configItem = {
            'Resource Name': self.__ResourceName,
            'Tags': [
                {
                    'Key': 'ExpirationDate',
                    'Value': (datetime.now() + timedelta(days=15)).date().isoformat()
                }]
        }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__hostedZoneEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testEvaluateForHostedZonesDateExceeded(self):
        configItem = {'Tags': [
            {
                'Key': 'ExpirationDate',
                'Value': (datetime.now() + timedelta(days=35)).date().isoformat()
            }],
                'Resource Name': self.__ResourceName
            }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__hostedZoneEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForHostedZonesAboutToExpireBoundaryCondition1(self):
        configItem = {'Tags': [
            {
                'Key': 'ExpirationDate',
                'Value': (datetime.now() + timedelta(days=3)).date().isoformat()
            }],
                'Resource Name': self.__ResourceName
            }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__hostedZoneEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForHostedZonesAboutToExpireBoundaryCondition2(self):
        configItem = {'Tags': [
            {
                'Key': 'ExpirationDate',
                'Value': (datetime.now() + timedelta(days=2)).date().isoformat()
            }],
                'Resource Name': self.__ResourceName
            }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__hostedZoneEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForHostedZonesExpired(self):
        configItem = {'Tags': [
                {
                    'Key': 'ExpirationDate',
                    'Value': (datetime.now() + timedelta(days=-1)).date().isoformat()
                }
        ],
            'Resource Name': self.__ResourceName
        }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__hostedZoneEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE


    def testEvaluateForHostedZonesTagNotFound(self):
        configItem = {'Tags': [],
                      'Resource Name': self.__ResourceName
                      }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__hostedZoneEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
