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
import delete_unused_launch_configurations.delete_unused_launch_configurations_evaluate as launchConfigurationEvaluate
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.abstract_evaluate import *
from common.common_constants import *
from common.common_utility import *
from common.i18n import Translation as _
from mock import MagicMock
from moto import *
import time
from datetime import datetime, timedelta
from dateutil.tz import tzutc
import pytz


EVENT_JSON = {
    "configRuleId": "config-rule-1v52mx",
    "version": "1.0",
    "configRuleName": "aws-sample-rule",
    "configRuleArn": "arn:aws:config:us-east-1:411815166437:config-rule/config-rule-1v52mx",
    "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"configurationItem\": {\n    \"relatedEvents\": [],\n    \"relationships\": [\n      {\n        \"resourceId\": \"i-05b8ba2c066f455ec\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::NetworkInterface\",\n        \"name\": \"Contains NetworkInterface\"\n      },\n      {\n        \"resourceId\": \"sg-056a2f78\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"sg-c500e8ba\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"subnet-e41559ad\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Subnet\",\n        \"name\": \"Is contained in Subnet\"\n      },\n      {\n        \"resourceId\": \"vol-03807f5f89a1b3d0b\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Volume\",\n        \"name\": \"Is attached to Volume\"\n      },\n      {\n        \"resourceId\": \"vpc-a02ce1c6\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::VPC\",\n        \"name\": \"Is contained in Vpc\"\n      }\n    ],\n    \"configuration\": {\n      \"instanceId\": \"i-05b8ba2c066f455ec\",\n      \"imageId\": \"ami-a4c7edb2\",\n      \"state\": {\n        \"code\": 16,\n        \"name\": \"running\"\n      },\n      \"privateDnsName\": \"ip-172-31-28-156.ec2.internal\",\n      \"publicDnsName\": \"ec2-54-235-57-47.compute-1.amazonaws.com\",\n      \"stateTransitionReason\": \"\",\n      \"keyName\": \"REAN_GAURAVASHTIKAR_VIRGINIA_KEYPAIR\",\n      \"amiLaunchIndex\": 0,\n      \"productCodes\": [],\n      \"instanceType\": \"t2.nano\",\n      \"launchTime\": \"2017-07-09T17:34:48.000Z\",\n      \"placement\": {\n        \"availabilityZone\": \"us-east-1b\",\n        \"groupName\": \"\",\n        \"tenancy\": \"default\",\n        \"hostId\": null,\n        \"affinity\": null\n      },\n      \"kernelId\": null,\n      \"ramdiskId\": null,\n      \"platform\": null,\n      \"monitoring\": {\n        \"state\": \"disabled\"\n      },\n      \"subnetId\": \"subnet-29aa575e\",\n      \"vpcId\": \"vpc-c5ec30a0\",\n      \"privateIpAddress\": \"172.31.28.156\",\n      \"publicIpAddress\": \"54.235.57.47\",\n      \"stateReason\": null,\n      \"architecture\": \"x86_64\",\n      \"rootDeviceType\": \"ebs\",\n      \"rootDeviceName\": \"/dev/sda1\",\n      \"blockDeviceMappings\": [\n        {\n          \"deviceName\": \"/dev/sda1\",\n          \"ebs\": {\n            \"volumeId\": \"vol-0bc42d36aa49858fd\",\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:11.000Z\",\n            \"deleteOnTermination\": true\n          }\n        }\n      ],\n      \"virtualizationType\": \"hvm\",\n      \"instanceLifecycle\": null,\n      \"spotInstanceRequestId\": null,\n      \"clientToken\": \"FSRse1484029749587\",\n      \"tags\": [\n        {\n          \"key\": \"Project\",\n          \"value\": \"mnc\"\n        },\n        {\n          \"key\": \"Environment\",\n          \"value\": \"Testing\"\n        },\n        {\n          \"key\": \"Owner\",\n          \"value\": \"Priyanka\"\n        },\n        {\n          \"key\": \"Name\",\n          \"value\": \"Gaurav-Test-MNC\"\n        },\n        {\n          \"value\": \"True\",\n          \"key\": \"NoShutdown\"\n        },\n        {\n          \"key\": \"ExpirationDate\",\n          \"value\": \"2017-09-13\"\n        }\n      ],\n      \"securityGroups\": [\n        {\n          \"groupName\": \"launch-wizard-4\",\n          \"groupId\": \"sg-a845a3d8\"\n        }\n      ],\n      \"sourceDestCheck\": true,\n      \"hypervisor\": \"xen\",\n      \"networkInterfaces\": [\n        {\n          \"networkInterfaceId\": \"eni-3cc64fd2\",\n          \"subnetId\": \"subnet-e41559ad\",\n          \"vpcId\": \"vpc-47105e22\",\n          \"description\": \"Primary network interface\",\n          \"ownerId\": \"107339370656\",\n          \"status\": \"in-use\",\n          \"macAddress\": \"0a:18:41:09:07:34\",\n          \"privateIpAddress\": \"172.31.42.129\",\n          \"privateDnsName\": \"ip-172-31-42-129.ec2.internal\",\n          \"sourceDestCheck\": true,\n          \"groups\": [\n            {\n              \"groupName\": \"launch-wizard-92\",\n              \"groupId\": \"sg-c500e8ba\"\n            },\n            {\n              \"groupName\": \"jenkins_sg_allow\",\n              \"groupId\": \"sg-056a2f78\"\n            }\n          ],\n          \"attachment\": {\n            \"attachmentId\": \"eni-attach-29cd5d69\",\n            \"deviceIndex\": 0,\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:10.000Z\",\n            \"deleteOnTermination\": true\n          },\n          \"association\": null,\n          \"privateIpAddresses\": [\n            {\n              \"privateIpAddress\": \"10.16.3.63\",\n              \"privateDnsName\": \"ip-10-16-3-63.ec2.internal\",\n              \"primary\": true,\n              \"association\": null\n            }\n          ],\n          \"ipv6Addresses\": []\n        }\n      ],\n      \"iamInstanceProfile\": {\n        \"arn\": \"arn:aws:iam::411815166437:instance-profile/jenkins_master_noel.georgi\",\n        \"id\": \"AIPAJ4KIXV5QRL25MMMCK\"\n      },\n      \"ebsOptimized\": false,\n      \"sriovNetSupport\": null,\n      \"enaSupport\": null\n    },\n    \"supplementaryConfiguration\": {},\n    \"tags\": {\n      \"Project\": \"mnc\",\n      \"Owner\": \"Priyanka\",\n      \"ExpirationDate\": \"2017-09-13\",\n      \"Environment\": \"Testing\",\n      \"NoShutdown\": \"true\",\n      \"Name\": \"Gaurav-Test-MNC\"\n    },\n    \"configurationItemVersion\": \"1.2\",\n    \"configurationItemCaptureTime\": \"2017-05-18T18:47:14.686Z\",\n    \"configurationStateId\": 1495133234686,\n    \"awsAccountId\": \"411815166437\",\n    \"configurationItemStatus\": \"OK\",\n    \"resourceType\": \"AWS::EC2::Instance\",\n    \"resourceId\": \"i-05b8ba2c066f455ec\",\n    \"resourceName\": null,\n    \"ARN\": \"arn:aws:ec2:us-east-1:411815166437:instance/i-0250bff57b217c421\",\n    \"awsRegion\": \"us-east-1\",\n    \"availabilityZone\": \"us-east-1b\",\n    \"configurationStateMd5Hash\": \"ed5fe5d85665e3be3607c27aa50fa0ea\",\n    \"resourceCreationTime\": \"2017-05-13T14:14:48.000Z\"\n  },\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ConfigurationItemChangeNotification\",\n  \"recordVersion\": \"1.2\"\n}",
    "resultToken": "",
    "eventLeftScope": "False",
    "ruleParameters": "{\"spareTimeInHours\":\"24\",\"performAction\": \"True\",\"notifier\": \"ses\"}",
    "executionRoleArn": "arn:aws:iam::411815166437:role/awsconfig-role",
    "accountId": "411815166437"
}

