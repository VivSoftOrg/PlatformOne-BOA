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
import common.compliance_object_factory as cof
from common.common_constants import *
from mock import MagicMock
from moto import mock_ec2
from botocore.exceptions import ClientError
import exposed_security_groups.exposed_security_groups_action as sgAction


EVENT_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-12-07T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
    "ruleParameters": "{\n  \"toEmail\": \"ankush.tehele@reancloud.com\", \"forbiddenPorts\": \"0-65535\",\n  \"performAction\": \"True\",\n  \"excludedPorts\": \"80, 443\",\n  \"excludedGroupsName\": \"abc\",\n  \"notifier\": \"email\" \n}",
    "resultToken": "eyJlbmNyeXB0ZWREYXRhIjpbNTAsNzgsNTIsMjksMTEyLDEwLDIwLDk2LC03Niw4OCwtODYsLTEyMywtODEsLTc3LDkxLC0xMTIsMzcsLTcwLDEwMSwtNTMsOTEsLTEwLDEyMiwzLDk5LC00MSwyMSw5OSw1NywxMDcsLTEyMSwtNDEsLTMsOTksLTU5LDQxLDIxLC0yMywxNSw1MSwtNjgsNTksLTM3LDEwNSwtOSwtMTQsMTI0LDg0LC00OSwzNiwxMCwzOCwtNzMsMTI0LDQ1LC0xLC0yNiwzMCw0Myw4NCwxMiwtNDIsLTc2LC0zLDMsMTEwLDU2LC01OCwtMzMsLTQwLDIwLC03OCwtODgsNywxMDUsLTM1LC0zOCwtODIsLTUwLDQ1LDM0LDExLDExNCwtODYsLTEsLTExNiwtOTIsLTMsMTUsLTczLDU5LDU3LC03OSwtMTIsLTEwMyw3NSwtNjIsLTMzLC0xMDMsLTIsLTUyLDM2LC0xMDUsLTEwOCwtNDcsNzQsMywtNCw5MCwzLDExNiwtOTMsOTAsMTE1LC03MCw1NSwtNTgsNzgsNDYsNjcsMjksLTg1LC01MSwzNSwtMTI2LDc3LDk2LC0yMiwtMTUsNjUsMTUsMjgsNjIsLTU0LC00NiwtNDgsLTUwLDc3LC0zNywtNjYsLTEyMSwtMzgsLTQsMTE4LC03LDE5LC02MSwtMTIzLDIwLDYyLC04Myw0NSwyOSwtMTAsMTI0LC02NSw3NSwtMTI0LDQ0LC02MywtMjcsMjcsLTMxLDk5LDY3LDAsMTIxLC05NywtMjEsLTcxLDMzLDg1LC0xMTQsLTUxLDEyNyw1NCwtMTAyLDcwLC03NCw4LDc0LC0xMjYsNDIsLTIzLDU2LC05OCwtMTA4LDgxLC0xMjgsMTEyLDE5LC03Myw3NCwtODgsLTY1LDc4LDc2LC0xMjYsLTE2LDExOCwtMTEyLDIsLTUyLDY3LC01Myw3NCwxMTYsLTc3LDcyLDk5LC0xNiwtMTAwLC05OSwtMTksOTEsNDksNSwtNzEsLTgsLTYyLDEyNywtMTEsLTQ0LDEyNywtODksNTEsODIsNjEsLTgxLDk4LDU2LC00Miw5MSw2LDI4LC0xNSwyMSwxOSw0MCwxMDgsMTA5LC04LDEyNCwzOSwtNjUsLTU3LDkwLC0xMDEsMTA2LC0yMSwxMTEsLTExOSw2NSw2LC01NSw5MSwtMzUsMTYsLTExOCwtMTA1LDgzLDQ0LDgwXSwibWF0ZXJpYWxTZXRTZXJpYWxOdW1iZXIiOjEsIml2UGFyYW1ldGVyU3BlYyI6eyJpdiI6WzkxLDc1LC03MywtMzEsNCw4LC0yMyw3OSwtODUsLTg1LDIsMTI3LDEyMywtNDksNCw4NV19fQ==eyJlbmNyeXB0ZWREYXRhIjpbNTAsNzgsNTIsMjksMTEyLDEwLDIwLDk2LC03Niw4OCwtODYsLTEyMywtODEsLTc3LDkxLC0xMTIsMzcsLTcwLDEwMSwtNTMsOTEsLTEwLDEyMiwzLDk5LC00MSwyMSw5OSw1NywxMDcsLTEyMSwtNDEsLTMsOTksLTU5LDQxLDIxLC0yMywxNSw1MSwtNjgsNTksLTM3LDEwNSwtOSwtMTQsMTI0LDg0LC00OSwzNiwxMCwzOCwtNzMsMTI0LDQ1LC0xLC0yNiwzMCw0Myw4NCwxMiwtNDIsLTc2LC0zLDMsMTEwLDU2LC01OCwtMzMsLTQwLDIwLC03OCwtODgsNywxMDUsLTM1LC0zOCwtODIsLTUwLDQ1LDM0LDExLDExNCwtODYsLTEsLTExNiwtOTIsLTMsMTUsLTczLDU5LDU3LC03OSwtMTIsLTEwMyw3NSwtNjIsLTMzLC0xMDMsLTIsLTUyLDM2LC0xMDUsLTEwOCwtNDcsNzQsMywtNCw5MCwzLDExNiwtOTMsOTAsMTE1LC03MCw1NSwtNTgsNzgsNDYsNjcsMjksLTg1LC01MSwzNSwtMTI2LDc3LDk2LC0yMiwtMTUsNjUsMTUsMjgsNjIsLTU0LC00NiwtNDgsLTUwLDc3LC0zNywtNjYsLTEyMSwtMzgsLTQsMTE4LC03LDE5LC02MSwtMTIzLDIwLDYyLC04Myw0NSwyOSwtMTAsMTI0LC02NSw3NSwtMTI0LDQ0LC02MywtMjcsMjcsLTMxLDk5LDY3LDAsMTIxLC05NywtMjEsLTcxLDMzLDg1LC0xMTQsLTUxLDEyNyw1NCwtMTAyLDcwLC03NCw4LDc0LC0xMjYsNDIsLTIzLDU2LC05OCwtMTA4LDgxLC0xMjgsMTEyLDE5LC03Myw3NCwtODgsLTY1LDc4LDc2LC0xMjYsLTE2LDExOCwtMTEyLDIsLTUyLDY3LC01Myw3NCwxMTYsLTc3LDcyLDk5LC0xNiwtMTAwLC05OSwtMTksOTEsNDksNSwtNzEsLTgsLTYyLDEyNywtMTEsLTQ0LDEyNywtODksNTEsODIsNjEsLTgxLDk4LDU2LC00Miw5MSw2LDI4LC0xNSwyMSwxOSw0MCwxMDgsMTA5LC04LDEyNCwzOSwtNjUsLTU3LDkwLC0xMDEsMTA2LC0yMSwxMTEsLTExOSw2NSw2LC01NSw5MSwtMzUsMTYsLTExOCwtMTA1LDgzLDQ0LDgwXSwibWF0ZXJpYWxTZXRTZXJpYWxOdW1iZXIiOjEsIml2UGFyYW1ldGVyU3BlYyI6eyJpdiI6WzkxLDc1LC03MywtMzEsNCw4LC0yMyw3OSwtODUsLTg1LDIsMTI3LDEyMywtNDksNCw4NV19fQ==eyJlbmNyeXB0ZWREYXRhIjpbNTAsNzgsNTIsMjksMTEyLDEwLDIwLDk2LC03Niw4OCwtODYsLTEyMywtODEsLTc3LDkxLC0xMTIsMzcsLTcwLDEwMSwtNTMsOTEsLTEwLDEyMiwzLDk5LC00MSwyMSw5OSw1NywxMDcsLTEyMSwtNDEsLTMsOTksLTU5LDQxLDIxLC0yMywxNSw1MSwtNjgsNTksLTM3LDEwNSwtOSwtMTQsMTI0LDg0LC00OSwzNiwxMCwzOCwtNzMsMTI0LDQ1LC0xLC0yNiwzMCw0Myw4NCwxMiwtNDIsLTc2LC0zLDMsMTEwLDU2LC01OCwtMzMsLTQwLDIwLC03OCwtODgsNywxMDUsLTM1LC0zOCwtODIsLTUwLDQ1LDM0LDExLDExNCwtODYsLTEsLTExNiwtOTIsLTMsMTUsLTczLDU5LDU3LC03OSwtMTIsLTEwMyw3NSwtNjIsLTMzLC0xMDMsLTIsLTUyLDM2LC0xMDUsLTEwOCwtNDcsNzQsMywtNCw5MCwzLDExNiwtOTMsOTAsMTE1LC03MCw1NSwtNTgsNzgsNDYsNjcsMjksLTg1LC01MSwzNSwtMTI2LDc3LDk2LC0yMiwtMTUsNjUsMTUsMjgsNjIsLTU0LC00NiwtNDgsLTUwLDc3LC0zNywtNjYsLTEyMSwtMzgsLTQsMTE4LC03LDE5LC02MSwtMTIzLDIwLDYyLC04Myw0NSwyOSwtMTAsMTI0LC02NSw3NSwtMTI0LDQ0LC02MywtMjcsMjcsLTMxLDk5LDY3LDAsMTIxLC05NywtMjEsLTcxLDMzLDg1LC0xMTQsLTUxLDEyNyw1NCwtMTAyLDcwLC03NCw4LDc0LC0xMjYsNDIsLTIzLDU2LC05OCwtMTA4LDgxLC0xMjgsMTEyLDE5LC03Myw3NCwtODgsLTY1LDc4LDc2LC0xMjYsLTE2LDExOCwtMTEyLDIsLTUyLDY3LC01Myw3NCwxMTYsLTc3LDcyLDk5LC0xNiwtMTAwLC05OSwtMTksOTEsNDksNSwtNzEsLTgsLTYyLDEyNywtMTEsLTQ0LDEyNywtODksNTEsODIsNjEsLTgxLDk4LDU2LC00Miw5MSw2LDI4LC0xNSwyMSwxOSw0MCwxMDgsMTA5LC04LDEyNCwzOSwtNjUsLTU3LDkwLC0xMDEsMTA2LC0yMSwxMTEsLTExOSw2NSw2LC01NSw5MSwtMzUsMTYsLTExOCwtMTA1LDgzLDQ0LDgwXSwibWF0ZXJpYWxTZXRTZXJpYWxOdW1iZXIiOjEsIml2UGFyYW1ldGVyU3BlYyI6eyJpdiI6WzkxLDc1LC03MywtMzEsNCw4LC0yMyw3OSwtODUsLTg1LDIsMTI3LDEyMywtNDksNCw4NV19fQ==",
    "eventLeftScope": "False",
    "executionRoleArn": "arn:aws:iam::107339370656:role/svc-rean-mnc-default-config-role",
    "configRuleArn": "arn:aws:config:us-east-1:107339370656:config-rule/config-rule-zgvfqq",
    "configRuleName": "gaurav-test",
    "configRuleId": "config-rule-zgvfqq",
    "accountId": "107339370656"
}

