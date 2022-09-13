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
""" Test class for delete_old_ami rule action class"""
import sys
import boto3
import delete_old_ami.delete_old_ami_action as deleteAMIAction
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.i18n import Translation as _
from common.common_constants import BotoConstants, ComplianceConstants
from mock import MagicMock
from moto import mock_ec2
sys.path.append('../../')


RESOURCE_ID = "ami-d75575a8"

EVENT_JSON = {
    "configRuleId": "config-rule-1v52mx",
    "version": "1.0",
    "configRuleName": "delete_old_ami",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-1v52mx",
    "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"configurationItem\": {\n    \"relatedEvents\": [],\n    \"relationships\": [\n      {\n        \"resourceId\": \"eni-3cc64fd2\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::AMI\",\n        \"name\": \"Contains NetworkInterface\"\n      },\n      {\n        \"resourceId\": \"sg-056a2f78\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"sg-c500e8ba\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"subnet-e41559ad\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Subnet\",\n        \"name\": \"Is contained in Subnet\"\n      },\n      {\n        \"resourceId\": \"vol-03807f5f89a1b3d0b\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Volume\",\n        \"name\": \"Is attached to Volume\"\n      },\n      {\n        \"resourceId\": \"vpc-a02ce1c6\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::VPC\",\n        \"name\": \"Is contained in Vpc\"\n      }\n    ],\n    \"configuration\": {\n      \"instanceId\": \"i-0d735363112477190\",\n      \"imageId\": \"ami-a4c7edb2\",\n      \"state\": {\n        \"code\": 16,\n        \"name\": \"running\"\n      },\n      \"privateDnsName\": \"ip-172-31-28-156.ec2.internal\",\n      \"publicDnsName\": \"ec2-54-235-57-47.compute-1.amazonaws.com\",\n      \"stateTransitionReason\": \"\",\n      \"keyName\": \"REAN_GAURAVASHTIKAR_VIRGINIA_KEYPAIR\",\n      \"amiLaunchIndex\": 0,\n      \"productCodes\": [],\n      \"instanceType\": \"t2.nano\",\n      \"launchTime\": \"2017-07-09T17:34:48.000Z\",\n      \"placement\": {\n        \"availabilityZone\": \"us-east-1b\",\n        \"groupName\": \"\",\n        \"tenancy\": \"default\",\n        \"hostId\": null,\n        \"affinity\": null\n      },\n      \"kernelId\": null,\n      \"ramdiskId\": null,\n      \"platform\": null,\n      \"monitoring\": {\n        \"state\": \"disabled\"\n      },\n      \"subnetId\": \"subnet-29aa575e\",\n      \"vpcId\": \"vpc-c5ec30a0\",\n      \"privateIpAddress\": \"172.31.28.156\",\n      \"publicIpAddress\": \"54.235.57.47\",\n      \"stateReason\": null,\n      \"architecture\": \"x86_64\",\n      \"rootDeviceType\": \"ebs\",\n      \"rootDeviceName\": \"/dev/sda1\",\n      \"blockDeviceMappings\": [\n        {\n          \"deviceName\": \"/dev/sda1\",\n          \"ebs\": {\n            \"volumeId\": \"vol-0bc42d36aa49858fd\",\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:11.000Z\",\n            \"deleteOnTermination\": true\n          }\n        }\n      ],\n      \"virtualizationType\": \"hvm\",\n      \"instanceLifecycle\": null,\n      \"spotInstanceRequestId\": null,\n      \"clientToken\": \"FSRse1484029749587\",\n      \"tags\": [\n        {\n          \"key\": \"Project\",\n          \"value\": \"mnc\"\n        },\n        {\n          \"key\": \"Environment\",\n          \"value\": \"Testing\"\n        },\n        {\n          \"key\": \"Owner\",\n          \"value\": \"gaurav.ashtikar\"\n        },\n        {\n          \"key\": \"Name\",\n          \"value\": \"Gaurav-Test-Machine\"\n        },\n        {\n          \"value\": \"NoShutdown\",\n          \"key\": \"true\"\n        },\n        {\n          \"key\": \"ExpirationDate\",\n          \"value\": \"2017-07-10\"\n        }\n      ],\n      \"securityGroups\": [\n        {\n          \"groupName\": \"gaurav-test-sg\",\n          \"groupId\": \"sg-cc9efcbd\"\n        }\n      ],\n      \"sourceDestCheck\": true,\n      \"hypervisor\": \"xen\",\n      \"networkInterfaces\": [\n        {\n          \"networkInterfaceId\": \"eni-3cc64fd2\",\n          \"subnetId\": \"subnet-e41559ad\",\n          \"vpcId\": \"vpc-a02ce1c6\",\n          \"description\": \"Primary network interface\",\n          \"ownerId\": \"411815166437\",\n          \"status\": \"in-use\",\n          \"macAddress\": \"0a:18:41:09:07:34\",\n          \"privateIpAddress\": \"10.16.3.63\",\n          \"privateDnsName\": \"ip-10-16-3-63.ec2.internal\",\n          \"sourceDestCheck\": true,\n          \"groups\": [\n            {\n              \"groupName\": \"launch-wizard-92\",\n              \"groupId\": \"sg-c500e8ba\"\n            },\n            {\n              \"groupName\": \"jenkins_sg_allow\",\n              \"groupId\": \"sg-056a2f78\"\n            }\n          ],\n          \"attachment\": {\n            \"attachmentId\": \"eni-attach-29cd5d69\",\n            \"deviceIndex\": 0,\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:10.000Z\",\n            \"deleteOnTermination\": true\n          },\n          \"association\": null,\n          \"privateIpAddresses\": [\n            {\n              \"privateIpAddress\": \"10.16.3.63\",\n              \"privateDnsName\": \"ip-10-16-3-63.ec2.internal\",\n              \"primary\": true,\n              \"association\": null\n            }\n          ],\n          \"ipv6Addresses\": []\n        }\n      ],\n      \"iamInstanceProfile\": {\n        \"arn\": \"arn:aws:iam::411815166437:instance-profile/jenkins_master_noel.georgi\",\n        \"id\": \"AIPAJ4KIXV5QRL25MMMCK\"\n      },\n      \"ebsOptimized\": false,\n      \"sriovNetSupport\": null,\n      \"enaSupport\": null\n    },\n    \"supplementaryConfiguration\": {},\n    \"tags\": {\n      \"Project\": \"mnc\",\n      \"Owner\": \"gaurav.ashtikar\",\n      \"ExpirationDate\": \"2017-07-11\",\n      \"Environment\": \"Testing\",\n      \"NoShutdown\": \"true\",\n      \"Name\": \"Gaurav-Test-Machine\"\n    },\n    \"configurationItemVersion\": \"1.2\",\n    \"configurationItemCaptureTime\": \"2017-05-18T18:47:14.686Z\",\n    \"configurationStateId\": 1495133234686,\n    \"awsAccountId\": \"411815166437\",\n    \"configurationItemStatus\": \"OK\",\n    \"resourceType\": \"AWS::EC2::Instance\",\n    \"resourceId\": \"i-0d735363112477190\",\n    \"resourceName\": null,\n    \"ARN\": \"arn:aws:ec2:us-east-1:411815166437:instance/i-0250bff57b217c421\",\n    \"awsRegion\": \"us-east-1\",\n    \"availabilityZone\": \"us-east-1b\",\n    \"configurationStateMd5Hash\": \"ed5fe5d85665e3be3607c27aa50fa0ea\",\n    \"resourceCreationTime\": \"2017-05-13T14:14:48.000Z\"\n  },\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
    "resultToken": "",
    "ruleParameters": "{ \"amiValidForDays\": \"90\",\"actionName\": \"DeleteOldAMIAction\",\"evaluateName\": \"DeleteOldAMIEvaluate\",\"resourceFetcherName\": \"DeleteOldAMIResourceFetcher\",\"age\":\"0\",\n \"notifier\":\"email\",\n \"toEmail\": \"vaibhav.menkudale@reancloud.com\",\n \"ccEmail\": \"vaibhav.menkudale@reancloud.com\",\n  \"performAction\": \"True\" }",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/awsconfig-role",
    "accountId": "107339370656"
}

