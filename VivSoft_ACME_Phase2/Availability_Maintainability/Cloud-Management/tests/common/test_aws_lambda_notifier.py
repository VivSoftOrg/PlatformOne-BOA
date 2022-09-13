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
import os
import boto3
from common.framework_objects import *
from moto import *
from datetime import datetime, timedelta, timezone
from dateutil.tz import tzutc
sys.path.append('../../')
import common.aws_lambda_notifier as lambdaNotify
import common.compliance_object_factory as cof
from common.compliance_object_factory import *
from mock import MagicMock

EVENTJSON = {
  "version": "1.0",
  "invokingEvent": "{\"awsAccountId\":\"107339370656\",\"notificationCreationTime\":\"2017-12-07T22:33:33.717Z\",\"messageType\":\"ScheduledNotification\",\"recordVersion\":\"1.0\"}",
  "ruleParameters": "{\n  \"toEmail\": \"vaibhav.fulsundar@reancloud.com\", \"resourceFetcherName\": \"CheckELBRequiredTagValuesResourceFetcher\", \"evaluateName\": \"CheckELBRequiredTagValuesEvaluate\", \"actionName\": \"CheckELBRequiredTagValuesAction\", \"validity\": \"3\",\"RequiredTags\": \"Owner,Environment,Project,ExpirationDate\",\n  \"performAction\": \"True\",\n  \"notifier\": \"ses\", \"expirationDateLimit\":\"8\" \n}",
  "resultToken": "",
  "eventLeftScope": "False",
  "executionRoleArn": "arn:aws:iam::693265998683:role/svc-rean-mnc-default-config-role",
  "configRuleArn": "arn:aws:config:us-east-1:693265998683:config-rule/config-rule-lcujqi",
  "configRuleName": "check_elb_required_tag_values",
  "configRuleId": "config-rule-kvvdy9",
  "accountId": "107339370656"
}


