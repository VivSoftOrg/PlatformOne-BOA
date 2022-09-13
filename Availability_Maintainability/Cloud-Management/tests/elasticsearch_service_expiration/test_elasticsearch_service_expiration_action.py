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
from tests.elasticsearch_service_expiration.test_elasticsearch_service_expiration_placebo_initializer import PlaceboMockResponseInitializer
from elasticsearch_service_expiration.elasticsearch_service_expiration_action import ElasticSearchServiceAction
from common.common_constants import AWSResourceClassConstants
import common.compliance_object_factory as complianceObjectFactory
from common.common_constants import ComplianceConstants, ResourceConstants
from common.compliance_object_factory import ComplianceObjectFactory
sys.path.append('../../')

RESOURCE_ID = "Service Name"
RESOURCE_TYPE = AWSResourceClassConstants.ELASTICSEARCH_SERVICE

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

class TestElasticSearchServiceAction:

    _AbstractAction__eventParam = complianceObjectFactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __ESServiceAction = ElasticSearchServiceAction(_AbstractAction__eventParam)

    __configItems = {
        'ARN': 'arn:aws:es:us-east-1:107339370656:domain/MockDomain1',
        'resourceName': 'MockDomain1',
        'region': 'us-east-1'
    }

    def testPerformActionAddExpirationTag(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('add_tag/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__ESServiceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testPerformActionAddExpirationTagFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('add_tag/failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__ESServiceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformActionAddExpirationTagRaisesException(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('add_tag/exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__ESServiceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformActionDeleteService(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_service/success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_VALIDITY_EXPIRED})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__ESServiceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testPerformActionDeleteServiceFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_service/failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_VALIDITY_EXPIRED})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__ESServiceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE


    def testPerformActionDeleteServiceRaiseException(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_service/exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_VALIDITY_EXPIRED})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__ESServiceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testPerformActionServiceAboutToExpire(self):
        self.__configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: ResourceConstants.RESOURCE_ABOUT_TO_EXPIRE})
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.__configItems)
        return_value = self.__ESServiceAction.performAction(eventItem)

        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
