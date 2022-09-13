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
import boto3
sys.path.append('../../')

from unencrypted_ebs.unencrypted_ebs_resource_fetcher import *
import common.compliance_object_factory as complianceobjectfactory
import unittest
from mock import MagicMock
from moto import mock_ec2

EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"configurationItemDiff\": {\"changedProperties\": {},\"changeType\": \"CREATE\"},\"configurationItem\": {\"relatedEvents\": [],\"relationships\": [],\"configuration\": {\"attachments\": [],\"availabilityZone\": \"us-east-1a\",\"createTime\": \"2018-02-26T14:52:02.249Z\",\"encrypted\": false,\"kmsKeyId\": null,\"size\": 1,\"snapshotId\": \"\",\"state\": \"available\",\"volumeId\": \"vol-0fe1c72bb04d6785a\",\"iops\": 100,\"tags\": [{\"key\": \"name\", \"value\": \"mncTest\"},{\"key\": \"Owner\", \"value\": \"devendra.suthar\"},{\"key\": \"project\", \"value\": \"mnc\"},{\"key\": \"environment\", \"value\": \"testing\"}],\"volumeType\": \"gp2\"},\"supplementaryConfiguration\": {},\"tags\": {},\"configurationItemVersion\": \"1.3\",\"configurationItemCaptureTime\": \"2018-02-26T14:55:07.816Z\",\"configurationStateId\": 1519656907816,\"awsAccountId\": \"693265998683\",\"configurationItemStatus\": \"ResourceDiscovered\",\"resourceType\": \"AWS::EC2::Volume\",\"resourceId\": \"vol-0fe1c72bb04d6785a\",\"resourceName\": null,\"ARN\": \"arn:aws:ec2:us-east-1:693265998683:volume/vol-0fe1c72bb04d6785a\",\"awsRegion\": \"us-east-1\",\"availabilityZone\": \"us-east-1a\",\"configurationStateMd5Hash\": \"\",\"resourceCreationTime\": \"2018-02-26T14:52:02.249Z\"},\"notificationCreationTime\": \"2018-02-26T14:55:08.008Z\",\"messageType\": \"ConfigurationItemChangeNotification\",\"recordVersion\": \"1.3\"}",
    "ruleParameters": "{\"customerName\":\"MNC-Client\",\"performAction\": \"False\", \"actionName\": \"UnencryptedEbsAction\", \"evaluateName\": \"UnencryptedEbsEvaluate\",   \"resourceFetcherName\" : \"UnencryptedEbsResourceFetcher\",  \"moduleName\": \"unencrypted_ebs\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\"}",
    "resultToken": "",
    "configRuleName": "unencrypted_ebs",
    "configRuleId": "config-rule-nvphxd",
    "accountId": "693265998683",
    "executionRoleArn": "arn:aws:iam::411815166437:role/awsconfig-role",
    "configRuleArn": "arn:aws:config:us-east-1:411815166437:config-rule/config-rule-1v52mx"
}

CONTEXT = ""


class TestUnencryptedEbsFetcher(unittest.TestCase):
    _AbstractResourceFetcher__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __awsRegion = "us-east-1"
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __mockResponse = {'Volumes': [
            {'Encrypted': "False", 'VolumeId': 'vol-0a8dd6aa5bc3ddd57', 'Tags': [
                {'Key': 'Owner', 'Value': 'devendra'
                 },
                {'Key': 'Name', 'Value': 'testEC2'
                 }
            ]
             }
        ]
    }

    __ebsResourceFetcher = UnencryptedEbsResourceFetcher(__eventParam)

    @mock_ec2
    def testResourceFetcher(self):
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__awsRegion)
        BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_volumes = MagicMock(return_value=self.__mockResponse)
        return_value = self.__ebsResourceFetcher.resourceFetcher()
        assert bool(return_value) == True

    @mock_ec2
    def testResourceFetcherFailure(self):
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__awsRegion)
        BotoUtility.getClient = MagicMock(return_value=ec2Client)
        ec2Client.describe_volumes = MagicMock(side_effect=Exception("Failed to fetch resource details"))
        return_value = UnencryptedEbsResourceFetcher.resourceFetcher(self)
        assert bool(return_value) == False