CONTEXT = ""


class TestUnusedNetworkInterfacesAction(object):
    """ Test cases for Delete Old AMI rule Action class"""

    __awsRegion = "us-east-1"

    @mock_ec2
    def testPerformActionWithCorrectResponse(self):
        """ Test case with correct response """
        self._AbstractAction__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )

        configItems = {"imageid": RESOURCE_ID, "blockdevicemappings": [{"devicename": "/dev/sda1", "ebs": {"encrypted": False, "deleteontermination": True, "snapshotid": "snap-04fbf8aa71a4e022d", "volumesize": 8, "volumetype": "gp2"}}]}
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, configItems=configItems)
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__awsRegion)
        deleteAMIAction.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        mockResponseDeregisterImage = {'ResponseMetadata': {'RequestId': 'b3c6ac99-172b-41c3-ad13-a9395e1103c2',
                                                            'HTTPStatusCode': 200,
                                                            'HTTPHeaders': {'content-type': 'text/xml;charset=UTF-8',
                                                                            'content-length': '231',
                                                                            'date': 'Fri, 06 Jul 2018 11:23:12 GMT',
                                                                            'server': 'AmazonEC2'},
                                                            'RetryAttempts': 0}}

        mockResponseDeleteSnapshots = {'ResponseMetadata': {'RequestId': '05f58e97-e3eb-4dd5-887a-36bf928659b8',
                                                            'HTTPStatusCode': 200,
                                                            'HTTPHeaders': {'content-type': 'text/xml;charset=UTF-8',
                                                                            'content-length': '229',
                                                                            'date': 'Fri, 06 Jul 2018 11:27:45 GMT',
                                                                            'server': 'AmazonEC2'},
                                                            'RetryAttempts': 0}}

        ec2Client.deregister_image = MagicMock(return_value=mockResponseDeregisterImage)
        ec2Client.delete_snapshot = MagicMock(return_value=mockResponseDeleteSnapshots)
        return_value = deleteAMIAction.DeleteOldAMIAction.performAction(self, eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

    def testPerformActionWithFailureResponseInDeregisteringAMI(self):
        """ Test case with failure while deregistering AMI. """
        self._AbstractAction__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
        imageId = RESOURCE_ID

        configItems = {"imageid": RESOURCE_ID, "blockdevicemappings": [{"devicename": "/dev/sda1", "ebs": {"encrypted": False, "deleteontermination": True, "snapshotid": "snap-04fbf8aa71a4e022d", "volumesize": 8, "volumetype": "gp2"}}]}
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, configItems=configItems)
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__awsRegion)
        deleteAMIAction.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        mockResponseDeregisterImage = {'ResponseMetadata': {'RequestId': 'b3c6ac99-172b-41c3-ad13-a9395e1103c2',
                                                            'HTTPStatusCode': 400,
                                                            'HTTPHeaders': {'content-type': 'text/xml;charset=UTF-8',
                                                                            'content-length': '231',
                                                                            'date': 'Fri, 06 Jul 2018 11:23:12 GMT',
                                                                            'server': 'AmazonEC2'},
                                                            'RetryAttempts': 0}}

        mockResponseDeleteSnapshots = {'ResponseMetadata': {'RequestId': '05f58e97-e3eb-4dd5-887a-36bf928659b8',
                                                            'HTTPStatusCode': 200,
                                                            'HTTPHeaders': {'content-type': 'text/xml;charset=UTF-8',
                                                                            'content-length': '229',
                                                                            'date': 'Fri, 06 Jul 2018 11:27:45 GMT',
                                                                            'server': 'AmazonEC2'},
                                                            'RetryAttempts': 0}}

        ec2Client.deregister_image = MagicMock(return_value=mockResponseDeregisterImage)
        ec2Client.delete_snapshot = MagicMock(return_value=mockResponseDeleteSnapshots)
        return_value = deleteAMIAction.DeleteOldAMIAction.performAction(self, eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION and return_value.annotation == _("Unable to deregister AMI id : {} and hence associated AMI Snapshots are not deleted.".format(imageId))

    def testPerformActionWithFailureResponseInDeletingSnapshot(self):
        """ Test case while deleting snapshot. """
        self._AbstractAction__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            EVENT_JSON,
            CONTEXT
        )
        imageId = RESOURCE_ID
        notDeletedSnapshotIds = ['snap-04fbf8aa71a4e022d']

        configItems = {"imageid": RESOURCE_ID, "blockdevicemappings": [{"devicename": "/dev/sda1", "ebs": {"encrypted": False, "deleteontermination": True, "snapshotid": "snap-04fbf8aa71a4e022d", "volumesize": 8, "volumetype": "gp2"}}]}
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, configItems=configItems)
        ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2, region_name=self.__awsRegion)
        deleteAMIAction.BotoUtility.getClient = MagicMock(return_value=ec2Client)
        mockResponseDeregisterImage = {'ResponseMetadata': {'RequestId': 'b3c6ac99-172b-41c3-ad13-a9395e1103c2',
                                                            'HTTPStatusCode': 200,
                                                            'HTTPHeaders': {'content-type': 'text/xml;charset=UTF-8',
                                                                            'content-length': '231',
                                                                            'date': 'Fri, 06 Jul 2018 11:23:12 GMT',
                                                                            'server': 'AmazonEC2'},
                                                            'RetryAttempts': 0}}

        mockResponseDeleteSnapshots = {'ResponseMetadata': {'RequestId': '05f58e97-e3eb-4dd5-887a-36bf928659b8',
                                                            'HTTPStatusCode': 400,
                                                            'HTTPHeaders': {'content-type': 'text/xml;charset=UTF-8',
                                                                            'content-length': '229',
                                                                            'date': 'Fri, 06 Jul 2018 11:27:45 GMT',
                                                                            'server': 'AmazonEC2'},
                                                            'RetryAttempts': 0}}

        ec2Client.deregister_image = MagicMock(return_value=mockResponseDeregisterImage)
        ec2Client.delete_snapshot = MagicMock(return_value=mockResponseDeleteSnapshots)
        return_value = deleteAMIAction.DeleteOldAMIAction.performAction(self, eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION and return_value.annotation == _("AMI id : {} deregistered successfully but unable to delete AMI snapshots with ids : {}.".format(imageId, notDeletedSnapshotIds))
