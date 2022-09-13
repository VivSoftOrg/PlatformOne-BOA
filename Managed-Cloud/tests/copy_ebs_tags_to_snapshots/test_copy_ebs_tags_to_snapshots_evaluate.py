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
from moto import mock_iam

sys.path.append('../../')

from common.abstract_evaluate import AbstractEvaluator
from common.framework_objects import EvaluationResult
import copy_ebs_tags_to_snapshots.copy_ebs_tags_to_snapshots_evaluate as copyEBS
import common.compliance_object_factory as cof
from common.common_constants import AWSResourceClassConstants, ComplianceConstants, BotoConstants
from common.compliance_object_factory import ComplianceObjectFactory

CONTEXT = ""
RESOURCE_ID = "test"
RESOURCE_TYPE = "AWS::EC2::Volume"

EVENT_JSON = {
    "configRuleId": "config-rule-1v52mx",
    "version": "1.0",
    "configRuleName": "aws-sample-rule",
    "configRuleArn": "arn:aws:config:us-east-1:411815166437:config-rule/config-rule-1v52mx",
    "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"configurationItem\": {\n    \"relatedEvents\": [],\n    \"relationships\": [\n      {\n        \"resourceId\": \"eni-3cc64fd2\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::NetworkInterface\",\n        \"name\": \"Contains NetworkInterface\"\n      },\n      {\n        \"resourceId\": \"sg-056a2f78\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"sg-33178157\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"subnet-e41559ad\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Subnet\",\n        \"name\": \"Is contained in Subnet\"\n      },\n      {\n        \"resourceId\": \"vol-03807f5f89a1b3d0b\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Volume\",\n        \"name\": \"Is attached to Volume\"\n      },\n      {\n        \"resourceId\": \"vpc-a02ce1c6\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::VPC\",\n        \"name\": \"Is contained in Vpc\"\n      }\n    ],\n    \"configuration\": {\n      \"instanceId\": \"i-098f9826f1ee4072d\",\n      \"imageId\": \"ami-a4c7edb2\",\n      \"state\": {\n        \"code\": 16,\n        \"name\": \"running\"\n      },\n      \"privateDnsName\": \"ip-172-31-28-156.ec2.internal\",\n      \"publicDnsName\": \"ec2-54-235-57-47.compute-1.amazonaws.com\",\n      \"stateTransitionReason\": \"\",\n      \"keyName\": \"REAN_GAURAVASHTIKAR_VIRGINIA_KEYPAIR\",\n      \"amiLaunchIndex\": 0,\n      \"productCodes\": [],\n      \"instanceType\": \"t2.nano\",\n      \"launchTime\": \"2017-07-09T17:34:48.000Z\",\n      \"placement\": {\n        \"availabilityZone\": \"us-east-1b\",\n        \"groupName\": \"\",\n        \"tenancy\": \"default\",\n        \"hostId\": null,\n        \"affinity\": null\n      },\n      \"kernelId\": null,\n      \"ramdiskId\": null,\n      \"platform\": null,\n      \"monitoring\": {\n        \"state\": \"disabled\"\n      },\n      \"subnetId\": \"subnet-29aa575e\",\n      \"vpcId\": \"vpc-c5ec30a0\",\n      \"privateIpAddress\": \"172.31.28.156\",\n      \"publicIpAddress\": \"54.235.57.47\",\n      \"stateReason\": null,\n      \"architecture\": \"x86_64\",\n      \"rootDeviceType\": \"ebs\",\n      \"rootDeviceName\": \"/dev/sda1\",\n      \"blockDeviceMappings\": [\n        {\n          \"deviceName\": \"/dev/sda1\",\n          \"ebs\": {\n            \"volumeId\": \"vol-0bc42d36aa49858fd\",\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:11.000Z\",\n            \"deleteOnTermination\": true\n          }\n        }\n      ],\n      \"virtualizationType\": \"hvm\",\n      \"instanceLifecycle\": null,\n      \"spotInstanceRequestId\": null,\n      \"clientToken\": \"FSRse1484029749587\",\n      \"tags\": [\n        {\n          \"key\": \"Project\",\n          \"value\": \"mnc\"\n        },\n        {\n          \"key\": \"Environment\",\n          \"value\": \"Testing\"\n        },\n        {\n          \"key\": \"Owner\",\n          \"value\": \"gaurav.ashtikar\"\n        },\n        {\n          \"key\": \"Name\",\n          \"value\": \"Gaurav-Test-Machine\"\n        },\n        {\n          \"value\": \"NoShutdown\",\n          \"key\": \"true\"\n        },\n        {\n          \"key\": \"ExpirationDate\",\n          \"value\": \"2017-07-10\"\n        }\n      ],\n      \"securityGroups\": [\n        {\n          \"groupName\": \"gaurav-test-sg\",\n          \"groupId\": \"sg-da9da1aa\"\n        }\n      ],\n      \"sourceDestCheck\": true,\n      \"hypervisor\": \"xen\",\n      \"networkInterfaces\": [\n        {\n          \"networkInterfaceId\": \"eni-3cc64fd2\",\n          \"subnetId\": \"subnet-e41559ad\",\n          \"vpcId\": \"vpc-a02ce1c6\",\n          \"description\": \"Primary network interface\",\n          \"ownerId\": \"411815166437\",\n          \"status\": \"in-use\",\n          \"macAddress\": \"0a:18:41:09:07:34\",\n          \"privateIpAddress\": \"10.16.3.63\",\n          \"privateDnsName\": \"ip-10-16-3-63.ec2.internal\",\n          \"sourceDestCheck\": true,\n          \"groups\": [\n            {\n              \"groupName\": \"launch-wizard-92\",\n              \"groupId\": \"sg-da9da1aa\"\n            }\n          ],\n          \"attachment\": {\n            \"attachmentId\": \"eni-attach-29cd5d69\",\n            \"deviceIndex\": 0,\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:10.000Z\",\n            \"deleteOnTermination\": true\n          },\n          \"association\": null,\n          \"privateIpAddresses\": [\n            {\n              \"privateIpAddress\": \"10.16.3.63\",\n              \"privateDnsName\": \"ip-10-16-3-63.ec2.internal\",\n              \"primary\": true,\n              \"association\": null\n            }\n          ],\n          \"ipv6Addresses\": []\n        }\n      ],\n      \"iamInstanceProfile\": {\n        \"arn\": \"arn:aws:iam::411815166437:instance-profile/jenkins_master_noel.georgi\",\n        \"id\": \"AIPAJ4KIXV5QRL25MMMCK\"\n      },\n      \"ebsOptimized\": false,\n      \"sriovNetSupport\": null,\n      \"enaSupport\": null\n    },\n    \"supplementaryConfiguration\": {},\n    \"tags\": {\n      \"Project\": \"mnc\",\n      \"Owner\": \"gaurav.ashtikar\",\n      \"ExpirationDate\": \"2017-07-11\",\n      \"Environment\": \"Testing\",\n      \"NoShutdown\": \"true\",\n      \"Name\": \"Gaurav-Test-Machine\"\n    },\n    \"configurationItemVersion\": \"1.2\",\n    \"configurationItemCaptureTime\": \"2017-05-18T18:47:14.686Z\",\n    \"configurationStateId\": 1495133234686,\n    \"awsAccountId\": \"411815166437\",\n    \"configurationItemStatus\": \"OK\",\n    \"resourceType\": \"AWS::EC2::Instance\",\n    \"resourceId\": \"i-098f9826f1ee4072d\",\n    \"resourceName\": null,\n    \"ARN\": \"arn:aws:ec2:us-east-1:411815166437:instance/i-098f9826f1ee4072d\",\n    \"awsRegion\": \"us-east-1\",\n    \"availabilityZone\": \"us-east-1b\",\n    \"configurationStateMd5Hash\": \"ed5fe5d85665e3be3607c27aa50fa0ea\",\n    \"resourceCreationTime\": \"2017-05-13T14:14:48.000Z\"\n  },\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ConfigurationItemChangeNotification\",\n  \"recordVersion\": \"1.2\"\n}",
    "resultToken": "",
    "eventLeftScope": "False",
    "ruleParameters": "{\"actionName\": \"CopyEbsTagsToSnapshotsAction\", \"evaluateName\": \"CopyEbsTagsToSnapshotsEvaluate\", \"resourceFetcherName\" :\"CopyEbsTagsToSnapshotsResourceFetcher\",\"tagsToCopy\": \"Name\", \n \"notifier\":\"email\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
    "executionRoleArn": "arn:aws:iam::411815166437:role/awsconfig-role",
    "accountId": "411815166437"
}

responseSnapshots = {
    'snapshots': [
        {
            'snapshotid': 'snap-1234321',
            'tags': [
                {
                    'key': 'Name',
                    'value': 'test'
                }
            ]
        }
    ]
}

responseSnapshotsFailure = {
    'snapshots': [
        {
            'snapshotid': 'snap-1234321',
            'tags': [
                {
                    'key': 'name',
                    'value': 'test'
                }
            ]
        }
    ]
}


class TestCopyEbsTagsToSnapshotsEvaluate(object):
    __regions = ['us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']

    __eventParam = cof.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __copyEBS = copyEBS.CopyEbsTagsToSnapshotsEvaluate(__eventParam)

    def testEvaluationNotApplicable(self):
        evaluationResult = EvaluationResult()
        configItems = {'volumeid': '123454321'}
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItems)
        return_value = self.__copyEBS.evaluate(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

    def testEvaluationException(self):
        evaluationResult = EvaluationResult()
        configItems = {'volumeid': '123454321', 'tags': []}
        ec2client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__regions[0])
        copyEBS.BotoUtility.getClient = MagicMock(return_value=ec2client)
        ec2client.describe_snapshots = MagicMock(return_value=Exception)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId="", resourceType=RESOURCE_TYPE, configItems=configItems)
        return_value = self.__copyEBS.evaluate(eventItem)
        assert return_value.complianceType == ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE

    def testEvaluationSucess(self):
        evaluationResult = EvaluationResult()
        configItems = {'volumeid': '123454321', 'tags': [
            {
                'key': 'Name',
                'value': 'Test'
            }
        ]}
        ec2client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__regions[0])
        copyEBS.BotoUtility.getClient = MagicMock(return_value=ec2client)
        ec2client.describe_snapshots = MagicMock(return_value=responseSnapshots)
        self._CopyEbsTagToSnapshotsEvaluate__get_tags_hash = MagicMock(return_value=True)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItems)
        return_value = self.__copyEBS.evaluate(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testEvaluationFailure(self):
        evaluationResult = EvaluationResult()
        configItems = {'volumeid': '123454321', 'tags': [
            {
                'key': 'Name',
                'value': 'Test'
            }
        ]}
        ec2client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__regions[0])
        copyEBS.BotoUtility.getClient = MagicMock(return_value=ec2client)
        ec2client.describe_snapshots = MagicMock(return_value=responseSnapshotsFailure)
        self._CopyEbsTagToSnapshotsEvaluate__get_tags_hash = MagicMock(return_value=True)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=configItems)
        return_value = self.__copyEBS.evaluate(eventItem)
        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
