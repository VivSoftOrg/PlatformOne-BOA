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
from datetime import datetime, timedelta
from common.common_constants import AWSResourceClassConstants, EvaluationMessages
from workspaces_expiration.workspaces_expiration_evaluate import *
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
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
RESOURCE_TYPE = AWSResourceClassConstants.WORKSPACES_RESOURCE
RESOURCE_ID = 'WorkSpaceName'

class TestWorkSpacesEvaluate(object):

    _AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems={})

    __workSpaceEvaluator = WorkSpacesEvaluate(_AbstractEvaluator__eventParam)

    __ResourceName = 'WorkSpace'

    # NOTE:- Tested on 2017-10-29. So all date.today() calls will be using this date
    def testEvaluateForWorkSpaceWithDaysRemaining(self):
        configItem = {
            'Resource Name': self.__ResourceName,
            'Tags': [
                {
                    'Key': 'ExpirationDate',
                    'Value': (datetime.now() + timedelta(days=9)).date().isoformat()
                }],
            'State': 'AVAILABLE'
        }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__workSpaceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testEvaluateForWorkSpaceTerminating(self):
        configItem = {
            'Resource Name': self.__ResourceName,
            'Tags': [],
            'State': 'TERMINATING'
        }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__workSpaceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testEvaluateForWorkSpaceDateExceeded(self):
        configItem = {'Tags': [
            {
                'Key': 'ExpirationDate',
                'Value': (datetime.now() + timedelta(days=60)).date().isoformat()
            }],
                'Resource Name': self.__ResourceName,
                'State': 'AVAILABLE'
            }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__workSpaceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForWorkSpaceAboutToExpireBoundaryCondition1(self):
        configItem = {'Tags': [
            {
                'Key': 'ExpirationDate',
                'Value': (datetime.now() + timedelta(days=2)).date().isoformat()
            }],
                'Resource Name': self.__ResourceName,
                'State': 'AVAILABLE'
            }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__workSpaceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForWorkSpaceAboutToExpireBoundaryCondition2(self):
        configItem = {'Tags': [
            {
                'Key': 'ExpirationDate',
                'Value': (datetime.now() + timedelta(days=3)).date().isoformat()
            }],
                'Resource Name': self.__ResourceName,
                'State': 'AVAILABLE'
            }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__workSpaceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForWorkSpaceExpired(self):
        configItem = {'Tags': [
                {
                    'Key': 'ExpirationDate',
                    'Value': datetime.now().date().isoformat()
                }
        ],
            'Resource Name': self.__ResourceName,
            'State': 'AVAILABLE'
        }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__workSpaceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForWorkSpaceExpiredButSuspended(self):
        configItem = {'Tags': [
                    {
                        'Key': 'ExpirationDate',
                        'Value': datetime.now().date().isoformat()
                    }
                    ],
                    'Resource Name': self.__ResourceName,
                    'State': 'SUSPENDED'
        }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__workSpaceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForWorkSpaceTagNotFound(self):
        configItem = {'Tags': [],
                      'Resource Name': self.__ResourceName,
                      'State': 'AVAILABLE'
                      }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__workSpaceEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