CONTEXT = ""
utc = pytz.utc
currentDate = datetime.now()
RESOURCE_ID1 = 'asg'
RESOURCE_ID2 = 'asgTest'
RESOURCE_TYPE = "AWS::AutoScaling::LaunchConfiguration"
CONFIG_ITEMS1 = {'ramdiskid': '', 'blockdevicemappings': [{'devicename': '/dev/sda1', 'ebs': {'snapshotid': 'snap-04a508523b761d796', 'volumesize': 8, 'volumetype': 'gp2', 'deleteontermination': True}}], 'createdtime': datetime(2017, 10, 30, 11, 43, 21, 996000, tzinfo=tzutc()), 'userdata': '', 'securitygroups': ['sg-4092fc28'], 'kernelid': '', 'imageid': 'ami-43391926', 'instancemonitoring': {'enabled': False}, 'launchconfigurationarn': 'arn:aws:autoscaling:us-east-2:107339370656:launchConfiguration:027a4a73-c9ca-4e4f-93c9-fb4f243f8b22:launchConfigurationName/asg', 'ebsoptimized': False, 'keyname': '', 'instancetype': 't2.micro', 'launchconfigurationname': 'asg', 'classiclinkvpcsecuritygroups': [], 'region': 'us-east-2'}
CONFIG_ITEMS2 = {'ramdiskid': '', 'blockdevicemappings': [{'devicename': '/dev/sda1', 'ebs': {'snapshotid': 'snap-04a508523b761d796', 'volumesize': 8, 'volumetype': 'gp2', 'deleteontermination': True}}], 'createdtime': utc.localize(currentDate), 'userdata': '', 'securitygroups': ['sg-4092fc28'], 'kernelid': '', 'imageid': 'ami-43391926', 'instancemonitoring': {'enabled': False}, 'launchconfigurationarn': 'arn:aws:autoscaling:us-east-2:107339370656:launchConfiguration:027a4a73-c9ca-4e4f-93c9-fb4f243f8b22:launchConfigurationName/asg', 'ebsoptimized': False, 'keyname': '', 'instancetype': 't2.micro', 'launchconfigurationname': 'asg', 'classiclinkvpcsecuritygroups': [], 'region': 'us-east-2'}


