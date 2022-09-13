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

from copy_alb_nlb_tags_to_target_groups.copy_alb_nlb_tags_to_target_groups_action import *
from tests.copy_alb_nlb_tags_to_target_groups.test_copy_alb_nlb_tags_to_target_groups_placebo_initializer import *
import common.compliance_object_factory as complianceObjectFactory
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import AWSResourceClassConstants, ComplianceConstants


import datetime
from dateutil.tz import tzutc


EVENT_JSON = {
    "configRuleId": "config-rule-1v52mx",
    "version": "1.0",
    "configRuleName": "copy_alb_nlb_tags_to_target_groups",
    "configRuleArn": "arn:aws:config:us-east-1:693265998683:config-rule/config-rule-1v52mx",
    "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"configurationItem\": {\n    \"relatedEvents\": [],\n    \"relationships\": [\n      {\n        \"resourceId\": \"eni-3cc64fd2\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::NetworkInterface\",\n        \"name\": \"Contains NetworkInterface\"\n      },\n      {\n        \"resourceId\": \"sg-056a2f78\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"sg-c500e8ba\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"subnet-e41559ad\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Subnet\",\n        \"name\": \"Is contained in Subnet\"\n      },\n      {\n        \"resourceId\": \"vol-03807f5f89a1b3d0b\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Volume\",\n        \"name\": \"Is attached to Volume\"\n      },\n      {\n        \"resourceId\": \"vpc-a02ce1c6\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::VPC\",\n        \"name\": \"Is contained in Vpc\"\n      }\n    ],\n    \"configuration\": {\n      \"instanceId\": \"i-0d735363112477190\",\n      \"imageId\": \"ami-a4c7edb2\",\n      \"state\": {\n        \"code\": 16,\n        \"name\": \"running\"\n      },\n      \"privateDnsName\": \"ip-172-31-28-156.ec2.internal\",\n      \"publicDnsName\": \"ec2-54-235-57-47.compute-1.amazonaws.com\",\n      \"stateTransitionReason\": \"\",\n      \"keyName\": \"REAN_GAURAVASHTIKAR_VIRGINIA_KEYPAIR\",\n      \"amiLaunchIndex\": 0,\n      \"productCodes\": [],\n      \"instanceType\": \"t2.nano\",\n      \"launchTime\": \"2017-07-09T17:34:48.000Z\",\n      \"placement\": {\n        \"availabilityZone\": \"us-east-1b\",\n        \"groupName\": \"\",\n        \"tenancy\": \"default\",\n        \"hostId\": null,\n        \"affinity\": null\n      },\n      \"kernelId\": null,\n      \"ramdiskId\": null,\n      \"platform\": null,\n      \"monitoring\": {\n        \"state\": \"disabled\"\n      },\n      \"subnetId\": \"subnet-29aa575e\",\n      \"vpcId\": \"vpc-c5ec30a0\",\n      \"privateIpAddress\": \"172.31.28.156\",\n      \"publicIpAddress\": \"54.235.57.47\",\n      \"stateReason\": null,\n      \"architecture\": \"x86_64\",\n      \"rootDeviceType\": \"ebs\",\n      \"rootDeviceName\": \"/dev/sda1\",\n      \"blockDeviceMappings\": [\n        {\n          \"deviceName\": \"/dev/sda1\",\n          \"ebs\": {\n            \"volumeId\": \"vol-0bc42d36aa49858fd\",\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:11.000Z\",\n            \"deleteOnTermination\": true\n          }\n        }\n      ],\n      \"virtualizationType\": \"hvm\",\n      \"instanceLifecycle\": null,\n      \"spotInstanceRequestId\": null,\n      \"clientToken\": \"FSRse1484029749587\",\n      \"tags\": [\n        {\n          \"key\": \"Project\",\n          \"value\": \"mnc\"\n        },\n        {\n          \"key\": \"Environment\",\n          \"value\": \"Testing\"\n        },\n        {\n          \"key\": \"Owner\",\n          \"value\": \"gaurav.ashtikar\"\n        },\n        {\n          \"key\": \"Name\",\n          \"value\": \"Gaurav-Test-Machine\"\n        },\n        {\n          \"value\": \"NoShutdown\",\n          \"key\": \"true\"\n        },\n        {\n          \"key\": \"ExpirationDate\",\n          \"value\": \"2017-07-10\"\n        }\n      ],\n      \"securityGroups\": [\n        {\n          \"groupName\": \"gaurav-test-sg\",\n          \"groupId\": \"sg-cc9efcbd\"\n        }\n      ],\n      \"sourceDestCheck\": true,\n      \"hypervisor\": \"xen\",\n      \"networkInterfaces\": [\n        {\n          \"networkInterfaceId\": \"eni-3cc64fd2\",\n          \"subnetId\": \"subnet-e41559ad\",\n          \"vpcId\": \"vpc-a02ce1c6\",\n          \"description\": \"Primary network interface\",\n          \"ownerId\": \"411815166437\",\n          \"status\": \"in-use\",\n          \"macAddress\": \"0a:18:41:09:07:34\",\n          \"privateIpAddress\": \"10.16.3.63\",\n          \"privateDnsName\": \"ip-10-16-3-63.ec2.internal\",\n          \"sourceDestCheck\": true,\n          \"groups\": [\n            {\n              \"groupName\": \"launch-wizard-92\",\n              \"groupId\": \"sg-c500e8ba\"\n            },\n            {\n              \"groupName\": \"jenkins_sg_allow\",\n              \"groupId\": \"sg-056a2f78\"\n            }\n          ],\n          \"attachment\": {\n            \"attachmentId\": \"eni-attach-29cd5d69\",\n            \"deviceIndex\": 0,\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:10.000Z\",\n            \"deleteOnTermination\": true\n          },\n          \"association\": null,\n          \"privateIpAddresses\": [\n            {\n              \"privateIpAddress\": \"10.16.3.63\",\n              \"privateDnsName\": \"ip-10-16-3-63.ec2.internal\",\n              \"primary\": true,\n              \"association\": null\n            }\n          ],\n          \"ipv6Addresses\": []\n        }\n      ],\n      \"iamInstanceProfile\": {\n        \"arn\": \"arn:aws:iam::411815166437:instance-profile/jenkins_master_noel.georgi\",\n        \"id\": \"AIPAJ4KIXV5QRL25MMMCK\"\n      },\n      \"ebsOptimized\": false,\n      \"sriovNetSupport\": null,\n      \"enaSupport\": null\n    },\n    \"supplementaryConfiguration\": {},\n    \"tags\": {\n      \"Project\": \"mnc\",\n      \"Owner\": \"gaurav.ashtikar\",\n      \"ExpirationDate\": \"2017-07-11\",\n      \"Environment\": \"Testing\",\n      \"NoShutdown\": \"true\",\n      \"Name\": \"Gaurav-Test-Machine\"\n    },\n    \"configurationItemVersion\": \"1.2\",\n    \"configurationItemCaptureTime\": \"2017-05-18T18:47:14.686Z\",\n    \"configurationStateId\": 1495133234686,\n    \"awsAccountId\": \"411815166437\",\n    \"configurationItemStatus\": \"OK\",\n    \"resourceType\": \"AWS::EC2::Instance\",\n    \"resourceId\": \"i-0d735363112477190\",\n    \"resourceName\": null,\n    \"ARN\": \"arn:aws:ec2:us-east-1:411815166437:instance/i-0250bff57b217c421\",\n    \"awsRegion\": \"us-east-1\",\n    \"availabilityZone\": \"us-east-1b\",\n    \"configurationStateMd5Hash\": \"ed5fe5d85665e3be3607c27aa50fa0ea\",\n    \"resourceCreationTime\": \"2017-05-13T14:14:48.000Z\"\n  },\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ScheduledNotification\",\n  \"recordVersion\": \"1.2\"\n}",
    "resultToken": "",
        "ruleParameters": "{\"actionName\": \"CopyAlbNlbTagsToTargetGroupsAction\", \"evaluateName\": \"CopyAlbNlbTagsToTargetGroupsEvaluate\", \"resourceFetcherName\" :\"CopyAlbNlbTagsToTargetGroupsResourceFetcher\",\"excludeTags\": \"Environment,Owner\", \n \"notifier\":\"email\",\n \"toEmail\": \"vaibhav.menkudale@reancloud.com\",\n \"ccEmail\": \"vaibhav.menkudale@reancloud.com\",\n  \"performAction\": \"True\"}",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/awsconfig-role",
    "accountId": "693265998683"
    }

