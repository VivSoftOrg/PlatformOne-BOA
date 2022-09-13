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
from check_ec2_unused_eip_values.check_ec2_unused_eip_values_action import *
import common.compliance_object_factory as cof
from common.compliance_object_factory import ComplianceObjectFactory 
from common.common_constants import ComplianceConstants

import check_ec2_unused_eip_values.check_ec2_unused_eip_values_action as eip

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

addressObjectVPC = {'allocationid': 'eipalloc-4ce3bb7e', 'publicip': '34.233.43.137', 'domain': 'vpc','region':'us-east-1'}

addressObjectNonVPC = {'allocationid': 'eipalloc-4ce3bb7e', 'publicip': '34.233.43.137', 'domain': 'ec2','region':'us-east-1'}

VPCVALID = {"ResponseMetadata":{"RequestId":"5d43510f-9498-45ba-b52a-118d5370f9f8","HTTPHeaders":{"vary":"Accept-Encoding","transfer-encoding":"chunked","content-type":"text/xml;charset=UTF-8","server":"AmazonEC2","date":"Mon, 25 Sep 2017 12:50:24 GMT"},"HTTPStatusCode":200,"RetryAttempts":0}}

class TestCheckEc2UnusedEIPValuesAction(object):

    __regions = ['us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    
    __eventParam = cof.ComplianceObjectFactory.createEventParamFrom(
        EVENTJSON,
        CONTEXT
    )

    __checkEc2UnusedEIPValuesAction = CheckEc2UnusedEIPValuesAction(__eventParam)

    __eventItemVPC = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=addressObjectVPC['allocationid'], resourceType=AWSResourceClassConstants.EC2_INSTANCE, configItems=addressObjectVPC)

    __eventItemNonVPC = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=addressObjectVPC['allocationid'], resourceType=AWSResourceClassConstants.EC2_INSTANCE, configItems=addressObjectNonVPC)

    @mock_ec2
    def test_perform_action_with_vpc(self):

        self._AbstractResourceFetcher__eventParam = self.__eventParam

        ec2Client = boto3.client('ec2', self.__regions[0])        
        eip.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.release_address = MagicMock(return_value=VPCVALID)
        
        returnValue = self.__checkEc2UnusedEIPValuesAction.performAction(self.__eventItemVPC)
        assert returnValue.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_ec2
    def test_perform_action_without_vpc(self):

        self._AbstractResourceFetcher__eventParam = self.__eventParam

        ec2Client = boto3.client('ec2', self.__regions[0])
        eip.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.release_address = MagicMock(return_value=VPCVALID)
        
        returnValue = self.__checkEc2UnusedEIPValuesAction.performAction(self.__eventItemNonVPC)
        assert returnValue.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_ec2
    def test_perform_action_with_vpc_else(self):

        self._AbstractResourceFetcher__eventParam = self.__eventParam

        ec2Client = boto3.client('ec2', self.__regions[0])
        eip.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        VPCVALID['ResponseMetadata']['HTTPStatusCode'] = 401
        ec2Client.release_address = MagicMock(return_value=VPCVALID)
        
        returnValue = self.__checkEc2UnusedEIPValuesAction.performAction(self.__eventItemVPC)
        assert returnValue.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_ec2
    def test_perform_action_without_vpc_else(self):

        self._AbstractResourceFetcher__eventParam = self.__eventParam

        ec2Client = boto3.client('ec2', self.__regions[0])
        eip.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.release_address = MagicMock(return_value=VPCVALID)
        
        returnValue = self.__checkEc2UnusedEIPValuesAction.performAction(self.__eventItemNonVPC)
        assert returnValue.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_ec2
    def test_perform_action_with_vpc_exception(self):

        self._AbstractResourceFetcher__eventParam = self.__eventParam

        ec2Client = boto3.client('ec2', self.__regions[0])
        eip.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.release_address = MagicMock(return_value=KeyError)
        
        returnValue = self.__checkEc2UnusedEIPValuesAction.performAction(self.__eventItemVPC)
        assert returnValue.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

