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
""" Test class for delete_old_ami rule resource fetcher"""
import sys
import boto3
import delete_old_ami.delete_old_ami_resource_fetcher as amiFetcher
import common.compliance_object_factory as complianceobjectfactory
from common.common_constants import BotoConstants
from mock import MagicMock
# from moto import mock_ec2, mock_autoscaling


sys.path.append('../../')


CONTEXT = ""

EVENT_JSON = {
    "configRuleId": "config-rule-1v52mx",
    "version": "1.0",
    "configRuleName": "delete_old_ami",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-1v52mx",
    "invokingEvent": "{\n  \"configurationItemDiff\": null, \n  \"configurationItem\": {\n    \"relatedEvents\": [],\n    \"relationships\": [\n      {\n        \"resourceId\": \"eni-3cc64fd2\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::AMI\",\n        \"name\": \"Contains NetworkInterface\"\n      },\n      {\n        \"resourceId\": \"sg-056a2f78\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"sg-c500e8ba\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"subnet-e41559ad\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Subnet\",\n        \"name\": \"Is contained in Subnet\"\n      },\n      {\n        \"resourceId\": \"vol-03807f5f89a1b3d0b\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Volume\",\n        \"name\": \"Is attached to Volume\"\n      },\n      {\n        \"resourceId\": \"vpc-a02ce1c6\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::VPC\",\n        \"name\": \"Is contained in Vpc\"\n      }\n    ],\n    \"configuration\": {\n      \"instanceId\": \"i-0d735363112477190\",\n      \"imageId\": \"ami-a4c7edb2\",\n      \"state\": {\n        \"code\": 16,\n        \"name\": \"running\"\n      },\n      \"privateDnsName\": \"ip-172-31-28-156.ec2.internal\",\n      \"publicDnsName\": \"ec2-54-235-57-47.compute-1.amazonaws.com\",\n      \"stateTransitionReason\": \"\",\n      \"keyName\": \"REAN_GAURAVASHTIKAR_VIRGINIA_KEYPAIR\",\n      \"amiLaunchIndex\": 0,\n      \"productCodes\": [],\n      \"instanceType\": \"t2.nano\",\n      \"launchTime\": \"2017-07-09T17:34:48.000Z\",\n      \"placement\": {\n        \"availabilityZone\": \"us-east-1b\",\n        \"groupName\": \"\",\n        \"tenancy\": \"default\",\n        \"hostId\": null,\n        \"affinity\": null\n      },\n      \"kernelId\": null,\n      \"ramdiskId\": null,\n      \"platform\": null,\n      \"monitoring\": {\n        \"state\": \"disabled\"\n      },\n      \"subnetId\": \"subnet-29aa575e\",\n      \"vpcId\": \"vpc-c5ec30a0\",\n      \"privateIpAddress\": \"172.31.28.156\",\n      \"publicIpAddress\": \"54.235.57.47\",\n      \"stateReason\": null,\n      \"architecture\": \"x86_64\",\n      \"rootDeviceType\": \"ebs\",\n      \"rootDeviceName\": \"/dev/sda1\",\n      \"blockDeviceMappings\": [\n        {\n          \"deviceName\": \"/dev/sda1\",\n          \"ebs\": {\n            \"volumeId\": \"vol-0bc42d36aa49858fd\",\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:11.000Z\",\n            \"deleteOnTermination\": true\n          }\n        }\n      ],\n      \"virtualizationType\": \"hvm\",\n      \"instanceLifecycle\": null,\n      \"spotInstanceRequestId\": null,\n      \"clientToken\": \"FSRse1484029749587\",\n      \"tags\": [\n        {\n          \"key\": \"Project\",\n          \"value\": \"mnc\"\n        },\n        {\n          \"key\": \"Environment\",\n          \"value\": \"Testing\"\n        },\n        {\n          \"key\": \"Owner\",\n          \"value\": \"gaurav.ashtikar\"\n        },\n        {\n          \"key\": \"Name\",\n          \"value\": \"Gaurav-Test-Machine\"\n        },\n        {\n          \"value\": \"NoShutdown\",\n          \"key\": \"true\"\n        },\n        {\n          \"key\": \"ExpirationDate\",\n          \"value\": \"2017-07-10\"\n        }\n      ],\n      \"securityGroups\": [\n        {\n          \"groupName\": \"gaurav-test-sg\",\n          \"groupId\": \"sg-cc9efcbd\"\n        }\n      ],\n      \"sourceDestCheck\": true,\n      \"hypervisor\": \"xen\",\n      \"networkInterfaces\": [\n        {\n          \"networkInterfaceId\": \"eni-3cc64fd2\",\n          \"subnetId\": \"subnet-e41559ad\",\n          \"vpcId\": \"vpc-a02ce1c6\",\n          \"description\": \"Primary network interface\",\n          \"ownerId\": \"411815166437\",\n          \"status\": \"in-use\",\n          \"macAddress\": \"0a:18:41:09:07:34\",\n          \"privateIpAddress\": \"10.16.3.63\",\n          \"privateDnsName\": \"ip-10-16-3-63.ec2.internal\",\n          \"sourceDestCheck\": true,\n          \"groups\": [\n            {\n              \"groupName\": \"launch-wizard-92\",\n              \"groupId\": \"sg-c500e8ba\"\n            },\n            {\n              \"groupName\": \"jenkins_sg_allow\",\n              \"groupId\": \"sg-056a2f78\"\n            }\n          ],\n          \"attachment\": {\n            \"attachmentId\": \"eni-attach-29cd5d69\",\n            \"deviceIndex\": 0,\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:10.000Z\",\n            \"deleteOnTermination\": true\n          },\n          \"association\": null,\n          \"privateIpAddresses\": [\n            {\n              \"privateIpAddress\": \"10.16.3.63\",\n              \"privateDnsName\": \"ip-10-16-3-63.ec2.internal\",\n              \"primary\": true,\n              \"association\": null\n            }\n          ],\n          \"ipv6Addresses\": []\n        }\n      ],\n      \"iamInstanceProfile\": {\n        \"arn\": \"arn:aws:iam::411815166437:instance-profile/jenkins_master_noel.georgi\",\n        \"id\": \"AIPAJ4KIXV5QRL25MMMCK\"\n      },\n      \"ebsOptimized\": false,\n      \"sriovNetSupport\": null,\n      \"enaSupport\": null\n    },\n    \"supplementaryConfiguration\": {},\n    \"tags\": {\n      \"Project\": \"mnc\",\n      \"Owner\": \"gaurav.ashtikar\",\n      \"ExpirationDate\": \"2017-07-11\",\n      \"Environment\": \"Testing\",\n      \"NoShutdown\": \"true\",\n      \"Name\": \"Gaurav-Test-Machine\"\n    },\n    \"configurationItemVersion\": \"1.2\",\n    \"configurationItemCaptureTime\": \"2017-05-18T18:47:14.686Z\",\n    \"configurationStateId\": 1495133234686,\n    \"awsAccountId\": \"411815166437\",\n    \"configurationItemStatus\": \"OK\",\n    \"resourceType\": \"AWS::EC2::Instance\",\n    \"resourceId\": \"i-0d735363112477190\",\n    \"resourceName\": null,\n    \"ARN\": \"arn:aws:ec2:us-east-1:411815166437:instance/i-0250bff57b217c421\",\n    \"awsRegion\": \"us-east-1\",\n    \"availabilityZone\": \"us-east-1b\",\n    \"configurationStateMd5Hash\": \"ed5fe5d85665e3be3607c27aa50fa0ea\",\n    \"resourceCreationTime\": \"2017-05-13T14:14:48.000Z\"\n  },\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
    "resultToken": "",
    "ruleParameters": "{ \"amiValidForDays\": \"90\",\"actionName\": \"DeleteOldAMIAction\",\"evaluateName\": \"DeleteOldAMIEvaluate\",\"resourceFetcherName\": \"DeleteOldAMIResourceFetcher\",\"age\":\"0\",\n \"notifier\":\"email\",\n \"toEmail\": \"vaibhav.menkudale@reancloud.com\",\n \"ccEmail\": \"vaibhav.menkudale@reancloud.com\",\n  \"performAction\": \"True\" }",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/awsconfig-role",
    "accountId": "107339370656"
}