CONTEXT = ""

RESOURCE_ID = ""
RESOURCE_TYPE = AWSResourceClassConstants.SG_RESOURCE
CONFIGITEMS = {"region": "us-east-1"}


class TestDeleteUnusedSGAction(object):

    __regions = ['us-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'sa-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    __mockInstanceResponse = {'ResponseMetadata': {'HTTPStatusCode': 200, 'RetryAttempts': 0}}
    __mockInstanceResponse_fail = {'ResponseMetadata': {'HTTPStatusCode': 500, 'RetryAttempts': 0}}
    __errorResponse = {'Error': {
        'Code': 400,
        'Message': 'AccessDenied'
    }}

    CONFIGITEMSEV = {
        "resourceId": "sg-d48ee69f",
        "description": "test",
        "groupname": "test",
        "ippermissions": [
            {
                "fromport": 56,
                "ipprotocol": "tcp",
                "ipranges": [
                    {
                        "cidrip": "0.0.0.0/0"
                    }
                ],
                "ipv6ranges": [],
                "prefixlistids": [],
                "toport": 56,
                "useridgrouppairs": []
            }
        ],
        "ownerid": "693265998683",
        "groupid": "sg-d48ee69f",
    }

    CONFIGITEMSNC = {
            "resourceId": "sg-d48ee69f",
            "description": "test",
            "groupname": "test",
            "ippermissions": [
                {
                    "fromport": 56,
                    "ipprotocol": "tcp",
                    "ipranges": [
                        {
                          "cidrip": "1.0.0.0/0"
                        }
                    ],
                    "ipv6ranges": [],
                    "prefixlistids": [],
                    "toport": 56,
                    "useridgrouppairs": []
                }
            ],
            "ownerid": "693265998683",
            "groupid": "sg-d48ee69f",
        }

    CONFIGITEMSNE = {
        "resourceId": "sg-d48ee69f",
        "description": "test",
        "groupname": "test"
    }

    __eventParam = cof.ComplianceObjectFactory.createEventParamFrom(
        EVENT_JSON,
        CONTEXT
    )
    __exposedSecurityGroupsAction = sgAction.ExposedSecurityGroupsAction(__eventParam)

    @mock_ec2
    def test_SGRevokeSuccess(self):
        CONFIGITEMS['region'] = 'us-east-1'
        RESOURCE_ID = 'sg-d48ee69f'

        eventItem = cof.ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.CONFIGITEMSNC)
        self.__revokePublicRule = MagicMock(return_value=True)
        evaluationResult = self.__exposedSecurityGroupsAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE

    @mock_ec2
    def test_SGRevokeFail(self):
        CONFIGITEMS['region'] = 'us-east-1'
        RESOURCE_ID = 'sg-d48ee69f'

        eventItem = cof.ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=RESOURCE_ID, resourceType=RESOURCE_TYPE, configItems=self.CONFIGITEMSNE)
        self.__revokePublicRule = MagicMock(return_value=False)
        evaluationResult = self.__exposedSecurityGroupsAction.performAction(eventItem)
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE
