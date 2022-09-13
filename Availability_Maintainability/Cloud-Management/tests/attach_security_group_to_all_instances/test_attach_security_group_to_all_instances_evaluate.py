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
from attach_security_group_to_all_instances.attach_security_group_to_all_instances_evaluate import *
import common.compliance_object_factory as complianceobjectfactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import *
from common.abstract_evaluate import *
from common.common_utility import *
from common.boto_utility import *
from datetime import datetime, timedelta

EVENT_JSON = {
      "configRuleId": "config-rule-1v52mx",
      "version": "1.0",
      "configRuleName": "aws-sample-rule",
      "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-1v52mx",
      "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
      "resultToken": "",
      "ruleParameters": "{\"mappings\": \"us-east-1 = vpc-a25216da + sg-14a16e63 | sg-f2a96685 : vpc-a25216da + sg-14a16e63 | sg-f2a96685 , us-west-2 = vpc-b34aa6ca + sg-a3867fdc | sg-77877e08\" , \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\",\n  \"performAction\": \"True\"}",
      "eventLeftScope": "False",
      "executionRoleArn": "arn:aws:iam::107339370656:role/awsconfig-role",
      "accountId": "107339370656"
}

SECURITY_GROUP_ATTACHED = {"region": "us-east-1", "RootDeviceType": "ebs","Placement": {"Tenancy": "default","AvailabilityZone": "us-east-1b","GroupName": ""},"AmiLaunchIndex": 0,"KeyName": "mnc-client","State": {"Name": "stopped","Code": 80},"Architecture": "x86_64","StateReason": {"Message": "Client.UserInitiatedShutdown: User initiated shutdown","Code": "Client.UserInitiatedShutdown"},"Tags": [{"Key": "Environment","Value": "Testing"},{"Key": "Owner","Value": "devendra.suthar"},{"Key": "Project","Value": "mnc"},{"Key": "Name","Value": "mncRuleTesting"},{"Key": "ExpirationDate","Value": "2018-02-04"}],"ProductCodes": [],"StateTransitionReason": "User initiated (2018-01-27 00:27:06 GMT)","SourceDestCheck": True,"ImageId": "ami-97785bed","InstanceId": "i-089678f1b711be73e","LaunchTime": {"minute": 33,"microsecond": 0,"year": 2018,"day": 25,"month": 1,"__class__": "datetime","second": 39,"hour": 8},"VpcId": "vpc-a25216da","BlockDeviceMappings": [{"Ebs": {"DeleteOnTermination": True,"Status": "attached","AttachTime": {"minute": 33,"microsecond": 0,"year": 2018,"day": 25,"month": 1,"__class__": "datetime","second": 40,"hour": 8},"VolumeId": "vol-0aa1a51ee5ae5400a"},"DeviceName": "/dev/xvda"}],"ClientToken": "","InstanceType": "t2.nano","PrivateIpAddress": "172.31.19.38","Hypervisor": "xen","VirtualizationType": "hvm","NetworkInterfaces": [{"PrivateIpAddresses": [{"PrivateDnsName": "ip-172-31-19-38.ec2.internal","Primary": True,"PrivateIpAddress": "172.31.19.38"}],"Ipv6Addresses": [],"PrivateIpAddress": "172.31.19.38","NetworkInterfaceId": "eni-326f6fc9","Attachment": {"DeleteOnTermination": True,"DeviceIndex": 0,"AttachTime": {"minute": 33,"microsecond": 0,"year": 2018,"day": 25,"month": 1,"__class__": "datetime","second": 39,"hour": 8},"AttachmentId": "eni-attach-b0555987","Status": "attached"},"MacAddress": "0a:34:45:d2:8a:f8","Description": "","VpcId": "vpc-a25216da","Groups": [{"GroupId": "sg-f8d4f18d","GroupName": "default"}],"SourceDestCheck": True,"PrivateDnsName": "ip-172-31-19-38.ec2.internal","Status": "in-use","OwnerId": "693265998683","SubnetId": "subnet-36c7b77d"}],"EnaSupport": True,"Monitoring": {"State": "disabled"},"PrivateDnsName": "ip-172-31-19-38.ec2.internal","PublicDnsName": "","EbsOptimized": False,"SubnetId": "subnet-36c7b77d","RootDeviceName": "/dev/xvda","SecurityGroups": [{"GroupId": "sg-f8d4f18d","GroupName": "default"},{"GroupId": "sg-14a16e63","GroupName": "SGTesting1"},{"GroupId": "sg-f2a96685","GroupName": "SGTesting2"}]}

