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
import datetime
from mock import MagicMock
from moto import mock_rds

sys.path.append('../../')

from common.abstract_evaluate import *
from common.boto_utility import *
import rds_expiry_tag.rds_expiry_tag_action as exptag
import common.compliance_object_factory as cof
from common.common_constants import AWSResourceClassConstants, ComplianceConstants
from common.compliance_object_factory import ComplianceObjectFactory


# EVENTJSON with valid ExpirationDate tag
expiration_date = (datetime.datetime.now()).strftime("%Y-%m-%d")
EVENTJSON = {
    "configRuleId": "config-rule-1v52mx",
    "version": "1.0",
    "configRuleName": "aws-sample-rule",
    "configRuleArn": "arn:aws:config:us-east-1:411815166437:config-rule/config-rule-1v52mx",
    "invokingEvent": "{\n  \"configurationItemDiff\": null,\n  \"configurationItem\": {\n    \"relatedEvents\": [],\n    \"relationships\": [\n      {\n        \"resourceId\": \"eni-3cc64fd2\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::NetworkInterface\",\n        \"name\": \"Contains NetworkInterface\"\n      },\n      {\n        \"resourceId\": \"sg-056a2f78\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"sg-c500e8ba\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::SecurityGroup\",\n        \"name\": \"Is associated with SecurityGroup\"\n      },\n      {\n        \"resourceId\": \"subnet-e41559ad\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Subnet\",\n        \"name\": \"Is contained in Subnet\"\n      },\n      {\n        \"resourceId\": \"vol-03807f5f89a1b3d0b\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::Volume\",\n        \"name\": \"Is attached to Volume\"\n      },\n      {\n        \"resourceId\": \"vpc-a02ce1c6\",\n        \"resourceName\": null,\n        \"resourceType\": \"AWS::EC2::VPC\",\n        \"name\": \"Is contained in Vpc\"\n      }\n    ],\n    \"configuration\": {\n      \"instanceId\": \"i-0d735363112477190\",\n      \"imageId\": \"ami-a4c7edb2\",\n      \"state\": {\n        \"code\": 16,\n        \"name\": \"running\"\n      },\n      \"privateDnsName\": \"ip-172-31-28-156.ec2.internal\",\n      \"publicDnsName\": \"ec2-54-235-57-47.compute-1.amazonaws.com\",\n      \"stateTransitionReason\": \"\",\n      \"keyName\": \"REAN_GAURAVASHTIKAR_VIRGINIA_KEYPAIR\",\n      \"amiLaunchIndex\": 0,\n      \"productCodes\": [],\n      \"instanceType\": \"t2.nano\",\n      \"launchTime\": \"2017-07-09T17:34:48.000Z\",\n      \"placement\": {\n        \"availabilityZone\": \"us-east-1b\",\n        \"groupName\": \"\",\n        \"tenancy\": \"default\",\n        \"hostId\": null,\n        \"affinity\": null\n      },\n      \"kernelId\": null,\n      \"ramdiskId\": null,\n      \"platform\": null,\n      \"monitoring\": {\n        \"state\": \"disabled\"\n      },\n      \"subnetId\": \"subnet-29aa575e\",\n      \"vpcId\": \"vpc-c5ec30a0\",\n      \"privateIpAddress\": \"172.31.28.156\",\n      \"publicIpAddress\": \"54.235.57.47\",\n      \"stateReason\": null,\n      \"architecture\": \"x86_64\",\n      \"rootDeviceType\": \"ebs\",\n      \"rootDeviceName\": \"/dev/sda1\",\n      \"blockDeviceMappings\": [\n        {\n          \"deviceName\": \"/dev/sda1\",\n          \"ebs\": {\n            \"volumeId\": \"vol-0bc42d36aa49858fd\",\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:11.000Z\",\n            \"deleteOnTermination\": true\n          }\n        }\n      ],\n      \"virtualizationType\": \"hvm\",\n      \"instanceLifecycle\": null,\n      \"spotInstanceRequestId\": null,\n      \"clientToken\": \"FSRse1484029749587\",\n      \"tags\": [\n        {\n          \"key\": \"Project\",\n          \"value\": \"mnc\"\n        },\n        {\n          \"key\": \"Environment\",\n          \"value\": \"Testing\"\n        },\n        {\n          \"key\": \"Owner\",\n          \"value\": \"Priyanka\"\n        },\n        {\n          \"key\": \"Name\",\n          \"value\": \"Priyanka-Test-Machine\"\n        },\n        {\n          \"value\": \"NoShutdown\",\n          \"key\": \"true\"\n        },\n        {\n          \"key\": \"ExpirationDate\",\n          \"value\": \"" + expiration_date + "\"\n        }\n      ],\n      \"securityGroups\": [\n        {\n          \"groupName\": \"launch-wizard-4\",\n          \"groupId\": \"sg-a845a3d8\"\n        }\n      ],\n      \"sourceDestCheck\": true,\n      \"hypervisor\": \"xen\",\n      \"networkInterfaces\": [\n        {\n          \"networkInterfaceId\": \"eni-3cc64fd2\",\n          \"subnetId\": \"subnet-e41559ad\",\n          \"vpcId\": \"vpc-47105e22\",\n          \"description\": \"Primary network interface\",\n          \"ownerId\": \"107339370656\",\n          \"status\": \"in-use\",\n          \"macAddress\": \"0a:18:41:09:07:34\",\n          \"privateIpAddress\": \"172.31.42.129\",\n          \"privateDnsName\": \"ip-172-31-42-129.ec2.internal\",\n          \"sourceDestCheck\": true,\n          \"groups\": [\n            {\n              \"groupName\": \"launch-wizard-92\",\n              \"groupId\": \"sg-c500e8ba\"\n            },\n            {\n              \"groupName\": \"jenkins_sg_allow\",\n              \"groupId\": \"sg-056a2f78\"\n            }\n          ],\n          \"attachment\": {\n            \"attachmentId\": \"eni-attach-29cd5d69\",\n            \"deviceIndex\": 0,\n            \"status\": \"attached\",\n            \"attachTime\": \"2017-01-10T06:29:10.000Z\",\n            \"deleteOnTermination\": true\n          },\n          \"association\": null,\n          \"privateIpAddresses\": [\n            {\n              \"privateIpAddress\": \"10.16.3.63\",\n              \"privateDnsName\": \"ip-10-16-3-63.ec2.internal\",\n              \"primary\": true,\n              \"association\": null\n            }\n          ],\n          \"ipv6Addresses\": []\n        }\n      ],\n      \"iamInstanceProfile\": {\n        \"arn\": \"arn:aws:iam::411815166437:instance-profile/jenkins_master_noel.georgi\",\n        \"id\": \"AIPAJ4KIXV5QRL25MMMCK\"\n      },\n      \"ebsOptimized\": false,\n      \"sriovNetSupport\": null,\n      \"enaSupport\": null\n    },\n    \"supplementaryConfiguration\": {},\n    \"tags\": {\n      \"Project\": \"mnc\",\n      \"Owner\": \"Priyanka\",\n      \"ExpirationDate\": \"" + expiration_date + "\",\n      \"Environment\": \"Testing\",\n      \"NoShutdown\": \"true\",\n      \"Name\": \"Priyanka-Test-Machine\"\n    },\n    \"configurationItemVersion\": \"1.2\",\n    \"configurationItemCaptureTime\": \"2017-05-18T18:47:14.686Z\",\n    \"configurationStateId\": 1495133234686,\n    \"awsAccountId\": \"411815166437\",\n    \"configurationItemStatus\": \"OK\",\n    \"resourceType\": \"AWS::EC2::Instance\",\n    \"resourceId\": \"i-0135c2c070d1bcfab\",\n    \"resourceName\": null,\n    \"ARN\": \"arn:aws:ec2:us-east-1:411815166437:instance/i-0250bff57b217c421\",\n    \"awsRegion\": \"us-east-1\",\n    \"availabilityZone\": \"us-east-1b\",\n    \"configurationStateMd5Hash\": \"ed5fe5d85665e3be3607c27aa50fa0ea\",\n    \"resourceCreationTime\": \"2017-05-13T14:14:48.000Z\"\n  },\n  \"notificationCreationTime\": \"2017-05-19T08:40:15.976Z\",\n  \"messageType\": \"ConfigurationItemChangeNotification\",\n  \"recordVersion\": \"1.2\"\n}",
    "resultToken": "",
    "eventLeftScope": "False",
    "ruleParameters": "{\"limit_expiration_date\":7,\"performAction\": \"True\",\"notifier\": \"sns\"}",
    "executionRoleArn": "arn:aws:iam::411815166437:role/awsconfig-role",
    "accountId": "411815166437"
}

