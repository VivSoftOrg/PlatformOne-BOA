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
""" This module is used for mock testing of rule evaluator class. """
import sys
import datetime
import common.compliance_object_factory as complianceobjectfactory
from common.common_constants import AWSResourceClassConstants, ComplianceConstants
from common.compliance_object_factory import ComplianceObjectFactory
from cloudfront_distribution_expiration.cloudfront_distribution_expiration_evaluate import CloudFrontDistributionEvaluate
from cloudfront_distribution_expiration.cloudfront_distribution_expiration_constants import Constants
from tests.cloudfront_distribution_expiration.test_cloudfront_expiration_placebo_initializer import PlaceboMockResponseInitializer
sys.path.append('../../')


EVENT_JSON = {
    "configRuleId": "config-rule-1v52mx",
    "version": "1.0",
    "configRuleName": "aws-sample-rule",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-1v52mx",
    "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"notificationCreationTime\": \"2018-05-19T08:40:15.976Z\",\n  \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
    "resultToken": "",
    "ruleParameters": "{\"validity\": \"10\", \n \"expirationDateLimit\": \"20\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/awsconfig-role",
    "accountId": "107339370656"}


CONTEXT = ""
RESOURCE_TYPE = AWSResourceClassConstants.CLOUDFRONT_DISTRIBUTION
RESOURCE_ID = 'DistributionName'


class TestCloudFrontExpirationEvaluate(object):
    """ This class is used for mock testing of rule evaluator class. """

    _AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __resourceConfig = {
        'ARN': '*****',
        'action': '',
        'region': 'us-east-1',
        'DistributionType': Constants.WEB_DISTRIBUTION_TYPE_REFERENCE,
        'ConfigType': Constants.WEB_DISTRIBUTION_CONFIG_REFERENCE,
        'WaiterType': Constants.WEB_DISTRIBUTION_WAITER_TYPE,
        'ListFunction': Constants.WEB_DISTRIBUTION_LIST_FUNCTION,
        'GetConfigFunction': Constants.WEB_DISTRIBUTION_GET_CONFIG_FUNCTION,
        'UpdateFunction': Constants.WEB_DISTRIBUTION_UPDATE_FUNCTION,
        'DeleteFunction': Constants.WEB_DISTRIBUTION_DELETE_FUNCTION}

    __eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems={})
    __distributionEvaluator = CloudFrontDistributionEvaluate(_AbstractEvaluator__eventParam)

    # NOTE:- Tested on 2018-10-19. So all date.today() calls will be using this date
    def testEvaluateForDistributionWithDaysRemaining(self):
        """ This method will Evaluate For Distribution With Days Remaining. """
        configItem = {'Tags': [
            {
                'Key': 'ExpirationDate',
                'Value': '{}'.format(datetime.datetime.today().date() + datetime.timedelta(days=10))
            }
        ]}
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__distributionEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testEvaluateForDistributionDateExceeded(self):
        """ This method will Evaluate For Distribution Date Exceeded. """
        configItem = {'Tags': [
            {
                'Key': 'ExpirationDate',
                'Value': '{}'.format(datetime.datetime.today().date() + datetime.timedelta(days=21))
            }
        ]}
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__distributionEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForDistributionAboutToExpireBoundaryCondition1(self):
        """ This method will Evaluate For Distribution About To Expire Boundary Condition 1. """
        configItem = {'Tags': [
            {
                'Key': 'ExpirationDate',
                'Value': '{}'.format(datetime.datetime.today().date() + datetime.timedelta(days=2))
            }
        ]}
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__distributionEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForDistributionAboutToExpireBoundaryCondition2(self):
        """ This method will Evaluate For Distribution About To Expire Boundary Condition 2. """
        configItem = {'Tags': [
            {
                'Key': 'ExpirationDate',
                'Value': '{}'.format(datetime.datetime.today().date() + datetime.timedelta(days=3))
            }
        ]}
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__distributionEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForDistributionExpiredButEnabled(self):
        """ This method will Evaluate For Distribution Expired But Enabled. """
        recordedMockResponsePath = PlaceboMockResponseInitializer.getEvaluatorMock('distribution_enabled')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)

        self.__resourceConfig.update({'Tags': [{
            'Key': 'ExpirationDate',
            'Value': '{}'.format(datetime.datetime.today().date() + datetime.timedelta(days=-2))}]})

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__resourceConfig)
        evaluationResult = self.__distributionEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForDistributionExpiredButDisabled(self):
        """ This method will Evaluate For Distribution Expired But Disabled. """
        recordedMockResponsePath = PlaceboMockResponseInitializer.getEvaluatorMock('distribution_disabled')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)

        self.__resourceConfig.update({'Tags': [
            {
                'Key': 'ExpirationDate',
                'Value': '{}'.format(datetime.datetime.today().date() + datetime.timedelta(days=2))}], 'Status': 'Deployed'})

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__resourceConfig)
        evaluationResult = self.__distributionEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForDistributionExpiredButNotDeployed(self):
        """ This method will Evaluate For Distribution Expired But Not Deployed. """
        recordedMockResponsePath = PlaceboMockResponseInitializer.getEvaluatorMock('distribution_not_deployed')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)

        self.__resourceConfig.update({'Tags': [{
            'Key': 'ExpirationDate',
            'Value': '{}'.format(datetime.datetime.today().date() + datetime.timedelta(days=2))}], 'Status': 'InProgress'})

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__resourceConfig)
        evaluationResult = self.__distributionEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForDistributionTagNotFound(self):
        """ This method will Evaluate For Distribution Tag Not Found. """
        configItem = {'Tags': []}
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItem)
        evaluationResult = self.__distributionEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
