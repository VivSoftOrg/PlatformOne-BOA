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
sys.path.append('../../')
from enable_delete_on_termination_ebs.enable_delete_on_termination_ebs_resource_fetcher import *
from tests.enable_delete_on_termination_ebs.test_enable_delete_on_termination_ebs_placebo_initializer import *
import common.compliance_object_factory as complianceobjectfactory
import unittest


EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"configurationItemDiff\":null,\"configurationItem\":{\"relatedEvents\":[\"851cb2ae-c623-4914-add9-0fdfa117423f\"],\"relationships\":[{\"resourceId\":\"eni-520d07d3\",\"resourceName\":null,\"resourceType\":\"AWS::EC2::NetworkInterface\",\"name\":\"Contains NetworkInterface\"},{\"resourceId\":\"sg-bf976acb\",\"resourceName\":null,\"resourceType\":\"AWS::EC2::SecurityGroup\",\"name\":\"Is associated with SecurityGroup\"},{\"resourceId\":\"subnet-ffdba29b\",\"resourceName\":null,\"resourceType\":\"AWS::EC2::Subnet\",\"name\":\"Is contained in Subnet\"},{\"resourceId\":\"vol-0363f54fc5e3d9906\",\"resourceName\":null,\"resourceType\":\"AWS::EC2::Volume\",\"name\":\"Is attached to Volume\"},{\"resourceId\":\"vpc-a04c01d8\",\"resourceName\":null,\"resourceType\":\"AWS::EC2::VPC\",\"name\":\"Is contained in Vpc\"}],\"configuration\":{\"amiLaunchIndex\":0,\"imageId\":\"ami-55ef662f\",\"instanceId\":\"i-05b8ba2c066f455ec\",\"instanceType\":\"t2.micro\",\"kernelId\":null,\"keyName\":null,\"launchTime\":\"2018-01-02T08:47:25.000Z\",\"monitoring\":{\"state\":\"disabled\"},\"placement\":{\"availabilityZone\":\"us-east-1a\",\"affinity\":null,\"groupName\":\"\",\"hostId\":null,\"tenancy\":\"default\",\"spreadDomain\":null},\"platform\":null,\"privateDnsName\":\"ip-172-30-0-125.ec2.internal\",\"privateIpAddress\":\"172.30.0.125\",\"productCodes\":[],\"publicDnsName\":\"\",\"publicIpAddress\":null,\"ramdiskId\":null,\"state\":{\"code\":80,\"name\":\"stopped\"},\"stateTransitionReason\":\"User initiated (2018-01-02 10:43:25 GMT)\",\"subnetId\":\"subnet-ffdba29b\",\"vpcId\":\"vpc-a04c01d8\",\"architecture\":\"x86_64\",\"blockDeviceMappings\":[{\"deviceName\":\"/dev/xvda\",\"ebs\":{\"attachTime\":\"2017-12-28T06:44:33.000Z\",\"deleteOnTermination\":true,\"status\":\"attached\",\"volumeId\":\"vol-0363f54fc5e3d9906\"}}],\"clientToken\":\"\",\"ebsOptimized\":false,\"enaSupport\":true,\"hypervisor\":\"xen\",\"iamInstanceProfile\":null,\"instanceLifecycle\":null,\"elasticGpuAssociations\":[],\"networkInterfaces\":[{\"association\":null,\"attachment\":{\"attachTime\":\"2017-12-28T06:44:32.000Z\",\"attachmentId\":\"eni-attach-47f7c0dc\",\"deleteOnTermination\":true,\"deviceIndex\":0,\"status\":\"attached\"},\"description\":\"Primary network interface\",\"groups\":[{\"groupName\":\"launch-wizard-1\",\"groupId\":\"sg-bf976acb\"}],\"ipv6Addresses\":[],\"macAddress\":\"02:18:5c:be:81:d4\",\"networkInterfaceId\":\"eni-520d07d3\",\"ownerId\":\"107339370656\",\"privateDnsName\":\"ip-172-30-0-125.ec2.internal\",\"privateIpAddress\":\"172.30.0.125\",\"privateIpAddresses\":[{\"association\":null,\"primary\":true,\"privateDnsName\":\"ip-172-30-0-125.ec2.internal\",\"privateIpAddress\":\"172.30.0.125\"}],\"sourceDestCheck\":true,\"status\":\"in-use\",\"subnetId\":\"subnet-ffdba29b\",\"vpcId\":\"vpc-a04c01d8\"}],\"rootDeviceName\":\"/dev/xvda\",\"rootDeviceType\":\"ebs\",\"securityGroups\":[{\"groupName\":\"launch-wizard-1\",\"groupId\":\"sg-bf976acb\"}],\"sourceDestCheck\":true,\"spotInstanceRequestId\":null,\"sriovNetSupport\":null,\"stateReason\":{\"code\":\"Client.UserInitiatedShutdown\",\"message\":\"Client.UserInitiatedShutdown: User initiated shutdown\"},\"tags\":[{\"key\":\"Environment\",\"value\":\"Testing\"},{\"key\":\"ExpirationDate\",\"value\":\"2018-01-08\"},{\"key\":\"Owner\",\"value\":\"devendra.suthar\"},{\"key\":\"Project\",\"value\":\"mnc\"},{\"key\":\"Name\",\"value\":\"test\"}],\"virtualizationType\":\"hvm\"},\"supplementaryConfiguration\":{},\"tags\":{\"Project\":\"mnc\",\"Owner\":\"devendra.suthar\",\"ExpirationDate\":\"2018-01-08\",\"Environment\":\"Testing\",\"Name\":\"test\"},\"configurationItemVersion\":\"1.2\",\"configurationItemCaptureTime\":\"2018-01-02T10:45:57.518Z\",\"configurationStateId\":1514889957518,\"awsAccountId\":\"107339370656\",\"configurationItemStatus\":\"OK\",\"resourceType\":\"AWS::EC2::Instance\",\"resourceId\":\"i-05b8ba2c066f455ec\",\"resourceName\":null,\"ARN\":\"arn:aws:ec2:us-east-1:107339370656:instance/i-05b8ba2c066f455ec\",\"awsRegion\":\"us-east-1\",\"availabilityZone\":\"us-east-1a\",\"configurationStateMd5Hash\":\"baf6a69a8c9fbb6129d758c2acb84c56\",\"resourceCreationTime\":\"2018-01-02T08:47:25.000Z\"},\"notificationCreationTime\":\"2018-01-03T09:58:11.794Z\",\"messageType\":\"ConfigurationItemChangeNotification\",\"recordVersion\":\"1.2\"}",
    "ruleParameters": "{\n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
    "resultToken": "eyJlbmNyeXB0ZWREYXRhIjpbN",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-xbqpcp",
    "configRuleName": "testRule",
    "configRuleId": "config-rule-xbqpcp",
    "accountId": "107339370656"
}

CONTEXT = ""


class TestEnableDeleteOnTerminationEBSFetcher(unittest.TestCase):
    __eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __ec2InstancesFetcher = EnableDeleteOnTerminationEBSResourceFetcher(__eventParam)

    def testESServiceResourceFetcher(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getResourceFetcherMock('fetch_ec2')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__ec2InstancesFetcher.resourceFetcher()
        assert bool(return_value) == True

    def testResourceFetcherNoData(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getResourceFetcherMock('fetch_ec2_response')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        return_value = self.__ec2InstancesFetcher.resourceFetcher()
        assert bool(return_value) == False