CONTEXT = ""

eventParam = cof.ComplianceObjectFactory.createEventParamFrom(
    EVENTJSON,
    CONTEXT
)

RESOURCE_ID = "i-0cd2c09e799d7fb02"
RESOURCE_TYPE = "AWS::RDS::DBInstance"
CONFIG_ITEMS = {
    "resourceId": "i-01254789351",
    "dbinstanceidentifier": "test",
    "dbinstancearn": "arn:test::rds:ds",
    "Resource Name": "RDS Expiry Tag",
    "tags": [
        {
            "key": "Name",
            "value": "Priyanka-Test-Machine"
        },
        {
            "key": "ExpirationDate",
            "value": ""
        }
    ],
    "NON_COMPLAINT_RESOURCE_ACTION": "For Reference when the resource validity corssed."
}

CONFIG_ITEMS_ABOUT_TO_EXPIRE = {
    "resourceId": "i-01254789351",
    "dbinstanceidentifier": "test",
    "Resource Name": "RDS Expiry Tag",
    "dbinstancearn": "arn:test::rds:ds",
    "tags": [
        {
            "key": "Name",
            "value": "Priyanka-Test-Machine"
        },
        {
            "key": "ExpirationDate",
            "value": "2018-06-12"
        }
    ],
    "NON_COMPLAINT_RESOURCE_ACTION": "For Reference when expiration date is near"
}