CONTEXT = ""
eventParam = cof.ComplianceObjectFactory.createEventParamFrom(
    EVENTJSON,
    CONTEXT
)
RESOURCE_ID = 'testELB'
RESOURCE_TYPE = AWSResourceClassConstants.ELB_RESOURCE
CONFIG_ITEMS = {'region':'us-east-1','loadbalancerarn':'arn:aws:elasticloadbalancing:us-east-1:693265998683:loadbalancer/app/testApp/0dd0188b39ece326'}
LAMBDA_MESSAGE = {'notifier': 'ses', 'aliasName': 'mnc-master', 'moduleName': 'CheckElbRequiredTagValues', 'messageType': 'ScheduledNotification', 'accountId': '107339370656', 'resourceDetails': [{'configItem': {'createdtime': datetime(2018, 2, 13, 16, 57, 49, 10000, tzinfo=tzutc()), 'loadbalancername': 'testClassic', 'securitygroups': ['sg-76b7c601'], 'Remaining Days': 2, 'vpcid': 'vpc-38738c43', 'instances': [{'instanceid': 'i-0dffa75bf74a9ad42'}], 'Tags': [{'Value': 'vaibhav', 'Key': 'Owner'}, {'Value': '2018-02-16', 'Key': 'RequiredTagsExpirationDate'}], 'Resource Name': 'ELB', 'subnets': ['subnet-29d69a16', 'subnet-3ac4ce71', 'subnet-4f60ac40', 'subnet-65f7b138', 'subnet-7b8dbc1f', 'subnet-eecf8dc1'], 'canonicalhostedzonenameid': 'Z35SXDOTRQ7X7K', 'availabilityzones': ['us-east-1a', 'us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e', 'us-east-1f'], 'backendserverdescriptions': [], 'policies': {'appcookiestickinesspolicies': [], 'lbcookiestickinesspolicies': [], 'otherpolicies': []}, 'NON_COMPLAINT_RESOURCE_ACTION': 'For Reference when expiration date is near', 'healthcheck': {'unhealthythreshold': 2, 'timeout': 5, 'interval': 30, 'healthythreshold': 10, 'target': 'HTTP:80/index.html'}, 'missingTags': 'Owner,Environment,Project,ExpirationDate,\n', 'sourcesecuritygroup': {'groupname': 'default', 'owneralias': '107339370656'}, 'dnsname': 'testClassic-1140076166.us-east-1.elb.amazonaws.com', 'scheme': 'internet-facing', 'canonicalhostedzonename': 'testClassic-1140076166.us-east-1.elb.amazonaws.com', 'listenerdescriptions': [{'listener': {'instanceprotocol': 'HTTP', 'loadbalancerport': 80, 'instanceport': 80, 'protocol': 'HTTP'}, 'policynames': []}], 'region': 'us-east-1'}, 'resourceType': 'AWS::ElasticLoadBalancing::LoadBalancer', 'resourceId': 'testClassic', 'evaluationMessage': 'The ELB  will be expired after 2 days.', 'ComplianceType': 'NON_COMPLIANT'}, {'configItem': {'createdtime': datetime(2018, 2, 13, 17, 25, 51, 680000, tzinfo=tzutc()), 'loadbalancername': 'testClassicMaster', 'securitygroups': ['sg-76b7c601'], 'Remaining Days': 2, 'vpcid': 'vpc-38738c43', 'instances': [{'instanceid': 'i-0dffa75bf74a9ad42'}], 'Tags': [{'Value': 'mnc', 'Key': 'Project'}, {'Value': 'vaibhav', 'Key': 'Owner'}, {'Value': '2018-02-16', 'Key': 'RequiredTagsExpirationDate'}], 'Resource Name': 'ELB', 'subnets': ['subnet-29d69a16', 'subnet-3ac4ce71', 'subnet-4f60ac40', 'subnet-65f7b138', 'subnet-7b8dbc1f', 'subnet-eecf8dc1'], 'canonicalhostedzonenameid': 'Z35SXDOTRQ7X7K', 'availabilityzones': ['us-east-1a', 'us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e', 'us-east-1f'], 'backendserverdescriptions': [], 'policies': {'appcookiestickinesspolicies': [], 'lbcookiestickinesspolicies': [], 'otherpolicies': []}, 'NON_COMPLAINT_RESOURCE_ACTION': 'For Reference when expiration date is near', 'healthcheck': {'unhealthythreshold': 2, 'timeout': 5, 'interval': 30, 'healthythreshold': 10, 'target': 'HTTP:80/index.html'}, 'missingTags': 'Owner,Environment,Project,ExpirationDate,\n', 'sourcesecuritygroup': {'groupname': 'default', 'owneralias': '107339370656'}, 'dnsname': 'testClassicMaster-605372820.us-east-1.elb.amazonaws.com', 'scheme': 'internet-facing', 'canonicalhostedzonename': 'testClassicMaster-605372820.us-east-1.elb.amazonaws.com', 'listenerdescriptions': [{'listener': {'instanceprotocol': 'HTTP', 'loadbalancerport': 80, 'instanceport': 80, 'protocol': 'HTTP'}, 'policynames': []}], 'region': 'us-east-1'}, 'resourceType': 'AWS::ElasticLoadBalancing::LoadBalancer', 'resourceId': 'testClassicMaster', 'evaluationMessage': 'The ELB  will be expired after 2 days.', 'ComplianceType': 'NON_COMPLIANT'}], 'configParam': {'notifier': 'ses', 'evaluateName': 'CheckELBRequiredTagValuesEvaluate', 'actionName': 'CheckELBRequiredTagValuesAction', 'resourceFetcherName': 'CheckELBRequiredTagValuesResourceFetcher', 'toEmail': 'vaibhav.fulsundar@reancloud.com', 'performAction': 'False', 'validity': '3', 'RequiredTags': 'Owner,Environment,Project,ExpirationDate', 'expirationDateLimit': '8'}}
LAMBDA_MESSAGE2 = {'notifier': 'ses', 'accountId': '107339370656', 'moduleName': 'CheckElbRequiredTagValues', 'aliasName': 'mnc-master', 'resourceDetails': [{'resourceId': 'testClassic', 'resourceType': 'AWS::ElasticLoadBalancing::LoadBalancer', 'configItem': {'instances': [{'instanceid': 'i-0dffa75bf74a9ad42'}], 'Tags': [{'Key': 'Owner', 'Value': 'vaibhav'}, {'Key': 'RequiredTagsExpirationDate', 'Value': '2018-02-16'}], 'NON_COMPLAINT_RESOURCE_ACTION': 'For Reference when expiration date is near', 'sourcesecuritygroup': {'groupname': 'default', 'owneralias': '107339370656'}, 'policies': {'lbcookiestickinesspolicies': [], 'otherpolicies': [], 'appcookiestickinesspolicies': []}, 'Remaining Days': 2, 'vpcid': 'vpc-38738c43', 'scheme': 'internet-facing', 'dnsname': 'testClassic-1140076166.us-east-1.elb.amazonaws.com', 'region': 'us-east-1', 'securitygroups': ['sg-76b7c601'], 'loadbalancername': 'testClassic', 'healthcheck': {'timeout': 5, 'target': 'HTTP:80/index.html', 'unhealthythreshold': 2, 'healthythreshold': 10, 'interval': 30}, 'Resource Name': 'ELB', 'createdtime': datetime(2018, 2, 13, 16, 57, 49, 10000, tzinfo=tzutc()), 'availabilityzones': ['us-east-1a', 'us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e', 'us-east-1f'], 'canonicalhostedzonenameid': 'Z35SXDOTRQ7X7K', 'backendserverdescriptions': [], 'subnets': ['subnet-29d69a16', 'subnet-3ac4ce71', 'subnet-4f60ac40', 'subnet-65f7b138', 'subnet-7b8dbc1f', 'subnet-eecf8dc1'], 'canonicalhostedzonename': 'testClassic-1140076166.us-east-1.elb.amazonaws.com', 'missingTags': 'Owner,Environment,Project,ExpirationDate,\n', 'listenerdescriptions': [{'policynames': [], 'listener': {'loadbalancerport': 80, 'protocol': 'HTTP', 'instanceport': 80, 'instanceprotocol': 'HTTP'}}]}, 'actionMessage': 'Please update the tags, if you want to retain the resource', 'ComplianceType': 'NON_COMPLIANT', 'evaluationMessage': 'The ELB  will be expired after 2 days.'}, {'resourceId': 'testClassicMaster', 'resourceType': 'AWS::ElasticLoadBalancing::LoadBalancer', 'configItem': {'instances': [{'instanceid': 'i-0dffa75bf74a9ad42'}], 'Tags': [{'Key': 'Project', 'Value': 'mnc'}, {'Key': 'Owner', 'Value': 'vaibhav'}, {'Key': 'RequiredTagsExpirationDate', 'Value': '2018-02-16'}], 'NON_COMPLAINT_RESOURCE_ACTION': 'For Reference when expiration date is near', 'sourcesecuritygroup': {'groupname': 'default', 'owneralias': '107339370656'}, 'policies': {'lbcookiestickinesspolicies': [], 'otherpolicies': [], 'appcookiestickinesspolicies': []}, 'Remaining Days': 2, 'vpcid': 'vpc-38738c43', 'scheme': 'internet-facing', 'dnsname': 'testClassicMaster-605372820.us-east-1.elb.amazonaws.com', 'region': 'us-east-1', 'securitygroups': ['sg-76b7c601'], 'loadbalancername': 'testClassicMaster', 'healthcheck': {'timeout': 5, 'target': 'HTTP:80/index.html', 'unhealthythreshold': 2, 'healthythreshold': 10, 'interval': 30}, 'Resource Name': 'ELB', 'createdtime': datetime(2018, 2, 13, 17, 25, 51, 680000, tzinfo=tzutc()), 'availabilityzones': ['us-east-1a', 'us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e', 'us-east-1f'], 'canonicalhostedzonenameid': 'Z35SXDOTRQ7X7K', 'backendserverdescriptions': [], 'subnets': ['subnet-29d69a16', 'subnet-3ac4ce71', 'subnet-4f60ac40', 'subnet-65f7b138', 'subnet-7b8dbc1f', 'subnet-eecf8dc1'], 'canonicalhostedzonename': 'testClassicMaster-605372820.us-east-1.elb.amazonaws.com', 'missingTags': 'Owner,Environment,Project,ExpirationDate,\n', 'listenerdescriptions': [{'policynames': [], 'listener': {'loadbalancerport': 80, 'protocol': 'HTTP', 'instanceport': 80, 'instanceprotocol': 'HTTP'}}]}, 'actionMessage': 'Please update the tags, if you want to retain the resource', 'ComplianceType': 'NON_COMPLIANT', 'evaluationMessage': 'The ELB  will be expired after 2 days.'}], 'messageType': 'ScheduledNotification', 'configParam': {'toEmail': 'vaibhav.fulsundar@reancloud.com', 'notifier': 'ses', 'validity': '3', 'performAction': 'False', 'expirationDateLimit': '8', 'actionName': 'CheckELBRequiredTagValuesAction', 'evaluateName': 'CheckELBRequiredTagValuesEvaluate', 'resourceFetcherName': 'CheckELBRequiredTagValuesResourceFetcher', 'RequiredTags': 'Owner,Environment,Project,ExpirationDate'}}
STS_RESPONSE = {'Account': '107339370656', 'ResponseMetadata': {'HTTPHeaders': {'content-type': 'text/xml', 'date': 'Thu, 15 Feb 2018 12:19:06 GMT', 'x-amzn-requestid': '6aeda8e0-124a-11e8-9984-5b05af858f4c', 'content-length': '414'}, 'HTTPStatusCode': 200, 'RetryAttempts': 0, 'RequestId': '6aeda8e0-124a-11e8-9984-5b05af858f4c'}, 'UserId': 'AIDAIOXK4A25UHXINGEBO', 'Arn': 'arn:aws:iam::107339370656:user/vaibhav.fulsundar'}
BUCKET_NAME = '107339370656-payload-bucket'

class TestAWSSNSNotifier(object):
    @mock_sts
    @mock_s3
    @mock_lambda
    def test_aws_lambda_notifier(self):
        eventItem = EventItems(RESOURCE_ID, RESOURCE_TYPE, CONFIG_ITEMS)
        evaluationMessage = "The ELB  will be expired after 2 days"
        messageType = "ScheduledNotification"
        evaluationResult = EvaluationResult()
        evaluationResult.complianceType = "COMPLIANT"
        notification = cof.ComplianceObjectFactory.createNotificationFrom(
                eventParam,
                eventItem,
                evaluationMessage,
                evaluationResult,
                messageType
            )
        notificationMessages = []
        notificationMessages.append(notification)
        self._AbstractNotifier__eventParam = notificationMessages
        lambdaClient = boto3.client('lambda', region_name='us-east-1')
        stsClient = boto3.client('sts', region_name='us-east-1')
        s3Resource = boto3.resource('s3', region_name='us-east-1')
        lambdaNotify.boto3.client = MagicMock(side_effect = [stsClient, lambdaClient])
        lambdaNotify.boto3.resource = MagicMock(return_value = s3Resource)
        stsClient.get_caller_identity = MagicMock(return_value = STS_RESPONSE)
        s3Resource.create_bucket(Bucket=BUCKET_NAME)
        lambdaClient.invoke_async = MagicMock(return_value = True)
        self._AWSLambdaNotifier__processNotifierResults = MagicMock(return_value=LAMBDA_MESSAGE)
        aws_lambda_notifier = lambdaNotify.AWSLambdaNotifier.notify(self)
        assert aws_lambda_notifier == True

    @mock_sts
    @mock_s3
    @mock_lambda
    def test_aws_lambda_notifier_with_action_message(self):
        eventItem = EventItems(RESOURCE_ID, RESOURCE_TYPE, CONFIG_ITEMS)
        evaluationMessage = "The ELB  will be expired after 2 days"
        messageType = "ScheduledNotification"
        evaluationResult = EvaluationResult()
        evaluationResult.complianceType = "COMPLIANT"
        notification = cof.ComplianceObjectFactory.createNotificationFrom(
                eventParam,
                eventItem,
                evaluationMessage,
                evaluationResult,
                messageType
            )
        notificationMessages = []
        notificationMessages.append(notification)
        self._AbstractNotifier__eventParam = notificationMessages
        lambdaClient = boto3.client('lambda', region_name='us-east-1')
        stsClient = boto3.client('sts', region_name='us-east-1')
        s3Resource = boto3.resource('s3', region_name='us-east-1')
        lambdaNotify.boto3.client = MagicMock(side_effect = [stsClient, lambdaClient])
        lambdaNotify.boto3.resource = MagicMock(return_value = s3Resource)
        stsClient.get_caller_identity = MagicMock(return_value = STS_RESPONSE)
        s3Resource.create_bucket(Bucket=BUCKET_NAME)
        lambdaClient.invoke_async = MagicMock(return_value = True)
        self._AWSLambdaNotifier__processNotifierResults = MagicMock(return_value=LAMBDA_MESSAGE)
        aws_lambda_notifier = lambdaNotify.AWSLambdaNotifier.notify(self)
        assert aws_lambda_notifier == True
