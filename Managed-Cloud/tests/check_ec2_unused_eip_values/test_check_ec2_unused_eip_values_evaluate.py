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
import sys
import boto3
from mock import MagicMock
from moto import mock_ec2

sys.path.append('../../')

from common.common_constants import *
from common.boto_utility import *
from check_ec2_unused_eip_values.check_ec2_unused_eip_values_evaluate import *
import common.compliance_object_factory as cof
from common.compliance_object_factory import ComplianceObjectFactory

import check_ec2_unused_eip_values.check_ec2_unused_eip_values_evaluate as eip

EVENTJSON = {
    "version": "1.0",
    "invokingEvent": "{\n \"configurationItemDiff\": null,\n \"configurationItem\": {\n \"relatedEvents\": [],\n \"relationships\": [{\n \"resourceId\": \"AGPAI5DSTRYR7HZKTK5NG\",\n \"resourceName\": \"PowerUsers\",\n \"resourceType\": \"AWS::IAM::Group\",\n \"name\": \"Is attached to Group\"\n }],\n \"configuration\": {\n \"path\": \" / \",\n \"userName\": \"test.user\",\n \"userId\": \"AIDAJNL63BJPIG4KUSNEC\",\n \"arn\": \"arn:aws:iam::107339370656:user/test.user\",\n \"createDate\": \"2017 - 07 - 21 T04: 15: 53.000 Z\",\n \"userPolicyList\": [],\n \"groupList\": [\n \"PowerUsers\"\n ],\n \"attachedManagedPolicies\": [{\n \"policyName\": \"AWSLambdaFullAccess\",\n \"policyArn\": \"arn: aws: iam::aws: policy / AWSLambdaFullAccess\"\n }, {\n \"policyName\": \"IAMFullAccess\",\n \"policyArn\": \"arn: aws: iam::aws: policy / IAMFullAccess\"\n }]\n },\n \"supplementaryConfiguration\": {},\n \"tags\": {},\n \"configurationItemVersion\": \"1.2 \",\n \"configurationItemCaptureTime\": \"2017 - 08 - 22 T14: 49: 58.374 Z\",\n \"configurationStateId\": 1503413398374,\n \"awsAccountId\":\n \"107339370656\",\n \"configurationItemStatus\": \"ResourceDiscovered\",\n \"resourceType\": \"AWS::IAM::User\",\n \"resourceId\": \"AIDAJZPKT5SW3N7TY7NZS\",\n \"resourceName\": \"anish.bhagwat\",\n \"ARN\": \"arn: aws: iam::107339370656: user / anish.bhagwat\",\n \"awsRegion\": \"global\",\n \"availabilityZone\": \"Not Applicable\",\n \"configurationStateMd5Hash\": \"c33ccb2c3df66b520401fe5a14344cdc\",\n \"resourceCreationTime\": \"2017 - 07 - 21 T04: 15: 53.000 Z\"\n },\n \"notificationCreationTime\": \"2017 - 09 - 18 T05: 58: 16.355 Z\",\n  \"messageType\": \"ConfigurationItemChangeNotification\",\n \"recordVersion\": 1.2\n }",
    "ruleParameters": "{\"performAction\": \"True\",\"notifier\": \"sns\"}",
    "resultToken": "",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-cb01p5",
    "configRuleName": "gaurav-test2",
    "configRuleId": "config-rule-cb01p5",
    "accountId": "107339370656"
}
CONTEXT = ""

validAddressObject = {'associationid': 'eipassoc-15c1f021', 'InstanceId': 'i-03e13d53a13077220', 'Domain': 'vpc', 'NetworkInterfaceId': 'eni-ae61c510', 'AllocationId': 'eipalloc-4ce3bb7e', 'NetworkInterfaceOwnerId': '107339370656', 'PrivateIpAddress': '172.31.37.51', 'PublicIp': '34.233.43.137'}
invalidAddressObject = {'PublicIp': '34.233.43.137', 'Domain': 'vpc'}


class TestCheckEc2UnusedEIPValuesEvaluate(object):

    __regions = ['us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __eventParam = cof.ComplianceObjectFactory.createEventParamFrom(
        EVENTJSON,
        CONTEXT
    )

    __checkEc2UnusedEIPValuesEvaluate = CheckEc2UnusedEIPValuesEvaluate(__eventParam)

    __validEventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId="", resourceType=AWSResourceClassConstants.EC2_INSTANCE, configItems=validAddressObject)

    __invalidEventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId="", resourceType=AWSResourceClassConstants.EC2_INSTANCE, configItems=invalidAddressObject)
    @mock_ec2
    def test_evaluate(self):
        evaluationResult = EvaluationResult()

        self._AbstractResourceFetcher__eventParam = self.__eventParam

        ec2Client = boto3.client('ec2', self.__regions[0])    
        # eip.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        
        
        evaluationResult = self.__checkEc2UnusedEIPValuesEvaluate.evaluate(self.__validEventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_ec2
    def test_evaluate_else(self):
        evaluationResult = EvaluationResult()

        self._AbstractResourceFetcher__eventParam = self.__eventParam

        ec2Client = boto3.client('ec2', self.__regions[0])    
        # eip.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        
        
        evaluationResult = self.__checkEc2UnusedEIPValuesEvaluate.evaluate(self.__invalidEventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
