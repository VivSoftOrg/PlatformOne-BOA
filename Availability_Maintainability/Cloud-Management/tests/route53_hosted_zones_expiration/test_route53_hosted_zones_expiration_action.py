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

from route53_hosted_zones_expiration.route53_hosted_zones_expiration_action import *
from tests.route53_hosted_zones_expiration.test_route53_hosted_zones_expiration_placebo_initializer import *
import common.compliance_object_factory as complianceObjectFactory
from common.common_constants import AWSResourceClassConstants
from common.compliance_object_factory import ComplianceObjectFactory


RESOURCE_ID = "Service Name"
RESOURCE_TYPE = AWSResourceClassConstants.WORKSPACES_RESOURCE

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

CONTEXT = ''

class TestHostedZonesExpirationAction:

    _AbstractAction__eventParam = complianceObjectFactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __hostedZonesAction = HostedZoneExpirationAction(_AbstractAction__eventParam)

    __configItems = {
        'resourceName': 'Mock HostedZone',
        'region': 'us-east-1'
    }

    def testPerformActionAddExpirationTag(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('add_tag/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__hostedZonesAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformActionAddExpirationTagFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('add_tag/failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__hostedZonesAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformActionAddExpirationTagRaisesException(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('add_tag/exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__hostedZonesAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformActionDeleteWorkSpace(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_hosted_zones/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_VALIDITY_EXPIRED})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__hostedZonesAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testPerformActionDeleteWorkSpaceWhenSuspended(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_hosted_zones/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_VALIDITY_EXPIRED})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__hostedZonesAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testPerformActionDeleteWorkSpaceFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_hosted_zones/failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_VALIDITY_EXPIRED})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__hostedZonesAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE


    def testPerformActionDeleteWorkSpaceRaiseException(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_hosted_zones/exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_VALIDITY_EXPIRED})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__hostedZonesAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformActionServiceAboutToExpire(self):
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_ABOUT_TO_EXPIRE})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__hostedZonesAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