CONTEXT = ""
RESOURCE_TYPE = AWSResourceClassConstants.ELB_V2_RESOURCE
RESOURCE_ID = 'arn:aws:elasticloadbalancing:us-east-1:107339370656:loadbalancer/app/vaibhavALBMNCTESTCOPYRULE/c01bcf796c5611d6'
CONFIG_EVENT = {'loadbalancerarn': 'arn:aws:elasticloadbalancing:us-east-1:107339370656:loadbalancer/app/vaibhavALBMNCTESTCOPYRULE/c01bcf796c5611d6', 'dnsname': 'vaibhavALBMNCTESTCOPYRULE-1987971516.us-east-1.elb.amazonaws.com', 'canonicalhostedzoneid': 'Z35SXDOTRQ7X7K', 'createdtime': datetime.datetime(2018, 10, 23, 7, 2, 58, 20000, tzinfo=tzutc()), 'loadbalancername': 'vaibhavALBMNCTESTCOPYRULE', 'scheme': 'internet-facing', 'vpcid': 'vpc-38738c43', 'state': {'code': 'active'}, 'type': 'application', 'availabilityzones': [{'zonename': 'us-east-1a', 'subnetid': 'subnet-7b8dbc1f'}, {'zonename': 'us-east-1b', 'subnetid': 'subnet-eecf8dc1'}], 'securitygroups': ['sg-03ab796da1406111e', 'sg-0ac3bbd40cade08f0'], 'ipaddresstype': 'ipv4', 'region': 'us-east-1', 'missingTagsTargetGroups': [{'ResourceArn': 'arn:aws:elasticloadbalancing:us-east-1:107339370656:targetgroup/vaibhavMNCTargetGroup/8b41b3e1be1d905f', 'Tags': [{'key': 'Name', 'value': 'vaibhavCopyTestNAMETag'}], 'tagsToAdd': [{'key': 'Project', 'value': 'MNC'}, {'key': 'ExpirationDate', 'value': '2018-10-30'}]}]}
CONFIG_EVENT_WO_MISSINGTAGS = {'loadbalancerarn': 'arn:aws:elasticloadbalancing:us-east-1:107339370656:loadbalancer/app/vaibhavALBMNCTESTCOPYRULE/c01bcf796c5611d6', 'dnsname': 'vaibhavALBMNCTESTCOPYRULE-1987971516.us-east-1.elb.amazonaws.com', 'canonicalhostedzoneid': 'Z35SXDOTRQ7X7K', 'createdtime': datetime.datetime(2018, 10, 23, 7, 2, 58, 20000, tzinfo=tzutc()), 'loadbalancername': 'vaibhavALBMNCTESTCOPYRULE', 'scheme': 'internet-facing', 'vpcid': 'vpc-38738c43', 'state': {'code': 'active'}, 'type': 'application', 'availabilityzones': [{'zonename': 'us-east-1a', 'subnetid': 'subnet-7b8dbc1f'}, {'zonename': 'us-east-1b', 'subnetid': 'subnet-eecf8dc1'}], 'securitygroups': ['sg-03ab796da1406111e', 'sg-0ac3bbd40cade08f0'], 'ipaddresstype': 'ipv4', 'region': 'us-east-1'}

class TestCopyAlbNlbTagsToTargetGroupsAction:
    _AbstractAction__eventParam = ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
        )

    __albTagAction = CopyAlbNlbTagsToTargetGroupsAction(_AbstractAction__eventParam)

    def testPerformActionCopyALBNLBTagsToTargetGroupsSucess(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('action_sucess')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_EVENT)
        return_value = self.__albTagAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def testPerformActionCopyALBNLBTagsToTargetGroupsFailure(self):
        recordedMockResponsePath = PlaceboMockResponseInitializer.getActionMock('action_sucess')
        PlaceboMockResponseInitializer.replaying_pill(recordedMockResponsePath)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_EVENT_WO_MISSINGTAGS)
        return_value = self.__albTagAction.performAction(eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION

