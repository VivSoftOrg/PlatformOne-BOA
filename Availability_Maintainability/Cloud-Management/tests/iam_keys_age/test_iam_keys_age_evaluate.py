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
import boto3
import iam_keys_age.iam_keys_age_evaluate as iamKeysEvaluate
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.abstract_evaluate import *
from common.common_constants import *
from common.boto_utility import *
from mock import MagicMock
from moto import mock_iam
import datetime
from dateutil.tz import tzutc
from dateutil.relativedelta import relativedelta

EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-08-21T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
    "ruleParameters": "{ \"deleteAfterValidForDays\": \"5\",\"notifyBeforeValidForDays\": \"2\",\"iamKeyValidForDays\": \"90\",\"performAction\": \"True\",\"notifier\": \"sns\",\"toEmail\": \"ankush.tehele@reancloud.com\"}",
    "resultToken": "",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-zgvfqq",
    "configRuleName": "gaurav-test",
    "configRuleId": "config-rule-zgvfqq",
    "accountId": "107339370656"
}

CONTEXT = ""

RESOURCE_ID = "TESTUSERRANDOMID"
APPLICABLE_RESOURCE_TYPE = AWSResourceClassConstants.IAM_RESOURCE
NOT_APPLICABLE_RESOURCE_TYPE = AWSResourceClassConstants.EC2_INSTANCE

CONFIG_ITEMS = [
{'CreateDate': datetime.datetime.now(tz=tzutc()) - relativedelta(days=90),
 'AccessKeyId': 'AKIAJA6PEGVJE6S6CUZQ', 'Status': 'Active', 'username': 'ankush.tehele'
},
{'CreateDate': datetime.datetime.now(tz=tzutc()) - relativedelta(days=84),
 'AccessKeyId': 'AKIAIBQPCKYNXZOFZS7Q', 'Status': 'Active', 'username': 'paras.mishra'
},
{'CreateDate': datetime.datetime.now(tz=tzutc()) - relativedelta(days=93),
 'AccessKeyId': 'AKIAIBQPCKYNXZOFZS7Q', 'Status': 'Active', 'username': 'paras.mishra'
},
{'CreateDate': datetime.datetime.now(tz=tzutc()) - relativedelta(days=97),
 'AccessKeyId': 'AKIAIBQPCKYNXZOFZS7Q', 'Status': 'Active', 'username': 'paras.mishra'
},
{'CreateDate': datetime.datetime.now(tz=tzutc()) - relativedelta(days=97),
 'AccessKeyId': 'AKIAIBQPCKYNXZOFZS7Q', 'username': 'paras.mishra'
}
]


class TestIamKeysAgeEvaluate(object):
    __regions = ['us-east-1']
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __iamKeysAgeEvaluate = iamKeysEvaluate.IamKeysAgeEvaluate(__eventParam)

    # Test result will vary as per date you run it. Set the date in CONFIG_ITEMS above
    @mock_iam
    def testCompliantResourceEvaluate(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[1])
        evaluationResult = self.__iamKeysAgeEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_iam
    def testNonCompliantResourceEvaluate(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        evaluationResult = self.__iamKeysAgeEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_iam
    def testNonCompliantAboutToExpireResourceEvaluate(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[2])
        evaluationResult = self.__iamKeysAgeEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_iam
    def testNonCompliantExpiredDisabledResourceEvaluate(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[3])
        evaluationResult = self.__iamKeysAgeEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_iam
    def testNonApplicableResourceEvaluate(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=NOT_APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[0])
        evaluationResult = self.__iamKeysAgeEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

    @mock_iam
    def testNonApplicableResourceException(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=APPLICABLE_RESOURCE_TYPE, configItems=CONFIG_ITEMS[4])
        evaluationResult = self.__iamKeysAgeEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
