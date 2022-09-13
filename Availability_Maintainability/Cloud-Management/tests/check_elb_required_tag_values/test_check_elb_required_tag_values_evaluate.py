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
import boto3
import sys
import os
sys.path.append('../../')
import check_elb_required_tag_values.check_elb_required_tag_values_evaluate as elbEvaluate
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.abstract_evaluate import *
from common.common_constants import *
from common.common_utility import *
from common.i18n import Translation as _
from mock import MagicMock
from moto import mock_elb

EVENT_JSON = {
    "configRuleId": "config-rule-1v52mx",
    "version": "1.0",
    "configRuleName": "aws-sample-rule",
    "configRuleArn": "arn:aws:config:us-east-1:411815166437:config-rule/config-rule-1v52mx",
    "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"configurationItem\": {\n    \"relatedEvents\": [],\n    \"relationships\": [\n      {\n        \"resourceId\": \"i-05b8ba2c066f455ec\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::NetworkInterface\",\n        \"name\": \"Contains NetworkInterface\"\n      },\n      {\n        \"resourceId\": \"sg-056a2f78\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"sg-c500e8ba\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"subnet-e41559ad\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Subnet\",\n        \"name\": \"Is contained in Subnet\"\n      },\n      {\n        \"resourceId\": \"vol-03807f5f89a1b3d0b\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Volume\",\n        \"name\": \"Is attached to Volume\"\n      },\n      {\n        \"resourceId\": \"vpc-a02ce1c6\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::VPC\",\n        \"name\": \"Is contained in Vpc\"\n      }\n    ],\n    \"configuration\": {\n      \"instanceId\": \"i-05b8ba2c066f455ec\",\n      \"imageId\": \"ami-a4c7edb2\",\n      \"state\": {\n        \"code\": 16,\n        \"name\": \"running\"\n      },\n      \"privateDnsName\": \"ip-172-31-28-156.ec2.internal\",\n      \"publicDnsName\": \"ec2-54-235-57-47.compute-1.amazonaws.com\",\n      \"stateTransitionReason\": \"\",\n      \"keyName\": \"REAN_GAURAVASHTIKAR_VIRGINIA_KEYPAIR\",\n      \"amiLaunchIndex\": 0,\n      \"productCodes\": [],\n      \"instanceType\": \"t2.nano\",\n      \"launchTime\": \"2017-07-09T17:34:48.000Z\",\n      \"placement\": {\n        \"availabilityZone\": \"us-east-1b\",\n        \"groupName\": \"\",\n        \"tenancy\": \"default\",\n        \"hostId\": null,\n        \"affinity\": null\n      },\n      \"kernelId\": null,\n      \"ramdiskId\": null,\n      \"platform\": null,\n      \"monitoring\": {\n        \"state\": \"disabled\"\n      },\n      \"subnetId\": \"subnet-29aa575e\",\n      \"vpcId\": \"vpc-c5ec30a0\",\n      \"privateIpAddress\": \"172.31.28.156\",\n      \"publicIpAddress\": \"54.235.57.47\",\n      \"stateReason\": null,\n      \"architecture\": \"x86_64\",\n      \"rootDeviceType\": \"ebs\",\n      \"rootDeviceName\": \"/dev/sda1\",\n      \"blockDeviceMappings\": [\n        {\n          \"deviceName\": \"/dev/sda1\",\n          \"ebs\": {\n            \"volumeId\": \"vol-0bc42d36aa49858fd\",\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:11.000Z\",\n            \"deleteOnTermination\": true\n          }\n        }\n      ],\n      \"virtualizationType\": \"hvm\",\n      \"instanceLifecycle\": null,\n      \"spotInstanceRequestId\": null,\n      \"clientToken\": \"FSRse1484029749587\",\n      \"tags\": [\n        {\n          \"key\": \"Project\",\n          \"value\": \"mnc\"\n        },\n        {\n          \"key\": \"Environment\",\n          \"value\": \"Testing\"\n        },\n        {\n          \"key\": \"Owner\",\n          \"value\": \"Priyanka\"\n        },\n        {\n          \"key\": \"Name\",\n          \"value\": \"Gaurav-Test-MNC\"\n        },\n        {\n          \"value\": \"True\",\n          \"key\": \"NoShutdown\"\n        },\n        {\n          \"key\": \"ExpirationDate\",\n          \"value\": \"2017-09-13\"\n        }\n      ],\n      \"securityGroups\": [\n        {\n          \"groupName\": \"launch-wizard-4\",\n          \"groupId\": \"sg-a845a3d8\"\n        }\n      ],\n      \"sourceDestCheck\": true,\n      \"hypervisor\": \"xen\",\n      \"networkInterfaces\": [\n        {\n          \"networkInterfaceId\": \"eni-3cc64fd2\",\n          \"subnetId\": \"subnet-e41559ad\",\n          \"vpcId\": \"vpc-47105e22\",\n          \"description\": \"Primary network interface\",\n          \"ownerId\": \"107339370656\",\n          \"status\": \"in-use\",\n          \"macAddress\": \"0a:18:41:09:07:34\",\n          \"privateIpAddress\": \"172.31.42.129\",\n          \"privateDnsName\": \"ip-172-31-42-129.ec2.internal\",\n          \"sourceDestCheck\": true,\n          \"groups\": [\n            {\n              \"groupName\": \"launch-wizard-92\",\n              \"groupId\": \"sg-c500e8ba\"\n            },\n            {\n              \"groupName\": \"jenkins_sg_allow\",\n              \"groupId\": \"sg-056a2f78\"\n            }\n          ],\n          \"attachment\": {\n            \"attachmentId\": \"eni-attach-29cd5d69\",\n            \"deviceIndex\": 0,\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:10.000Z\",\n            \"deleteOnTermination\": true\n          },\n          \"association\": null,\n          \"privateIpAddresses\": [\n            {\n              \"privateIpAddress\": \"10.16.3.63\",\n              \"privateDnsName\": \"ip-10-16-3-63.ec2.internal\",\n              \"primary\": true,\n              \"association\": null\n            }\n          ],\n          \"ipv6Addresses\": []\n        }\n      ],\n      \"iamInstanceProfile\": {\n        \"arn\": \"arn:aws:iam::411815166437:instance-profile/jenkins_master_noel.georgi\",\n        \"id\": \"AIPAJ4KIXV5QRL25MMMCK\"\n      },\n      \"ebsOptimized\": false,\n      \"sriovNetSupport\": null,\n      \"enaSupport\": null\n    },\n    \"supplementaryConfiguration\": {},\n    \"tags\": {\n      \"Project\": \"mnc\",\n      \"Owner\": \"Priyanka\",\n      \"ExpirationDate\": \"2017-09-13\",\n      \"Environment\": \"Testing\",\n      \"NoShutdown\": \"true\",\n      \"Name\": \"Gaurav-Test-MNC\"\n    },\n    \"configurationItemVersion\": \"1.2\",\n    \"configurationItemCaptureTime\": \"2017-05-18T18:47:14.686Z\",\n    \"configurationStateId\": 1495133234686,\n    \"awsAccountId\": \"411815166437\",\n    \"configurationItemStatus\": \"OK\",\n    \"resourceType\": \"AWS::EC2::Instance\",\n    \"resourceId\": \"i-05b8ba2c066f455ec\",\n    \"resourceName\": null,\n    \"ARN\": \"arn:aws:ec2:us-east-1:411815166437:instance/i-0250bff57b217c421\",\n    \"awsRegion\": \"us-east-1\",\n    \"availabilityZone\": \"us-east-1b\",\n    \"configurationStateMd5Hash\": \"ed5fe5d85665e3be3607c27aa50fa0ea\",\n    \"resourceCreationTime\": \"2017-05-13T14:14:48.000Z\"\n  },\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ConfigurationItemChangeNotification\",\n  \"recordVersion\": \"1.2\"\n}",
    "resultToken": "",
    "eventLeftScope": "False",
    "ruleParameters": "{\n  \"toEmail\": \"vaibhav.fulsundar@reancloud.com\", \"validity\": \"1\", \"expirationDateLimit\": \"20\",\n  \"performAction\": \"True\",\n  \"notifier\": \"ses\", \"RequiredTags\":\"Owner, Project, Environment, ExpirationDate\" \n}",
    "executionRoleArn": "arn:aws:iam::411815166437:role/awsconfig-role",
    "accountId": "411815166437"
}

CONTEXT = ""

RESOURCE_ID = 'testELB'
RESOURCE_TYPE1 = AWSResourceClassConstants.ELB_RESOURCE
RESOURCE_TYPE2 = AWSResourceClassConstants.ELB_V2_RESOURCE
RESOURCE_TYPE3 = AWSResourceClassConstants.IAM_RESOURCE
CONFIG_ITEMS = {'region': 'us-east-1', 'loadbalancerarn': 'arn:aws:elasticloadbalancing:us-east-1:693265998683:loadbalancer/app/testApp/0dd0188b39ece326'}


class TestELBRequiredTagValuesEvaluate(object):

    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __checkELBRequiredTagValuesEvaluate = elbEvaluate.CheckELBRequiredTagValuesEvaluate(__eventParam)

    __regions = ['us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']

    __mockResponse1 = {'TagDescriptions': [{'LoadBalancerName': 'testELB', 'Tags': [{'Key': 'Environment', 'Value': 'Testing'}, {'Key': 'Owner', 'Value': 'vaibhav.fulsundar'}, {'Key': 'ExpirationDate', 'Value': '2018-02-05'}, {'Key': 'Name', 'Value': 'TestELB'}]}], 'ResponseMetadata': {'HTTPStatusCode': 200, 'HTTPHeaders': {'content-length': '967', 'x-amzn-requestid': 'c243238d-066a-11e8-8c16-7789a35fc791', 'content-type': 'text/xml', 'date': 'Wed, 31 Jan 2018 09:40:22 GMT'}, 'RequestId': 'c243238d-066a-11e8-8c16-7789a35fc791', 'RetryAttempts': 0}}
    __mockResponse2 = {'TagDescriptions': [{'LoadBalancerName': 'testELB', 'Tags': [{'Key': 'RequiredTagsExpirationDate', 'Value': '2018-02-05'}, {'Key': 'Project', 'Value': 'mnc'}, {'Key': 'Environment', 'Value': 'Testing'}, {'Key': 'Owner', 'Value': 'vaibhav.fulsundar'}, {'Key': 'ExpirationDate', 'Value': '2018-02-05'}, {'Key': 'Name', 'Value': 'TestELB'}]}], 'ResponseMetadata': {'HTTPStatusCode': 200, 'HTTPHeaders': {'content-length': '967', 'x-amzn-requestid': 'c243238d-066a-11e8-8c16-7789a35fc791', 'content-type': 'text/xml', 'date': 'Wed, 31 Jan 2018 09:40:22 GMT'}, 'RequestId': 'c243238d-066a-11e8-8c16-7789a35fc791', 'RetryAttempts': 0}}
    __mockResponse3 = {'TagDescriptions': [{'LoadBalancerName': 'testELB', 'Tags': [{'Key': 'RequiredTagsExpirationDate', 'Value': '2018-02-05'}, {'Key': 'Environment', 'Value': 'Testing'}, {'Key': 'ExpirationDate', 'Value': '2018-02-05'}, {'Key': 'Name', 'Value': 'TestELB'}]}], 'ResponseMetadata': {'HTTPStatusCode': 200, 'HTTPHeaders': {'content-length': '967', 'x-amzn-requestid': 'c243238d-066a-11e8-8c16-7789a35fc791', 'content-type': 'text/xml', 'date': 'Wed, 31 Jan 2018 09:40:22 GMT'}, 'RequestId': 'c243238d-066a-11e8-8c16-7789a35fc791', 'RetryAttempts': 0}}
    __mockResponse4 = {'TagDescriptions': [{'LoadBalancerName': 'testELB', 'Tags': [{'Key': 'RequiredTagsExpirationDate', 'Value': (datetime.now() + timedelta(days=3)).date().isoformat()}, {'Key': 'Environment', 'Value': 'Testing'}, {'Key': 'ExpirationDate', 'Value': '2018-02-05'}, {'Key': 'Name', 'Value': 'TestELB'}]}], 'ResponseMetadata': {'HTTPStatusCode': 200, 'HTTPHeaders': {'content-length': '967', 'x-amzn-requestid': 'c243238d-066a-11e8-8c16-7789a35fc791', 'content-type': 'text/xml', 'date': 'Wed, 31 Jan 2018 09:40:22 GMT'}, 'RequestId': 'c243238d-066a-11e8-8c16-7789a35fc791', 'RetryAttempts': 0}}
    __mockResponse5 = {'TagDescriptions': [{'LoadBalancerName': 'testELB', 'Tags': [{'Key': 'RequiredTagsExpirationDate', 'Value': (datetime.now() + timedelta(days=2)).date().isoformat()}, {'Key': 'Environment', 'Value': 'Testing'}, {'Key': 'ExpirationDate', 'Value': '2018-02-05'}, {'Key': 'Name', 'Value': 'TestELB'}]}], 'ResponseMetadata': {'HTTPStatusCode': 200, 'HTTPHeaders': {'content-length': '967', 'x-amzn-requestid': 'c243238d-066a-11e8-8c16-7789a35fc791', 'content-type': 'text/xml', 'date': 'Wed, 31 Jan 2018 09:40:22 GMT'}, 'RequestId': 'c243238d-066a-11e8-8c16-7789a35fc791', 'RetryAttempts': 0}}
    __mockResponse6 = {'TagDescriptions': [{'LoadBalancerName': 'testELB', 'Tags': [{'Key': 'RequiredTagsExpirationDate', 'Value': (datetime.now() + timedelta(days=35)).date().isoformat()}, {'Key': 'Environment', 'Value': 'Testing'}, {'Key': 'ExpirationDate', 'Value': '2018-02-05'}, {'Key': 'Name', 'Value': 'TestELB'}]}], 'ResponseMetadata': {'HTTPStatusCode': 200, 'HTTPHeaders': {'content-length': '967', 'x-amzn-requestid': 'c243238d-066a-11e8-8c16-7789a35fc791', 'content-type': 'text/xml', 'date': 'Wed, 31 Jan 2018 09:40:22 GMT'}, 'RequestId': 'c243238d-066a-11e8-8c16-7789a35fc791', 'RetryAttempts': 0}}
    __mockResponse7 = {'TagDescriptions': [{'LoadBalancerName': 'testELB', 'Tags': [{'Key': 'RequiredTagsExpirationDate', 'Value': '02-05-2018'}, {'Key': 'Environment', 'Value': 'Testing'}, {'Key': 'ExpirationDate', 'Value': '2018-02-05'}, {'Key': 'Name', 'Value': 'TestELB'}]}], 'ResponseMetadata': {'HTTPStatusCode': 200, 'HTTPHeaders': {'content-length': '967', 'x-amzn-requestid': 'c243238d-066a-11e8-8c16-7789a35fc791', 'content-type': 'text/xml', 'date': 'Wed, 31 Jan 2018 09:40:22 GMT'}, 'RequestId': 'c243238d-066a-11e8-8c16-7789a35fc791', 'RetryAttempts': 0}}
    __ResourceName = 'ELB'


    @mock_elb
    def test_elb_required_tag_values_noncompliant(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB, self.__regions[0])
        elbEvaluate.BotoUtility.getClient = MagicMock(return_value=elbClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE1, configItems=CONFIG_ITEMS)
        elbClient.describe_tags = MagicMock(return_value=self.__mockResponse1)
        evaluationResult = self.__checkELBRequiredTagValuesEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_elb
    def test_elb_required_tag_values_compliant(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB, self.__regions[0])
        elbEvaluate.BotoUtility.getClient = MagicMock(return_value=elbClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE1, configItems=CONFIG_ITEMS)
        elbClient.describe_tags = MagicMock(return_value=self.__mockResponse2)
        elbClient.remove_tags = MagicMock(return_value=self.__mockResponse2)
        evaluationResult = self.__checkELBRequiredTagValuesEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def test_elbv2_required_tag_values_noncompliant(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        elbClientv2 = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB_V2, self.__regions[0])
        elbEvaluate.BotoUtility.getClient = MagicMock(return_value=elbClientv2)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE2, configItems=CONFIG_ITEMS)
        elbClientv2.describe_tags = MagicMock(return_value=self.__mockResponse1)
        evaluationResult = self.__checkELBRequiredTagValuesEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_elb
    def test_elbv2_required_tag_values_compliant(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        elbClientv2 = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB_V2, self.__regions[0])
        elbEvaluate.BotoUtility.getClient = MagicMock(return_value=elbClientv2)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE2, configItems=CONFIG_ITEMS)
        elbClientv2.describe_tags = MagicMock(return_value=self.__mockResponse2)
        elbClientv2.remove_tags = MagicMock(return_value=self.__mockResponse2)
        evaluationResult = self.__checkELBRequiredTagValuesEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_elb
    def test_invalid_resource_type(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE3, configItems=CONFIG_ITEMS)
        message = "The rule doesn't apply to resources of type {} ."
        evaluationResult = self.__checkELBRequiredTagValuesEvaluate.evaluate(eventItem)
        assert evaluationResult.annotation == message.format(RESOURCE_TYPE3)

    @mock_elb
    def test_elb_with_date_expired(self):
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB, self.__regions[0])
        elbEvaluate.BotoUtility.getClient = MagicMock(return_value=elbClient)
        elbClient.describe_tags = MagicMock(return_value=self.__mockResponse3)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE1, configItems=CONFIG_ITEMS)
        evaluationResult = self.__checkELBRequiredTagValuesEvaluate.evaluate(eventItem)
        assert evaluationResult.annotation == EvaluationMessages.RESOURCE_EXPIRED.format(self.__ResourceName, '')

    @mock_elb
    def test_elb_with_date_exceeded(self):
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB, self.__regions[0])
        elbEvaluate.BotoUtility.getClient = MagicMock(return_value=elbClient)
        elbClient.describe_tags = MagicMock(return_value=self.__mockResponse6)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE1, configItems=CONFIG_ITEMS)
        evaluationResult = self.__checkELBRequiredTagValuesEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_elb
    def test_elb_with_days_remaining_condition1(self):
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB, self.__regions[0])
        elbEvaluate.BotoUtility.getClient = MagicMock(return_value=elbClient)
        elbClient.describe_tags = MagicMock(return_value=self.__mockResponse4)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE1, configItems=CONFIG_ITEMS)
        evaluationResult = self.__checkELBRequiredTagValuesEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_elb
    def test_elb_with_invalid_date(self):
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB, self.__regions[0])
        elbEvaluate.BotoUtility.getClient = MagicMock(return_value=elbClient)
        elbClient.describe_tags = MagicMock(return_value=self.__mockResponse7)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE1, configItems=CONFIG_ITEMS)
        evaluationResult = self.__checkELBRequiredTagValuesEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_elb
    def test_elb_with_days_remaining_condition2(self):
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB, self.__regions[0])
        elbEvaluate.BotoUtility.getClient = MagicMock(return_value=elbClient)
        elbClient.describe_tags = MagicMock(return_value=self.__mockResponse5)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE1, configItems=CONFIG_ITEMS)
        evaluationResult = self.__checkELBRequiredTagValuesEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_elb
    def test_elb_with_no_tags(self):
        elbClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ELB, self.__regions[0])
        elbEvaluate.BotoUtility.getClient = MagicMock(return_value=elbClient)
        elbClient.describe_tags = MagicMock(return_value=self.__mockResponse1)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE1, configItems=CONFIG_ITEMS)
        evaluationResult = self.__checkELBRequiredTagValuesEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