SECURITY_GROUP_NOT_ATTACHED = {"allsecuritygroupsofvpc": "", "region": "us-east-1", "RootDeviceType": "ebs","Placement": {"Tenancy": "default","AvailabilityZone": "us-east-1b","GroupName": ""},"AmiLaunchIndex": 0,"KeyName": "mnc-client","State": {"Name": "stopped","Code": 80},"Architecture": "x86_64","StateReason": {"Message": "Client.UserInitiatedShutdown: User initiated shutdown","Code": "Client.UserInitiatedShutdown"},"Tags": [{"Key": "Environment","Value": "Testing"},{"Key": "Owner","Value": "devendra.suthar"},{"Key": "Project","Value": "mnc"},{"Key": "Name","Value": "mncRuleTesting"},{"Key": "ExpirationDate","Value": "2018-02-04"}],"ProductCodes": [],"StateTransitionReason": "User initiated (2018-01-27 00:27:06 GMT)","SourceDestCheck": True,"ImageId": "ami-97785bed","InstanceId": "i-089678f1b711be73e","LaunchTime": {"minute": 33,"microsecond": 0,"year": 2018,"day": 25,"month": 1,"__class__": "datetime","second": 39,"hour": 8},"VpcId": "vpc-a25216da","BlockDeviceMappings": [{"Ebs": {"DeleteOnTermination": True,"Status": "attached","AttachTime": {"minute": 33,"microsecond": 0,"year": 2018,"day": 25,"month": 1,"__class__": "datetime","second": 40,"hour": 8},"VolumeId": "vol-0aa1a51ee5ae5400a"},"DeviceName": "/dev/xvda"}],"ClientToken": "","InstanceType": "t2.nano","PrivateIpAddress": "172.31.19.38","Hypervisor": "xen","VirtualizationType": "hvm","NetworkInterfaces": [{"PrivateIpAddresses": [{"PrivateDnsName": "ip-172-31-19-38.ec2.internal","Primary": True,"PrivateIpAddress": "172.31.19.38"}],"Ipv6Addresses": [],"PrivateIpAddress": "172.31.19.38","NetworkInterfaceId": "eni-326f6fc9","Attachment": {"DeleteOnTermination": True,"DeviceIndex": 0,"AttachTime": {"minute": 33,"microsecond": 0,"year": 2018,"day": 25,"month": 1,"__class__": "datetime","second": 39,"hour": 8},"AttachmentId": "eni-attach-b0555987","Status": "attached"},"MacAddress": "0a:34:45:d2:8a:f8","Description": "","VpcId": "vpc-a25216da","Groups": [{"GroupId": "sg-f8d4f18d","GroupName": "default"}],"SourceDestCheck": True,"PrivateDnsName": "ip-172-31-19-38.ec2.internal","Status": "in-use","OwnerId": "693265998683","SubnetId": "subnet-36c7b77d"}],"EnaSupport": True,"Monitoring": {"State": "disabled"},"PrivateDnsName": "ip-172-31-19-38.ec2.internal","PublicDnsName": "","EbsOptimized": False,"SubnetId": "subnet-36c7b77d","RootDeviceName": "/dev/xvda","SecurityGroups": [{"GroupId": "sg-f8d4f18d","GroupName": "default"}]}

CONTEXT = ""
RESOURCE_TYPE = AWSResourceClassConstants.EC2_INSTANCE
RESOURCE_ID = 'id-as87asd'

class TestAttachSecurityGroupToInstancesEvaluate(object):

    _AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )

    __securityGroupEvaluator = AttachSecurityGroupToInstancesEvaluate(_AbstractEvaluator__eventParam)

    def testEvaluateForSecurityGroupAttached(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CommonUtility.changeDictionaryKeysToLowerCase(SECURITY_GROUP_ATTACHED))
        evaluationResult = self.__securityGroupEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testEvaluateForSecurityGroupNotAttached(self):
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CommonUtility.changeDictionaryKeysToLowerCase(SECURITY_GROUP_NOT_ATTACHED))
        evaluationResult = self.__securityGroupEvaluator.evaluate(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