CONFIG_ITEMS_INVALID_DATE = {
    "resourceId": "i-01254789351",
    "dbinstanceidentifier": "test",
    "dbinstancearn": "arn:test::rds:ds",
    "Resource Name": "RDS Expiry Tag",
    "tags": [
        {
            "key": "Name",
            "value": "Priyanka-Test-Machine"
        },
        {
            "key": "ExpirationDate",
            "value": "2018-06"
        }
    ],
    "NON_COMPLAINT_RESOURCE_ACTION": "For Reference when the Expiration tag is not valid "
}

CONFIG_ITEMS_TERMINATE_INST = {
    "resourceId": "i-01254789351",
    "dbinstanceidentifier": "test",
    "dbinstancearn": "arn:test::rds:ds",
    "Resource Name": "RDS Expiry Tag",
    "tags": [
        {
            "key": "Name",
            "value": "Priyanka-Test-Machine"
        },
        {
            "key": "ExpirationDate",
            "value": "2018-06-07"
        }
    ],
    "NON_COMPLAINT_RESOURCE_ACTION": "For Reference when the resource validity corssed."
}

CONFIG_ITEMS_EXCEPTION = {
    "configItems": {
        "resourceId": "i-01254789351",
        "dbinstanceidentifier": "test",
        "dbinstancearn": "arn:test::rds:ds",
        "Resource Name": "RDS Expiry Tag",
        "tags": [
            {
                "key": "Name",
                "value": "Priyanka-Test-Machine"
            },
            {
                "key": "ExpirationDate",
                "value": "2018-06-07"
            }
        ],
    }
}


class TestRdsExpiryTagAction(object):
    """ This method is used to test RDS Expiry Tag Action """

    __mockHttpResponseSuccess = {'ResponseMetadata': {'HTTPStatusCode': 200, 'RetryAttempts': 0}}
    __mockHttpResponseFail = {'ResponseMetadata': {'HTTPStatusCode': 500, 'RetryAttempts': 0}}
    __awsRegion = "us-east-1"
    __eventParam = cof.ComplianceObjectFactory.createEventParamFrom(
        EVENTJSON,
        CONTEXT
    )

    @mock_rds
    def test_perform_action_date_invalid_date_failed(self):
        """ This method checks for invalid date for failed case """
        self._AbstractAction__eventParam = self.__eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS_INVALID_DATE)
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__awsRegion)
        exptag.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        rdsClient.add_tags_to_resource = MagicMock(return_value=self.__mockHttpResponseFail)
        return_value = exptag.RdsExpiryTagAction.performAction(self, eventItem)

        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_rds
    def test_perform_action_date_invalid_date(self):
        """ This method checks for invalid date for success case """
        self._AbstractAction__eventParam = self.__eventParam
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__awsRegion)
        exptag.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        rdsClient.add_tags_to_resource = MagicMock(return_value=self.__mockHttpResponseSuccess)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS_INVALID_DATE)
        return_value = exptag.RdsExpiryTagAction.performAction(self, eventItem)

        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_rds
    def test_perform_action_date_about_to_expire(self):
        """ This method checks when the resource are about to expire """
        self._AbstractAction__eventParam = eventParam
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS_ABOUT_TO_EXPIRE)
        return_value = exptag.RdsExpiryTagAction.performAction(self, eventItem)

        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_rds
    def test_perform_action_expdate_crossed_failed(self):
        """ This method checks if the expiration date is crossed but response failed """
        self._AbstractAction__eventParam = eventParam
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__awsRegion)
        exptag.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        rdsClient.delete_db_instance = MagicMock(return_value=self.__mockHttpResponseFail)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        return_value = exptag.RdsExpiryTagAction.performAction(self, eventItem)

        assert return_value.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    @mock_rds
    def test_perform_action_expdate_crossed(self):
        """ This method checks for invalid date for success case """
        self._AbstractAction__eventParam = eventParam
        rdsClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_RDS, region_name=self.__awsRegion)
        exptag.BotoUtility.getClient = MagicMock(return_value=rdsClient)
        rdsClient.delete_db_instance = MagicMock(return_value=self.__mockHttpResponseSuccess)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS)
        return_value = exptag.RdsExpiryTagAction.performAction(self, eventItem)

        assert return_value.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    def test_perform_action_with_exception(self):
        """ This method checks for expiration date with exception"""
        self._AbstractAction__eventParam = eventParam
        rds = 'rds'
        exptag.BotoUtility.getClient = MagicMock(return_value=rds)
        eventItem = ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=CONFIG_ITEMS_EXCEPTION)
        return_value = exptag.RdsExpiryTagAction.performAction(self, eventItem)
        assert return_value.complianceType == ComplianceConstants.MNC_ACTION_EXCEPTION
