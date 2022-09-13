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
from elasticsearch_service_expiration.elasticsearch_service_expiration_evaluate import *
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import AWSResourceClassConstants
import datetime
from common.abstract_evaluate import *
from common.boto_utility import *


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
RESOURCE_TYPE = AWSResourceClassConstants.ELASTICSEARCH_SERVICE
RESOURCE_ID = 'ElasticSearch Service Name'

class TestElasticSearchServiceEvaluate(object):

    _AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems={})

    __ESServiceEvaluator = ElasticSearchServiceEvaluate(_AbstractEvaluator__eventParam)

    __ResourceName = 'ElasticSearch Service'

    # NOTE:- Tested on 2017-12-11. So all date.today() calls will be using this date
    def testEvaluateForESServiceWithDaysRemaining(self):
        configItem = {
            'Resource Name': self.__ResourceName,
            'Tags': [
                {
                    'Key': 'ExpirationDate',
                    'Value': (datetime.datetime.today().date()+datetime.timedelta(days=11)).strftime('%Y-%m-%d')
                }],
            'Deleted': False
        }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__ESServiceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE
# (datetime.datetime.today().date()+datetime.timedelta(days=10)).strftime('%Y-%m-%d')
    def testEvaluateForESServiceDateExceeded(self):
        configItem = {'Tags': [
            {
                'Key': 'ExpirationDate',
                'Value': (datetime.datetime.today().date()+datetime.timedelta(days=18)).strftime('%Y-%m-%d')
            }],
                'Resource Name': 'ElasticSearch Service',
                'Deleted': False
            }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__ESServiceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testEvaluateForESServiceAboutToExpireBoundaryCondition1(self):
        configItem = {'Tags': [
            {
                'Key': 'ExpirationDate',
                'Value': (datetime.datetime.today().date()+datetime.timedelta(days=2)).strftime('%Y-%m-%d')
            }],
                'Resource Name': 'ElasticSearch Service',
                'Deleted': False
            }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__ESServiceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
        

    def testEvaluateForESServiceAboutToExpireBoundaryCondition2(self):
        configItem = {'Tags': [
            {
                'Key': 'ExpirationDate',
                'Value': (datetime.datetime.today().date()).strftime('%Y-%m-%d')
            }],
                'Resource Name': 'ElasticSearch Service',
                'Deleted': False
            }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__ESServiceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForESServiceExpired(self):
        configItem = {'Tags': [
                {
                    'Key': 'ExpirationDate',
                    'Value': (datetime.datetime.today().date()+datetime.timedelta(days=-40)).strftime('%Y-%m-%d')
                }
        ],
            'Resource Name': 'ElasticSearch Service',
            'Deleted': False
        }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__ESServiceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForESServiceInBeingDeletedState(self):
        configItem = {'Tags': [],
                      'Resource Name': 'ElasticSearch Service',
                    'Deleted': True}

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__ESServiceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testEvaluateForESServiceTagNotFound(self):
        configItem = {'Tags': [],
                      'Resource Name': 'ElasticSearch Service',
                      'Deleted': False
                      }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__ESServiceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