class TestDeleteUnusedLaunchConfigurationsEvaluate(object):

    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
    __deleteUnusedLaunchConfigurationsEvaluate = launchConfigurationEvaluate.DeleteUnusedLaunchConfigurationsEvaluate(__eventParam)
    __regions = ['us-east-2', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-1', 'us-west-1', 'us-west-2']
    __asgResponse1 = {'ResponseMetadata': {'RetryAttempts': 0, 'HTTPStatusCode': 200, 'RequestId': 'f29747d0-1790-11e8-a159-577a079efc6a', 'HTTPHeaders': {'date': 'Thu, 22 Feb 2018 05:26:34 GMT', 'vary': 'Accept-Encoding', 'content-type': 'text/xml', 'x-amzn-requestid': 'f29747d0-1790-11e8-a159-577a079efc6a', 'content-length': '2828'}}, 'AutoScalingGroups': [{'LaunchConfigurationName': 'asg', 'VPCZoneIdentifier': 'subnet-800f20ca', 'EnabledMetrics': [], 'DefaultCooldown': 300, 'SuspendedProcesses': [{'ProcessName': 'AddToLoadBalancer', 'SuspensionReason': 'User suspended at 2017-12-09T19:00:23Z'}, {'ProcessName': 'HealthCheck', 'SuspensionReason': 'User suspended at 2017-12-09T19:00:23Z'}, {'ProcessName': 'AlarmNotification', 'SuspensionReason': 'User suspended at 2017-12-09T19:00:23Z'}, {'ProcessName': 'ScheduledActions', 'SuspensionReason': 'User suspended at 2017-12-09T19:00:23Z'}, {'ProcessName': 'Launch', 'SuspensionReason': 'User suspended at 2017-12-09T19:00:23Z'}], 'DesiredCapacity': 1, 'AutoScalingGroupARN': 'arn:aws:autoscaling:us-east-2:107339370656:autoScalingGroup:562e255d-6792-40e2-9ff5-d1653cae76ee:autoScalingGroupName/asg', 'TerminationPolicies': ['Default'], 'AutoScalingGroupName': 'asg', 'Tags': [], 'AvailabilityZones': ['us-east-2c'], 'CreatedTime': datetime(2017, 10, 30, 11, 44, 19, 498000, tzinfo=tzutc()), 'MinSize': 1, 'MaxSize': 1, 'NewInstancesProtectedFromScaleIn': False, 'HealthCheckType': 'EC2', 'TargetGroupARNs': [], 'HealthCheckGracePeriod': 300, 'Instances': [{'LaunchConfigurationName': 'asg', 'HealthStatus': 'Healthy', 'InstanceId': 'i-06a171cbc2118e0ff', 'ProtectedFromScaleIn': False, 'AvailabilityZone': 'us-east-2c', 'LifecycleState': 'InService'}], 'LoadBalancerNames': []}]}
    __asgResponse2 = {'ResponseMetadata': {'RetryAttempts': 0, 'HTTPStatusCode': 200, 'RequestId': 'f29747d0-1790-11e8-a159-577a079efc6a', 'HTTPHeaders': {'date': 'Thu, 22 Feb 2018 05:26:34 GMT', 'vary': 'Accept-Encoding', 'content-type': 'text/xml', 'x-amzn-requestid': 'f29747d0-1790-11e8-a159-577a079efc6a', 'content-length': '2828'}}, 'AutoScalingGroups': [{'LaunchConfigurationName': 'asg', 'VPCZoneIdentifier': 'subnet-800f20ca', 'EnabledMetrics': [], 'DefaultCooldown': 300, 'SuspendedProcesses': [{'ProcessName': 'AddToLoadBalancer', 'SuspensionReason': 'User suspended at 2017-12-09T19:00:23Z'}, {'ProcessName': 'HealthCheck', 'SuspensionReason': 'User suspended at 2017-12-09T19:00:23Z'}, {'ProcessName': 'AlarmNotification', 'SuspensionReason': 'User suspended at 2017-12-09T19:00:23Z'}, {'ProcessName': 'ScheduledActions', 'SuspensionReason': 'User suspended at 2017-12-09T19:00:23Z'}, {'ProcessName': 'Launch', 'SuspensionReason': 'User suspended at 2017-12-09T19:00:23Z'}], 'DesiredCapacity': 1, 'AutoScalingGroupARN': 'arn:aws:autoscaling:us-east-2:107339370656:autoScalingGroup:562e255d-6792-40e2-9ff5-d1653cae76ee:autoScalingGroupName/asg', 'TerminationPolicies': ['Default'], 'AutoScalingGroupName': 'asg', 'Tags': [], 'AvailabilityZones': ['us-east-2c'], 'CreatedTime': datetime(2017, 10, 30, 11, 44, 19, 498000, tzinfo=tzutc()), 'MinSize': 1, 'MaxSize': 1, 'NewInstancesProtectedFromScaleIn': False, 'HealthCheckType': 'EC2', 'TargetGroupARNs': [], 'HealthCheckGracePeriod': 300, 'Instances': [{'LaunchConfigurationName': 'asg', 'HealthStatus': 'Healthy', 'InstanceId': 'i-06a171cbc2118e0ff', 'ProtectedFromScaleIn': False, 'AvailabilityZone': 'us-east-2c', 'LifecycleState': 'InService'}], 'LoadBalancerNames': []}]}

    @mock_autoscaling
    def test_unused_launch_configuration_compliant(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        asgClient = boto3.client('autoscaling',self.__regions[0])
        launchConfigurationEvaluate.BotoUtility.getClient = MagicMock(return_value=asgClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID1, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS1)
        asgClient.describe_auto_scaling_groups = MagicMock(return_value=self.__asgResponse1)
        evaluationResult = self.__deleteUnusedLaunchConfigurationsEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_autoscaling
    def test_unused_launch_configuration_noncompliant(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        asgClient = boto3.client('autoscaling',self.__regions[0])
        launchConfigurationEvaluate.BotoUtility.getClient = MagicMock(return_value=asgClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID2, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS1)
        asgClient.describe_auto_scaling_groups = MagicMock(return_value=self.__asgResponse1)
        evaluationResult = self.__deleteUnusedLaunchConfigurationsEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def test_unused_launch_configuration_compliant_not_older(self):
        self._AbstractEvaluator__eventParam = self.__eventParam
        asgClient = boto3.client('autoscaling',self.__regions[0])
        launchConfigurationEvaluate.BotoUtility.getClient = MagicMock(return_value=asgClient)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID1, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS2)
        asgClient.describe_auto_scaling_groups = MagicMock(return_value=self.__asgResponse1)
        evaluationResult = self.__deleteUnusedLaunchConfigurationsEvaluate.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE
