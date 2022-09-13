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

from common.framework_objects import EvaluationResult
from check_ec2_unused_eip_values.check_ec2_unused_eip_values_resource_fetcher import *
import common.compliance_object_factory as cof

import check_ec2_unused_eip_values.check_ec2_unused_eip_values_resource_fetcher as eip

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

ADDRESSES = {
	"ResponseMetadata": {
		"RequestId": "5d43510f-9498-45ba-b52a-118d5370f9f8",
		"HTTPHeaders": {
			"vary": "Accept-Encoding",
			"transfer-encoding": "chunked",
			"content-type": "text/xml;charset=UTF-8",
			"server": "AmazonEC2",
			"date": "Mon, 25 Sep 2017 12:50:24 GMT"
		},
		"HTTPStatusCode": 200,
		"RetryAttempts": 0
	},
	"Addresses": [{
		"InstanceId": "i-03e13d53a13077220",
		"NetworkInterfaceOwnerId": "107339370656",
		"AssociationId": "eipassoc-15c1f021",
		"PublicIp": "34.233.43.137",
		"AllocationId": "eipalloc-4ce3bb7e",
		"PrivateIpAddress": "172.31.37.51",
		"Domain": "vpc",
		"NetworkInterfaceId": "eni-ae61c510"
	},{
		"AllocationId": "eipalloc-4ce3bb7e",
		"PublicIp": "34.233.43.137",
		"Domain": "vpc",
    }
    ]
}

REGIONS ={"Regions": [{"Endpoint": "ec2.ap-south-1.amazonaws.com", "RegionName": "ap-south-1"}, {"Endpoint": "ec2.eu-west-2.amazonaws.com", "RegionName": "eu-west-2"}, {"Endpoint": "ec2.eu-west-1.amazonaws.com", "RegionName": "eu-west-1"}, {"Endpoint": "ec2.ap-northeast-2.amazonaws.com", "RegionName": "ap-northeast-2"}, {"Endpoint": "ec2.ap-northeast-1.amazonaws.com", "RegionName": "ap-northeast-1"}, {"Endpoint": "ec2.sa-east-1.amazonaws.com", "RegionName": "sa-east-1"}, {"Endpoint": "ec2.ca-central-1.amazonaws.com", "RegionName": "ca-central-1"}, {"Endpoint": "ec2.ap-southeast-1.amazonaws.com", "RegionName": "ap-southeast-1"}, {"Endpoint": "ec2.ap-southeast-2.amazonaws.com", "RegionName": "ap-southeast-2"}, {"Endpoint": "ec2.eu-central-1.amazonaws.com", "RegionName": "eu-central-1"}, {"Endpoint": "ec2.us-east-1.amazonaws.com", "RegionName": "us-east-1"}, {"Endpoint": "ec2.us-east-2.amazonaws.com", "RegionName": "us-east-2"}, {"Endpoint": "ec2.us-west-1.amazonaws.com", "RegionName": "us-west-1"}, {"Endpoint": "ec2.us-west-2.amazonaws.com", "RegionName": "us-west-2"}], "ResponseMetadata": {"RetryAttempts": 0, "HTTPStatusCode": 200, "RequestId": "1cf48544-1773-464e-9c79-bc95b0fee480", "HTTPHeaders": {"transfer-encoding": "chunked", "vary": "Accept-Encoding", "server": "AmazonEC2", "content-type": "text/xml;charset=UTF-8", "date": "Tue, 26 Sep 2017 10:06:37 GMT"}}}


class TestCheckEc2UnusedEIPValuesResourceFetcher(object):

    __regions = ['us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __eventParam = cof.ComplianceObjectFactory.createEventParamFrom(
        EVENTJSON,
        CONTEXT
    )

    __checkEc2UnusedEIPValuesResourceFetcher = CheckEc2UnusedEIPValuesResourceFetcher(__eventParam)
    @mock_ec2
    def test_fetcher_empty_list(self):
        evaluationResult = EvaluationResult()

        self._AbstractResourceFetcher__eventParam = self.__eventParam

        ec2Client = boto3.client('ec2', self.__regions[0])    
        eip.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        
        
        addressList = self.__checkEc2UnusedEIPValuesResourceFetcher.resourceFetcher()
        assert len(addressList) == 0

    @mock_ec2
    def test_fetcher(self):
        evaluationResult = EvaluationResult()
        self._AbstractResourceFetcher__eventParam = self.__eventParam

        ec2Con = boto3.client('ec2', self.__regions[0])
        ec2Con.describe_regions = MagicMock(return_value=REGIONS)
        ec2Client = boto3.client('ec2', self.__regions[0])    
        eip.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_addresses = MagicMock(return_value=ADDRESSES)
        
        addressList = self.__checkEc2UnusedEIPValuesResourceFetcher.resourceFetcher()
        assert len(addressList) != 0