class TestDeleteOldAMIResourceFetcher(object):
    """ Test cases for delete_old_ami rule """

# def readFileToJson(self,filename):
#       with open(filename, encoding='utf-8') as filedata:
#         jsonVal= json.loads(filedata.read())
#       return jsonVal

    __mockResponseForAllAMI = {'Images': [{'ImageId': 'ami-8ac59ef5', 'ImageLocation': '107339370656/vaibhavTestMNC6', 'State': 'available', 'OwnerId': '107339370656', 'CreationDate': '2018-06-29T10:45:16.000Z', 'Public': False, 'Architecture': 'x86_64', 'ImageType': 'machine', 'SriovNetSupport': 'simple', 'EnaSupport': True, 'Name': 'vaibhavTestMNC6', 'Description': 'vaibhavTestMNC6', 'RootDeviceType': 'ebs', 'RootDeviceName': '/dev/sda1', 'BlockDeviceMappings': [{'DeviceName': '/dev/sda1', 'Ebs': {'SnapshotId': 'snap-04fbf8aa71a4e022d', 'VolumeSize': 8, 'DeleteOnTermination': True, 'VolumeType': 'gp2', 'Encrypted': False}}], 'VirtualizationType': 'hvm', 'Hypervisor': 'xen'}, {'ImageId': 'ami-b69dc3c9', 'ImageLocation': '107339370656/vsmImg1', 'State': 'available', 'OwnerId': '107339370656', 'CreationDate': '2018-06-27T13:36:43.000Z', 'Public': False, 'Architecture': 'x86_64', 'ImageType': 'machine', 'SriovNetSupport': 'simple', 'EnaSupport': True, 'Name': 'vsmImg1', 'Description': 'mncTest', 'RootDeviceType': 'ebs', 'RootDeviceName': '/dev/sda1', 'BlockDeviceMappings': [{'DeviceName': '/dev/sda1', 'Ebs': {'SnapshotId': 'snap-05164522419ee42e1', 'VolumeSize': 8, 'DeleteOnTermination': True, 'VolumeType': 'gp2', 'Encrypted': False}}], 'VirtualizationType': 'hvm', 'Tags': [{'Key': 'doNotDelete', 'Value': 'True'}], 'Hypervisor': 'xen'}, {'ImageId': 'ami-d75575a8', 'ImageLocation': '107339370656/mncTestVsm10', 'State': 'available', 'OwnerId': '107339370656', 'CreationDate': '2018-07-03T08:14:50.000Z', 'Public': False, 'Architecture': 'x86_64', 'ImageType': 'machine', 'SriovNetSupport': 'simple', 'EnaSupport': True, 'Name': 'mncTestVsm10', 'Description': 'for ami test', 'RootDeviceType': 'ebs', 'RootDeviceName': '/dev/xvda', 'BlockDeviceMappings': [{'DeviceName': '/dev/xvda', 'Ebs': {'SnapshotId': 'snap-0dc982350c106d4ba', 'VolumeSize': 8, 'DeleteOnTermination': True, 'VolumeType': 'gp2', 'Encrypted': False}}], 'VirtualizationType': 'hvm', 'Hypervisor': 'xen'}], 'ResponseMetadata': {'RequestId': 'c6f4d19a-f16d-44a3-8953-3b9226608b50', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'text/xml;charset=UTF-8', 'content-length': '4458', 'vary': 'Accept-Encoding', 'date': 'Tue, 03 Jul 2018 08:17:38 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}

    __mockResponseforDoNotDeleteTag = {'Images': [{'ImageId': 'ami-b69dc3c9', 'ImageLocation': '107339370656/vsmImg1', 'State': 'available', 'OwnerId': '107339370656', 'CreationDate': '2018-06-27T13:36:43.000Z', 'Public': False, 'Architecture': 'x86_64', 'ImageType': 'machine', 'SriovNetSupport': 'simple', 'EnaSupport': True, 'Name': 'vsmImg1', 'Description': 'mncTest', 'RootDeviceType': 'ebs', 'RootDeviceName': '/dev/sda1', 'BlockDeviceMappings': [{'DeviceName': '/dev/sda1', 'Ebs': {'SnapshotId': 'snap-05164522419ee42e1', 'VolumeSize': 8, 'DeleteOnTermination': True, 'VolumeType': 'gp2', 'Encrypted': False}}], 'VirtualizationType': 'hvm', 'Tags': [{'Key': 'doNotDelete', 'Value': 'True'}], 'Hypervisor': 'xen'}], 'ResponseMetadata': {'RequestId': '99bcad30-57e1-4e07-869a-3a0e15d2eaea', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'text/xml;charset=UTF-8', 'content-length': '1745', 'date': 'Tue, 03 Jul 2018 08:16:51 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}

    __mockResponseLC = {'LaunchConfigurations': [{'LaunchConfigurationName': 'VSm', 'LaunchConfigurationARN': 'arn:aws:autoscaling:us-east-1:107339370656:launchConfiguration:f9d8a2b9-97c2-48b1-8a45-ce13d065d023:launchConfigurationName/VSm', 'ImageId': 'ami-1e174f61', 'KeyName': 'vaibhavMncMaster', 'SecurityGroups': ['sg-52c9b419'], 'ClassicLinkVPCSecurityGroups': [], 'UserData': '', 'InstanceType': 't2.micro', 'KernelId': '', 'RamdiskId': '', 'BlockDeviceMappings': [{'DeviceName': '/dev/sda1', 'Ebs': {'SnapshotId': 'snap-096ef093205a3918e', 'VolumeSize': 8, 'VolumeType': 'gp2', 'DeleteOnTermination': True}}], 'InstanceMonitoring': {'Enabled': False}, 'CreatedTime': '2018-06-28T12:25:16.000Z', 'EbsOptimized': False}], 'ResponseMetadata': {'RequestId': 'ddc28966-7e99-11e8-8324-75daf5c5c260', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'ddc28966-7e99-11e8-8324-75daf5c5c260', 'content-type': 'text/xml', 'content-length': '1566', 'date': 'Tue, 03 Jul 2018 08:19:54 GMT'}, 'RetryAttempts': 0}}

    # __regions = ['ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __regions = ['us-east-1']
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __deleteOldAmiResourceFetcher = amiFetcher.DeleteOldAMIResourceFetcher(__eventParam)

# @mock_autoscaling
# @mock_ec2
# def testResourceFetcher(self):
#     """ OK """

#         # lcImages = []['ami-1e174f61']


#     # autoScalingClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ASC, self.__regions[0])
#     # amiFetcher.BotoUtility.getClient = MagicMock(return_value=autoScalingClient)
#     # autoScalingClient.describe_launch_configurations = MagicMock(return_value=self.__mockResponseLC)
#     # amiFetcher.BotoUtility.getClient = MagicMock(side_effect=[ec2Client,autoScalingClient])


#     ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
#     # amiFetcher.regionsEc2 = MagicMock(return_value = ['us-east-1'])

#     self.__getLaunchConfigAMIList = MagicMock(return_value=['ami-1e174f61'])

#     ec2Client.describe_images = MagicMock(return_value=self.__mockResponseForAllAMI)
#     amiFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)

#     # amiFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)

#     return_value = self.__deleteOldAmiResourceFetcher.resourceFetcher()
#     print('xxx', return_value)
#     assert bool(return_value) == True


# mock=mock_autoscaling()
# mock.start()
# mock.stop()
# mock=mock_ec2()
# mock.start()
# mock.stop()

#  @mock_ec2
#     def testResourceFetcher(self):
#         eniFetcher.regions = MagicMock(return_value = self.__regions)
#         ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, self.__regions[0])
#         eniFetcher.BotoUtility.getClient = MagicMock(return_value=ec2Client)
#         ec2Client.describe_network_interfaces = MagicMock(return_value=self.__mockResponse)
#         return_value = self.__deleteEC2UnusedENIsResourceFetcher.resourceFetcher()
#         assert bool(return_value) == True

    # @mock_autoscaling
    def testGetLC(self):
        """ OK """

        # with self.assertRaises(AttributeError):

        autoScalingClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_ASC, self.__regions[0])
        amiFetcher.BotoUtility.getClient = MagicMock(return_value=autoScalingClient)
        autoScalingClient.describe_launch_configurations = MagicMock(return_value=self.__mockResponseLC)
        amiFetcher.BotoUtility.getClient = MagicMock(side_effect=[autoScalingClient])

        # return_value = self.__deleteOldAmiResourceFetcher.__getLaunchConfigAMIList()

        # assert True == True
