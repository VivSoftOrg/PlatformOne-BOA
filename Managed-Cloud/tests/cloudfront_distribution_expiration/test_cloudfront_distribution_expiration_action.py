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
""" Test cases for cloudfront_distribution_expiration action"""
import sys
import common.compliance_object_factory as complianceObjectFactory
from common.common_constants import AWSResourceClassConstants, ComplianceConstants, ResourceConstants
from common.compliance_object_factory import ComplianceObjectFactory
from cloudfront_distribution_expiration.cloudfront_distribution_expiration_action import CloudFrontDistributionAction
from cloudfront_distribution_expiration.cloudfront_distribution_expiration_constants import Constants
from tests.cloudfront_distribution_expiration.test_cloudfront_expiration_placebo_initializer import PlaceboMockResponseInitializer

sys.path.append('../../')


RESOURCE_ID = "DistributionName"
RESOURCE_TYPE = AWSResourceClassConstants.CLOUDFRONT_DISTRIBUTION

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

CONTEXT = ''


class TestCloudFrontDistributionAction:
    """ Test cases for cloudfront_distribution_expiration action class"""

    __StreamingConfig = {
        'ARN': '****',
        'action': '',
        'region': 'us-east-1',
        'DistributionType': Constants.STREAMING_DISTRIBUTION_TYPE_REFERENCE,
        'ConfigType': Constants.STREAMING_DISTRIBUTION_CONFIG_REFERENCE,
        'WaiterType': Constants.STREAMING_DISTRIBUTION_WAITER_TYPE,
        'ListFunction': Constants.STREAMING_DISTRIBUTION_LIST_FUNCTION,
        'GetConfigFunction': Constants.STREAMING_DISTRIBUTION_GET_CONFIG_FUNCTION,
        'UpdateFunction': Constants.STREAMING_DISTRIBUTION_UPDATE_FUNCTION,
        'DeleteFunction': Constants.STREAMING_DISTRIBUTION_DELETE_FUNCTION
    }

    __WebConfig = {
        'ARN': '*****',
        'action': '',
        'region': 'us-east-1',
        'DistributionType': Constants.WEB_DISTRIBUTION_TYPE_REFERENCE,
        'ConfigType': Constants.WEB_DISTRIBUTION_CONFIG_REFERENCE,
        'WaiterType': Constants.WEB_DISTRIBUTION_WAITER_TYPE,
        'ListFunction': Constants.WEB_DISTRIBUTION_LIST_FUNCTION,
        'GetConfigFunction': Constants.WEB_DISTRIBUTION_GET_CONFIG_FUNCTION,
        'UpdateFunction': Constants.WEB_DISTRIBUTION_UPDATE_FUNCTION,
        'DeleteFunction': Constants.WEB_DISTRIBUTION_DELETE_FUNCTION
    }

    _AbstractAction__eventParam = complianceObjectFactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __awsRegion = "us-east-1"

    __distributionAction = CloudFrontDistributionAction(_AbstractAction__eventParam)

    def testPerformActionAddExpirationTag(self):
        """ test Perform Action Add Expiration Tag """
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('add_tag/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)

        self.__StreamingConfig.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND})

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__StreamingConfig)
        return_value = self.__distributionAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testPerformActionAddExpirationTagFailure(self):
        """ test Perform Action Add Expiration Tag Failure """
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('add_tag/failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)

        self.__StreamingConfig.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND})

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__StreamingConfig)
        return_value = self.__distributionAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformActionAddExpirationTagRaisesException(self):
        """ test Perform Action Add Expiration Tag Raises Exception """
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('add_tag/exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)

        self.__StreamingConfig.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND})

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__StreamingConfig)
        return_value = self.__distributionAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformActionDisableDistribution(self):
        """ test Perform Action Disable Distribution """
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('disable_distributions/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)

        self.__WebConfig.update({
            'configArgument': {"DistributionConfig": {"CallerReference": "1508319919736", "Origins": {"Quantity": 1, "Items": [{"Id": "S3-cf-test-bucket-expiration", "DomainName": "cf-test-bucket-expiration.s3.amazonaws.com", }]}, "DefaultCacheBehavior": {"TargetOriginId": "S3-cf-test-bucket-expiration", "ForwardedValues": {"QueryString": False, "Cookies": {"Forward": "none"}}, "TrustedSigners": {"Enabled": False, "Quantity": 0}, "ViewerProtocolPolicy": "allow-all", "MinTTL": 0, }, "Comment": "", "Enabled": True, }},
            ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_ENABLED_STATE_REFERENCE),
            'ETag': 'MOCKEDETAG'})

        self.__StreamingConfig.update({
            'configArgument': {"StreamingDistributionConfig": {"CallerReference": "1508322219154", "S3Origin": {"DomainName": "cf-test-bucket-expiration.s3.amazonaws.com", "OriginAccessIdentity": ""}, "Aliases": {"Quantity": 0}, "Comment": "", "Logging": {"Enabled": False, "Bucket": "", "Prefix": ""}, "TrustedSigners": {"Enabled": False, "Quantity": 0}, "PriceClass": "PriceClass_All", "Enabled": True}},
            ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_ENABLED_STATE_REFERENCE),
            'ETag': 'MOCKEDETAG'
        })

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__StreamingConfig)
        return_value1 = self.__distributionAction.performAction(eventItem)

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__WebConfig)
        return_value2 = self.__distributionAction.performAction(eventItem)

        assert return_value1 and return_value2

    def testPerformActionDisableDistributionFailure(self):
        """ test Perform Action Disable Distribution Failure """
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('disable_distributions/failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)

        self.__WebConfig.update({
            'configArgument': {"DistributionConfig": {"CallerReference": "1508319919736", "Origins": {"Quantity": 1, "Items": [{"Id": "S3-cf-test-bucket-expiration", "DomainName": "cf-test-bucket-expiration.s3.amazonaws.com"}]}, "DefaultCacheBehavior": {"TargetOriginId": "S3-cf-test-bucket-expiration", "ForwardedValues": {"QueryString": False, "Cookies": {"Forward": "none"}}, "TrustedSigners": {"Enabled": False, "Quantity": 0}, "ViewerProtocolPolicy": "allow-all", "MinTTL": 0}, "Comment": "", "Enabled": True}},
            ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_ENABLED_STATE_REFERENCE),
            'ETag': 'MOCKEDETAG'})

        self.__StreamingConfig.update({
            'configArgument': {"StreamingDistributionConfig": {"CallerReference": "1508322219154", "S3Origin": {"DomainName": "cf-test-bucket-expiration.s3.amazonaws.com", "OriginAccessIdentity": ""}, "Aliases": {"Quantity": 0}, "Comment": "", "Logging": {"Enabled": False, "Bucket": "", "Prefix": ""}, "TrustedSigners": {"Enabled": False, "Quantity": 0}, "PriceClass": "PriceClass_All", "Enabled": True}},
            ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_ENABLED_STATE_REFERENCE),
            'ETag': 'MOCKEDETAG'
        })

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__StreamingConfig)
        return_value1 = self.__distributionAction.performAction(eventItem)

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__WebConfig)
        return_value2 = self.__distributionAction.performAction(eventItem)

        assert return_value1.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformActionDisableDistributionRaiseException(self):
        """ test Perform Action Disable Distribution Raise Exception """
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('disable_distributions/exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)

        self.__WebConfig.update({
            'configArgument': {"DistributionConfig": {"CallerReference": "1508319919736", "Origins": {"Quantity": 1, "Items": [{"Id": "S3-cf-test-bucket-expiration", "DomainName": "cf-test-bucket-expiration.s3.amazonaws.com", }]}, "DefaultCacheBehavior": {"TargetOriginId": "S3-cf-test-bucket-expiration", "ForwardedValues": {"QueryString": False, "Cookies": {"Forward": "none"}}, "TrustedSigners": {"Enabled": False, "Quantity": 0}, "ViewerProtocolPolicy": "allow-all", "MinTTL": 0, }, "Comment": "", "Enabled": True}},
            ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_ENABLED_STATE_REFERENCE),
            'ETag': 'MOCKEDETAG'})

        self.__StreamingConfig.update({
            'configArgument': {"StreamingDistributionConfig": {"CallerReference": "1508322219154", "S3Origin": {"DomainName": "cf-test-bucket-expiration.s3.amazonaws.com", "OriginAccessIdentity": ""}, "Aliases": {"Quantity": 0}, "Comment": "", "Logging": {"Enabled": False, "Bucket": "", "Prefix": ""}, "TrustedSigners": {"Enabled": False, "Quantity": 0}, "PriceClass": "PriceClass_All", "Enabled": True}},
            ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_ENABLED_STATE_REFERENCE),
            'ETag': 'MOCKEDETAG'})

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__StreamingConfig)
        return_value1 = self.__distributionAction.performAction(eventItem)

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__WebConfig)
        return_value2 = self.__distributionAction.performAction(eventItem)

        assert return_value1.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
        assert return_value2.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformActionDeleteDistribution(self):
        """ test Perform Action Delete Distribution """
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_distributions/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)

        self.__WebConfig.update({
            ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_DISABLED_STATE_REFERENCE),
            'ETag': 'MOCKEDETAG'})

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__WebConfig)
        return_value = self.__distributionAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    def testPerformActionDeleteDistributionFailure(self):
        """ test Perform Action Delete Distribution Failure """
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_distributions/failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)

        self.__WebConfig.update({
            ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_DISABLED_STATE_REFERENCE),
            'ETag': 'MOCKEDETAG'
        })

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__WebConfig)
        return_value = self.__distributionAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    def testPerformActionDeleteDistributionRaiseException(self):
        """ test Perform Action Delete Distribution Raise Exception"""
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_distributions/exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)

        self.__WebConfig.update({
            ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_DISABLED_STATE_REFERENCE),
            'ETag': 'MOCKEDETAG'
        })

        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__WebConfig)
        return_value = self.__distributionAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION
