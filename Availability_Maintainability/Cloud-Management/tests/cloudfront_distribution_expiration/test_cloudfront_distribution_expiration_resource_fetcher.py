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
""" Test cases for cloudfront_distribution_expiration resource fetcher"""
import sys
import unittest
import common.compliance_object_factory as complianceobjectfactory
from cloudfront_distribution_expiration.cloudfront_distribution_expiration_resource_fetcher import CloudFrontDistributionResourceFetcher
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
    "accountId": "107339370656"
}

CONTEXT = ""


class TestCloudFrontExpirationFetcher(unittest.TestCase):
    """ Class fot test cases for cloudfront_distribution_expiration resource fetcher"""
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __distributionFetcher = CloudFrontDistributionResourceFetcher(__eventParam)

    def testWebDistributionResourceFetcher(self):
        """ test case for Web Distribution Resource Fetcher """
        recordedMockResponsePath = PlaceboMockResponseInitializer.getResourceFetcherMock('fetch_distributions')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__distributionFetcher.resourceFetcher()
        assert bool(return_value)

    def testResourceFetcherNoData(self):
        """ test  case Resource Fetcher No Data """
        recordedMockResponsePath = PlaceboMockResponseInitializer.getResourceFetcherMock('fetch_distributions_blank_response')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__distributionFetcher.resourceFetcher()
        assert not bool(return_value)
