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

from iam_roles_excess_permissions.iam_roles_excess_permissions_action import *
from tests.iam_roles_excess_permissions.iam_roles_excess_permissions_placebo_initializer import *
import common.compliance_object_factory as complianceObjectFactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import *
from common.common_utility import CommonUtility
from moto import mock_iam
from mock import MagicMock

RESOURCE_ID = "AIDSDFISDFS"

EVENT_JSON = {
    "configRuleId": "config-rule-1v52mx",
    "version": "1.0",
    "configRuleName": "iam_roles_excess_permissions",
    "configRuleArn": "arn:aws:config:us-east-1:693265998683:config-rule/config-rule-1v52mx",
    "invokingEvent": "{\n \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
    "resultToken": "",
    "ruleParameters": "{\"performAction\": \"True\", \n  \"excludeRoles\": \"REANMSAdmin, svc-iam-permissions-monitor\", \n   \"policynames\": \"AdministratorAccess, IAMFullAccess, PowerUserAccess\", \n \"actionName\": \"IamRolesAccessPermissionsAction\", \"evaluateName\": \"IamRolesAccessPermissionsEvaluate\",   \"resourceFetcherName\" : \"IamRolesAccessPermissionsResourceFetcher\",  \"moduleName\": \"iam_roles_excess_permissions\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\"}",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::693265998683:role/awsconfig-role",
    "accountId": "693265998683"
}
CONTEXT = ""
RESOURCE_TYPE = AWSResourceClassConstants.IAM_ROLE

class TestIamRoleExcessPermissionsAction:

    _AbstractAction__eventParam = complianceObjectFactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __configItems = {
        IamConstants.ROLE_NAME: "DummyRole",
        IamConstants.AWS_MANAGED_POLICIES:[
            {
                IamConstants.POLICY_NAME : 'AdministratorAccess',
                IamConstants.POLICY_ARN : "arn:aws:iam::aws:policy/Other"
            },
            {
                IamConstants.POLICY_NAME: 'IAMFullAccess',
                IamConstants.POLICY_ARN : "arn:aws:iam::aws:policy/Other"
            },
            {
                IamConstants.POLICY_NAME: 'PowerUserAccess',
                IamConstants.POLICY_ARN : "arn:aws:iam::aws:policy/Other"
            },
            {
                IamConstants.POLICY_NAME: 'SomeOtherPolicy',
                IamConstants.POLICY_ARN : "arn:aws:iam::aws:policy/Other"
            }
        ],
        IamConstants.INLINE_POLICIES : ["DummyPolicy"]
    }

    __iamRolesExcessPermissionsAction = IamRolesAccessPermissionsAction(_AbstractAction__eventParam)

    __eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=__configItems)

    @mock_iam
    def testDeleteRoleSuccess(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('success')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=self.__configItems)
        return_value = self.__iamRolesExcessPermissionsAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_iam
    def testDeleteRoleFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_role_failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=self.__configItems)
        return_value = self.__iamRolesExcessPermissionsAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    def testDeleteRoleException(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_role_exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=self.__configItems)
        return_value = self.__iamRolesExcessPermissionsAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    def testDeleteInstanceProfileFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_instance_profile_failure')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=self.__configItems)
        return_value = self.__iamRolesExcessPermissionsAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

    def testDeleteInstanceProfileException(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('delete_instance_profile_exception')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=self.__configItems)
        return_value = self.__iamRolesExcessPermissionsAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION
