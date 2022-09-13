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
from iam_roles_excess_permissions.iam_roles_excess_permissions_evaluate import *
from tests.iam_roles_excess_permissions.iam_roles_excess_permissions_placebo_initializer import *
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import *
from common.abstract_evaluate import *
from common.common_utility import *
from common.boto_utility import *

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
RESOURCE_ID = ''

class TestIamRoleExcessPermissionsEvaluate(object):

    _AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __evaluateIamRolesWithExcessPermissions = IamRolesAccessPermissionsEvaluate(_AbstractEvaluator__eventParam)

    def testEvaluateIamRoleWithMinimalPermissions(self):
        configItems = {
            IamConstants.ROLE_NAME: "dummyRole"
        }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItems)
        recordedMockResponsePath = PlaceboMockResponseInitializer.getEvaluatorMock('compliant_resources')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        evaluationResult = self.__evaluateIamRolesWithExcessPermissions.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testEvaluateIamRoleWithMorePermissions(self):
        configItems = {
            IamConstants.ROLE_NAME: "dummyRole"
        }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItems)
        recordedMockResponsePath = PlaceboMockResponseInitializer.getEvaluatorMock('non_compliant_resources')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        evaluationResult = self.__evaluateIamRolesWithExcessPermissions.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateExcludeIamRole(self):
        configItems = {
            IamConstants.ROLE_NAME: "REANMSAdmin"
        }
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItems)
        evaluationResult = self.__evaluateIamRolesWithExcessPermissions.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE
