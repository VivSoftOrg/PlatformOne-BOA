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
import ec2_termination_protection.ec2_termination_protection_evaluate as instanceEvaluate
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.abstract_evaluate import *
from common.common_constants import *
from common.common_utility import *
from mock import MagicMock
from moto import mock_ec2



EVENT_JSON = {
    "configRuleId": "config-rule-1v52mx",
    "version": "1.0",
    "configRuleName": "aws-sample-rule",
    "configRuleArn": "arn:aws:config:us-east-1:411815166437:config-rule/config-rule-1v52mx",
    "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"configurationItem\": {\n    \"relatedEvents\": [],\n    \"relationships\": [\n      {\n        \"resourceId\": \"i-05b8ba2c066f455ec\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::NetworkInterface\",\n        \"name\": \"Contains NetworkInterface\"\n      },\n      {\n        \"resourceId\": \"sg-056a2f78\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"sg-c500e8ba\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"subnet-e41559ad\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Subnet\",\n        \"name\": \"Is contained in Subnet\"\n      },\n      {\n        \"resourceId\": \"vol-03807f5f89a1b3d0b\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Volume\",\n        \"name\": \"Is attached to Volume\"\n      },\n      {\n        \"resourceId\": \"vpc-a02ce1c6\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::VPC\",\n        \"name\": \"Is contained in Vpc\"\n      }\n    ],\n    \"configuration\": {\n      \"instanceId\": \"i-05b8ba2c066f455ec\",\n      \"imageId\": \"ami-a4c7edb2\",\n      \"state\": {\n        \"code\": 16,\n        \"name\": \"running\"\n      },\n      \"privateDnsName\": \"ip-172-31-28-156.ec2.internal\",\n      \"publicDnsName\": \"ec2-54-235-57-47.compute-1.amazonaws.com\",\n      \"stateTransitionReason\": \"\",\n      \"keyName\": \"REAN_GAURAVASHTIKAR_VIRGINIA_KEYPAIR\",\n      \"amiLaunchIndex\": 0,\n      \"productCodes\": [],\n      \"instanceType\": \"t2.nano\",\n      \"launchTime\": \"2017-07-09T17:34:48.000Z\",\n      \"placement\": {\n        \"availabilityZone\": \"us-east-1b\",\n        \"groupName\": \"\",\n        \"tenancy\": \"default\",\n        \"hostId\": null,\n        \"affinity\": null\n      },\n      \"kernelId\": null,\n      \"ramdiskId\": null,\n      \"platform\": null,\n      \"monitoring\": {\n        \"state\": \"disabled\"\n      },\n      \"subnetId\": \"subnet-29aa575e\",\n      \"vpcId\": \"vpc-c5ec30a0\",\n      \"privateIpAddress\": \"172.31.28.156\",\n      \"publicIpAddress\": \"54.235.57.47\",\n      \"stateReason\": null,\n      \"architecture\": \"x86_64\",\n      \"rootDeviceType\": \"ebs\",\n      \"rootDeviceName\": \"/dev/sda1\",\n      \"blockDeviceMappings\": [\n        {\n          \"deviceName\": \"/dev/sda1\",\n          \"ebs\": {\n            \"volumeId\": \"vol-0bc42d36aa49858fd\",\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:11.000Z\",\n            \"deleteOnTermination\": true\n          }\n        }\n      ],\n      \"virtualizationType\": \"hvm\",\n      \"instanceLifecycle\": null,\n      \"spotInstanceRequestId\": null,\n      \"clientToken\": \"FSRse1484029749587\",\n      \"tags\": [\n        {\n          \"key\": \"Project\",\n          \"value\": \"mnc\"\n        },\n        {\n          \"key\": \"Environment\",\n          \"value\": \"Testing\"\n        },\n        {\n          \"key\": \"Owner\",\n          \"value\": \"Priyanka\"\n        },\n        {\n          \"key\": \"Name\",\n          \"value\": \"Gaurav-Test-MNC\"\n        },\n        {\n          \"value\": \"True\",\n          \"key\": \"NoShutdown\"\n        },\n        {\n          \"key\": \"ExpirationDate\",\n          \"value\": \"2017-09-13\"\n        }\n      ],\n      \"securityGroups\": [\n        {\n          \"groupName\": \"launch-wizard-4\",\n          \"groupId\": \"sg-a845a3d8\"\n        }\n      ],\n      \"sourceDestCheck\": true,\n      \"hypervisor\": \"xen\",\n      \"networkInterfaces\": [\n        {\n          \"networkInterfaceId\": \"eni-3cc64fd2\",\n          \"subnetId\": \"subnet-e41559ad\",\n          \"vpcId\": \"vpc-47105e22\",\n          \"description\": \"Primary network interface\",\n          \"ownerId\": \"107339370656\",\n          \"status\": \"in-use\",\n          \"macAddress\": \"0a:18:41:09:07:34\",\n          \"privateIpAddress\": \"172.31.42.129\",\n          \"privateDnsName\": \"ip-172-31-42-129.ec2.internal\",\n          \"sourceDestCheck\": true,\n          \"groups\": [\n            {\n              \"groupName\": \"launch-wizard-92\",\n              \"groupId\": \"sg-c500e8ba\"\n            },\n            {\n              \"groupName\": \"jenkins_sg_allow\",\n              \"groupId\": \"sg-056a2f78\"\n            }\n          ],\n          \"attachment\": {\n            \"attachmentId\": \"eni-attach-29cd5d69\",\n            \"deviceIndex\": 0,\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:10.000Z\",\n            \"deleteOnTermination\": true\n          },\n          \"association\": null,\n          \"privateIpAddresses\": [\n            {\n              \"privateIpAddress\": \"10.16.3.63\",\n              \"privateDnsName\": \"ip-10-16-3-63.ec2.internal\",\n              \"primary\": true,\n              \"association\": null\n            }\n          ],\n          \"ipv6Addresses\": []\n        }\n      ],\n      \"iamInstanceProfile\": {\n        \"arn\": \"arn:aws:iam::411815166437:instance-profile/jenkins_master_noel.georgi\",\n        \"id\": \"AIPAJ4KIXV5QRL25MMMCK\"\n      },\n      \"ebsOptimized\": false,\n      \"sriovNetSupport\": null,\n      \"enaSupport\": null\n    },\n    \"supplementaryConfiguration\": {},\n    \"tags\": {\n      \"Project\": \"mnc\",\n      \"Owner\": \"Priyanka\",\n      \"ExpirationDate\": \"2017-09-13\",\n      \"Environment\": \"Testing\",\n      \"NoShutdown\": \"true\",\n      \"Name\": \"Gaurav-Test-MNC\"\n    },\n    \"configurationItemVersion\": \"1.2\",\n    \"configurationItemCaptureTime\": \"2017-05-18T18:47:14.686Z\",\n    \"configurationStateId\": 1495133234686,\n    \"awsAccountId\": \"411815166437\",\n    \"configurationItemStatus\": \"OK\",\n    \"resourceType\": \"AWS::EC2::Instance\",\n    \"resourceId\": \"i-05b8ba2c066f455ec\",\n    \"resourceName\": null,\n    \"ARN\": \"arn:aws:ec2:us-east-1:411815166437:instance/i-0250bff57b217c421\",\n    \"awsRegion\": \"us-east-1\",\n    \"availabilityZone\": \"us-east-1b\",\n    \"configurationStateMd5Hash\": \"ed5fe5d85665e3be3607c27aa50fa0ea\",\n    \"resourceCreationTime\": \"2017-05-13T14:14:48.000Z\"\n  },\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ConfigurationItemChangeNotification\",\n  \"recordVersion\": \"1.2\"\n}",
    "resultToken": "",
    "eventLeftScope": "False",
    "ruleParameters": "{\"instanceList\":[\"i-0d1a6a41f136b426f\",\"i-08ee3e0a5894f6b59\",\"i-041890c697d58ed56\"],\"performAction\": \"True\",\"notifier\": \"email\",\"environmentValues\": \"Production\"}",
    "executionRoleArn": "arn:aws:iam::411815166437:role/awsconfig-role",
    "accountId": "411815166437"
}

CONTEXT = ""
CONFIG_ITEMS = {'region':'us-east-1'}
RESOURCE_ID = ''
RESOURCE_TYPE = AWSResourceClassConstants.EC2_INSTANCE


class TestEc2NoshutdownTagEvaluate(object):

    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )

    __ec2TerminationProtectionEvaluate = instanceEvaluate.Ec2TerminationProtectionEvaluate(__eventParam)
    __regions = ['us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __compliantMock = {'ResponseMetadata': {'RetryAttempts': 0, 'RequestId': '59dbff89-35bd-4eac-99ed-be587EXAMPLE', 'HTTPHeaders': {'Content-Type': 'text/plain', 'server': 'amazon.com'}, 'HTTPStatusCode': 200}, 'InstanceId': 'i-79dadce832b6647f1', 'DisableApiTermination': {'Value': True}}
    __noncompliantMock = {'ResponseMetadata': {'RetryAttempts': 0, 'RequestId': '59dbff89-35bd-4eac-99ed-be587EXAMPLE', 'HTTPHeaders': {'Content-Type': 'text/plain', 'server': 'amazon.com'}, 'HTTPStatusCode': 200}, 'InstanceId': 'i-79dadce832b6647f1', 'DisableApiTermination': {'Value': False}}
    @mock_ec2
    def test_ec2_termination_protection_noncompliant(self):

        ec2 = boto3.resource('ec2', 'us-east-1')
        vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
        vpc.create_tags(Tags=[{"Key": "Name", "Value": "default_vpc"}])
        ig = ec2.create_internet_gateway()
        vpc.attach_internet_gateway(InternetGatewayId=ig.id)
        route_table = vpc.create_route_table()
        route = route_table.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=ig.id
        )
        subnet = ec2.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc.id)
        sg = ec2.create_security_group(
            GroupName='v-sg1',
            Description='moto sg',
            VpcId=vpc.id
        )
        sg.authorize_ingress(
                CidrIp='0.0.0.0/0',
                IpProtocol='icmp',
                FromPort=-1,
                ToPort=-1
        )
        instances = ec2.create_instances(
            ImageId='ami-835b4efa', InstanceType='t2.micro', MaxCount=1, MinCount=1,
            NetworkInterfaces=[{'SubnetId': subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sg.group_id]}])
        ec2.create_tags(Resources=[instances[0].instance_id], Tags=[{'Key': 'Environment', 'Value': 'Production'}])
        ec2 = boto3.client('ec2', 'us-east-1')
        response = CommonUtility.changeDictionaryKeysToLowerCase(ec2.describe_instances(InstanceIds=[instances[0].instance_id]))
        RESOURCE_ID = instances[0].instance_id
        instanceObject = response['reservations'][0]['instances'][0]
        instanceObject.update({'region': 'us-east-1'})
        CONFIG_ITEMS = instanceObject
        instanceEvaluate.BotoUtility.getClient = MagicMock(return_value=ec2)
        ec2.describe_instance_attribute = MagicMock(return_value = self.__noncompliantMock)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        evaluationResult = self.__ec2TerminationProtectionEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_ec2
    def test_ec2_termination_protection_compliant(self):

        ec2 = boto3.resource('ec2', 'us-east-1')
        vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
        vpc.create_tags(Tags=[{"Key": "Name", "Value": "default_vpc"}])
        ig = ec2.create_internet_gateway()
        vpc.attach_internet_gateway(InternetGatewayId=ig.id)
        route_table = vpc.create_route_table()
        route = route_table.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=ig.id
        )
        subnet = ec2.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc.id)
        sg = ec2.create_security_group(
            GroupName='v-sg1', Description='moto sg', VpcId=vpc.id
        )
        sg.authorize_ingress(
            CidrIp='0.0.0.0/0',
            IpProtocol='icmp',
            FromPort=-1,
            ToPort=-1
        )
        instances = ec2.create_instances(
            ImageId='ami-835b4efa', InstanceType='t2.micro', MaxCount=1, MinCount=1,
            NetworkInterfaces=[{'SubnetId': subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sg.group_id]}])

        ec2.create_tags(Resources=[instances[0].instance_id], Tags=[{'Key': 'Environment', 'Value': 'Production'}])
        ec2 = boto3.client('ec2', 'us-east-1')
        response = CommonUtility.changeDictionaryKeysToLowerCase(ec2.describe_instances(InstanceIds=[instances[0].instance_id]))
        RESOURCE_ID = instances[0].instance_id
        instanceObject = response['reservations'][0]['instances'][0]
        instanceObject.update({'region': 'us-east-1'})
        CONFIG_ITEMS = instanceObject
        instanceEvaluate.BotoUtility.getClient = MagicMock(return_value=ec2)
        ec2.describe_instance_attribute = MagicMock(return_value = self.__compliantMock)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        evaluationResult = self.__ec2TerminationProtectionEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_ec2
    def test_ec2_termination_protection_notapplicable(self):

        ec2 = boto3.resource('ec2', 'us-east-1')
        vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
        vpc.create_tags(Tags=[{"Key": "Name", "Value": "default_vpc"}])
        ig = ec2.create_internet_gateway()
        vpc.attach_internet_gateway(InternetGatewayId=ig.id)
        route_table = vpc.create_route_table()
        route = route_table.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=ig.id
        )
        subnet = ec2.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc.id)
        sg = ec2.create_security_group(
            GroupName='v-sg1', Description='moto sg', VpcId=vpc.id
        )
        sg.authorize_ingress(
            CidrIp='0.0.0.0/0',
            IpProtocol='icmp',
            FromPort=-1,
            ToPort=-1
        )
        instances = ec2.create_instances(
            ImageId='ami-835b4efa', InstanceType='t2.micro', MaxCount=1, MinCount=1,
            NetworkInterfaces=[{'SubnetId': subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sg.group_id]}])

        ec2 = boto3.client('ec2', 'us-east-1')
        response = CommonUtility.changeDictionaryKeysToLowerCase(ec2.describe_instances(InstanceIds=[instances[0].instance_id]))
        RESOURCE_ID = instances[0].instance_id
        instanceObject = response['reservations'][0]['instances'][0]
        instanceObject.update({'region': 'us-east-1'})
        CONFIG_ITEMS = instanceObject
        instanceEvaluate.BotoUtility.getClient = MagicMock(return_value=ec2)
        ec2.describe_instance_attribute = MagicMock(return_value = self.__compliantMock)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        evaluationResult = self.__ec2TerminationProtectionEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

    @mock_ec2
    def test_ec2_termination_protection_no_tags(self):

        ec2 = boto3.resource('ec2', 'us-east-1')
        vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
        vpc.create_tags(Tags=[{"Key": "Name", "Value": "default_vpc"}])
        ig = ec2.create_internet_gateway()
        vpc.attach_internet_gateway(InternetGatewayId=ig.id)
        route_table = vpc.create_route_table()
        route = route_table.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=ig.id
        )
        subnet = ec2.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc.id)
        sg = ec2.create_security_group(
            GroupName='v-sg1', Description='moto sg', VpcId=vpc.id
        )
        sg.authorize_ingress(
            CidrIp='0.0.0.0/0',
            IpProtocol='icmp',
            FromPort=-1,
            ToPort=-1
        )
        instances = ec2.create_instances(
            ImageId='ami-835b4efa', InstanceType='t2.micro', MaxCount=1, MinCount=1,
            NetworkInterfaces=[{'SubnetId': subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sg.group_id]}])

        ec2 = boto3.client('ec2', 'us-east-1')
        response = CommonUtility.changeDictionaryKeysToLowerCase(ec2.describe_instances(InstanceIds=[instances[0].instance_id]))
        RESOURCE_ID = instances[0].instance_id
        instanceObject = response['reservations'][0]['instances'][0]
        instanceObject.update({'region': 'us-east-1'})
        CONFIG_ITEMS = instanceObject
        del CONFIG_ITEMS['tags']
        instanceEvaluate.BotoUtility.getClient = MagicMock(return_value=ec2)
        ec2.describe_instance_attribute = MagicMock(return_value = self.__compliantMock)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        evaluationResult = self.__ec2TerminationProtectionEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
