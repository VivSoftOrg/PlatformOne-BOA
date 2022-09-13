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
import mock
import sys
import boto3
from mock import MagicMock
from moto import mock_ses
from common.common_utility import *
from common.common_constants import *
sys.path.append('notifiers/ses/')
from aws_ses_notifier import *

EVENTJSON_WITHOUT_TO_EMAIL = {
    "Records": [
      {
        "EventSource": "aws:sns",
        "EventVersion": "1.0",
        "EventSubscriptionArn": "arn:aws:sns:us-east-1:107339370656:sns-testing:95903905-199c-485b-9197-199ca3228116",
        "Sns": {
          "Type": "Notification",
          "MessageId": "7563e605-b19c-5ee8-b565-b42c273f3f78",
          "TopicArn": "arn:aws:sns:us-east-1:107339370656:sns-testing",
          "Subject": "SNS Message",
          "Message": "{\"configParam\": {\"performAction\": \"True\", \"notifier\": \"ses\", \"forbiddenPorts\": \"22\"}, \"accountId\": \"107339370656\", \"resourceDetails\": [{\"configItem\": {\"rootdevicetype\": \"ebs\", \"instanceid\": \"i-cb660d3b\", \"placement\": {\"tenancy\": \"default\", \"groupname\": \"\", \"availabilityzone\": \"us-east-1b\"}, \"statereason\": {\"message\": \"Client.UserInitiatedShutdown: User initiated shutdown\", \"code\": \"Client.UserInitiatedShutdown\"}, \"virtualizationtype\": \"hvm\", \"tags\": [{\"key\": \"Name\", \"value\": \"win_2003_new_ssd\"}], \"sourcedestcheck\": true, \"rootdevicename\": \"/dev/sda1\", \"clienttoken\": \"skwQN1426316216934\", \"amilaunchindex\": 0, \"subnetid\": \"subnet-da04a4f1\", \"ebsoptimized\": false, \"productcodes\": [], \"platform\": \"windows\", \"networkinterfaces\": [{\"groups\": [{\"groupid\": \"sg-cead26aa\", \"groupname\": \"launch-wizard-1\"}], \"vpcid\": \"vpc-47105e22\", \"privateipaddress\": \"172.31.54.203\", \"privateipaddresses\": [{\"privatednsname\": \"ip-172-31-54-203.ec2.internal\", \"primary\": true, \"privateipaddress\": \"172.31.54.203\"}], \"sourcedestcheck\": true, \"privatednsname\": \"ip-172-31-54-203.ec2.internal\", \"description\": \"\", \"networkinterfaceid\": \"eni-a288b18f\", \"subnetid\": \"subnet-da04a4f1\", \"attachment\": {\"status\": \"attached\", \"attachtime\": \"2015-03-14T06:57:03+00:00\", \"attachmentid\": \"eni-attach-0865f774\", \"deleteontermination\": true, \"deviceindex\": 0}, \"status\": \"in-use\", \"macaddress\": \"12:e6:db:41:b9:8b\", \"ownerid\": \"107339370656\"}], \"keyname\": \"CloudEndureKP\", \"architecture\": \"x86_64\", \"securitygroups\": [{\"groupid\": \"sg-cead26aa\", \"groupname\": \"launch-wizard-1\"}], \"vpcid\": \"vpc-47105e22\", \"instancetype\": \"t2.medium\", \"hypervisor\": \"xen\", \"state\": {\"code\": 80, \"name\": \"stopped\"}, \"imageid\": \"ami-1286a77a\", \"monitoring\": {\"state\": \"disabled\"}, \"privatednsname\": \"ip-172-31-54-203.ec2.internal\", \"privateipaddress\": \"172.31.54.203\", \"blockdevicemappings\": [], \"launchtime\": \"2015-03-23T08:25:36+00:00\", \"publicdnsname\": \"\", \"statetransitionreason\": \"User initiated (2015-03-23 08:31:08 GMT)\"}, \"resourceId\": \"i-cb660d3b\", \"ComplianceType\": \"NON_COMPLIANT\", \"evaluationMessage\": \"This resource is compliant with the rule.\", \"resourceType\": \"AWS::EC2::Instance\"}], \"notifier\": \"ses\"}",
          "Timestamp": "2017-09-06T06:23:31.136Z",
          "SignatureVersion": "1",
          "Signature": "KDYBNEs601RXv0uyi1ElzSEtCIo+u6vlKpYRgxIHsRFCsPqOV6cqYbPWpKiJ3hN2VNzWAZ1qcL51xJzmTJg3HsqwcjoUqvEBfMCw5RduI3EprFtEh7F67Te4ae4gAwDrLxQKKjUaMuC8qjZfBDc/br/no6XE+2zcwykz0pJO30Okt0Ku0nThJ2Tqo7y4bgBqqBvjjZsJNK7vG55XZPpxrvs3JlBf8cHgYwo0W3c0kiTPl/JRy8PEjdZvBc4Pv97kLgLSi4GviGwdp96+emmaJczYXduuvQlQ/5N0b4eQyFJzNwm9YOj6dINM0v9uPksQR92qCHEF52QVqhYQAF++uQ==",
          "SigningCertUrl": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-433026a4050d206028891664da859041.pem', 'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:107339370656:sns-testing:95903905-199c-485b-9197-199ca3228116",
          "MessageAttributes": {}
        }
      }
    ]
  }

EVENTJSON_WITHOUT_NOTIFIER = {
    "Records": [
      {
        "EventSource": "aws:sns",
        "EventVersion": "1.0",
        "EventSubscriptionArn": "arn:aws:sns:us-east-1:107339370656:sns-testing:95903905-199c-485b-9197-199ca3228116",
        "Sns": {
          "Type": "Notification",
          "MessageId": "7563e605-b19c-5ee8-b565-b42c273f3f78",
          "TopicArn": "arn:aws:sns:us-east-1:107339370656:sns-testing",
          "Subject": "SNS Message",
          "Message": "{\"configParam\": {\"performAction\": \"True\", \"notifier\": \"\", \"toEmail\": \"anish.bhagwat@reancloud.com\", \"forbiddenPorts\": \"22\"}, \"accountId\": \"107339370656\", \"resourceDetails\": [{\"configItem\": {\"rootdevicetype\": \"ebs\", \"instanceid\": \"i-cb660d3b\", \"placement\": {\"tenancy\": \"default\", \"groupname\": \"\", \"availabilityzone\": \"us-east-1b\"}, \"statereason\": {\"message\": \"Client.UserInitiatedShutdown: User initiated shutdown\", \"code\": \"Client.UserInitiatedShutdown\"}, \"virtualizationtype\": \"hvm\", \"tags\": [{\"key\": \"Name\", \"value\": \"win_2003_new_ssd\"}], \"sourcedestcheck\": true, \"rootdevicename\": \"/dev/sda1\", \"clienttoken\": \"skwQN1426316216934\", \"amilaunchindex\": 0, \"subnetid\": \"subnet-da04a4f1\", \"ebsoptimized\": false, \"productcodes\": [], \"platform\": \"windows\", \"networkinterfaces\": [{\"groups\": [{\"groupid\": \"sg-cead26aa\", \"groupname\": \"launch-wizard-1\"}], \"vpcid\": \"vpc-47105e22\", \"privateipaddress\": \"172.31.54.203\", \"privateipaddresses\": [{\"privatednsname\": \"ip-172-31-54-203.ec2.internal\", \"primary\": true, \"privateipaddress\": \"172.31.54.203\"}], \"sourcedestcheck\": true, \"privatednsname\": \"ip-172-31-54-203.ec2.internal\", \"description\": \"\", \"networkinterfaceid\": \"eni-a288b18f\", \"subnetid\": \"subnet-da04a4f1\", \"attachment\": {\"status\": \"attached\", \"attachtime\": \"2015-03-14T06:57:03+00:00\", \"attachmentid\": \"eni-attach-0865f774\", \"deleteontermination\": true, \"deviceindex\": 0}, \"status\": \"in-use\", \"macaddress\": \"12:e6:db:41:b9:8b\", \"ownerid\": \"107339370656\"}], \"keyname\": \"CloudEndureKP\", \"architecture\": \"x86_64\", \"securitygroups\": [{\"groupid\": \"sg-cead26aa\", \"groupname\": \"launch-wizard-1\"}], \"vpcid\": \"vpc-47105e22\", \"instancetype\": \"t2.medium\", \"hypervisor\": \"xen\", \"state\": {\"code\": 80, \"name\": \"stopped\"}, \"imageid\": \"ami-1286a77a\", \"monitoring\": {\"state\": \"disabled\"}, \"privatednsname\": \"ip-172-31-54-203.ec2.internal\", \"privateipaddress\": \"172.31.54.203\", \"blockdevicemappings\": [], \"launchtime\": \"2015-03-23T08:25:36+00:00\", \"publicdnsname\": \"\", \"statetransitionreason\": \"User initiated (2015-03-23 08:31:08 GMT)\"}, \"resourceId\": \"i-cb660d3b\", \"ComplianceType\": \"NON_COMPLIANT\", \"evaluationMessage\": \"This resource is compliant with the rule.\", \"resourceType\": \"AWS::EC2::Instance\"}], \"notifier\": \"ses\"}",
          "Timestamp": "2017-09-06T06:23:31.136Z",
          "SignatureVersion": "1",
          "Signature": "KDYBNEs601RXv0uyi1ElzSEtCIo+u6vlKpYRgxIHsRFCsPqOV6cqYbPWpKiJ3hN2VNzWAZ1qcL51xJzmTJg3HsqwcjoUqvEBfMCw5RduI3EprFtEh7F67Te4ae4gAwDrLxQKKjUaMuC8qjZfBDc/br/no6XE+2zcwykz0pJO30Okt0Ku0nThJ2Tqo7y4bgBqqBvjjZsJNK7vG55XZPpxrvs3JlBf8cHgYwo0W3c0kiTPl/JRy8PEjdZvBc4Pv97kLgLSi4GviGwdp96+emmaJczYXduuvQlQ/5N0b4eQyFJzNwm9YOj6dINM0v9uPksQR92qCHEF52QVqhYQAF++uQ==",
          "SigningCertUrl": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-433026a4050d206028891664da859041.pem', 'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:107339370656:sns-testing:95903905-199c-485b-9197-199ca3228116",
          "MessageAttributes": {}
        }
      }
    ]
  }

CONTEXT = ""


class TestSESNotifier():

        __dir_path = os.path.dirname(os.path.realpath(__file__))
        __sampleInvokingEventFileName = "/sample_invoking_event.json"
        __sampleScheduledEventFileName = "/sample_scheduled_event.json"
        __awsRegion = "us-east-1"
        __testMailId = "pytest@tests.com"

        @mock_ses
        def testSESNotifierWithoutAwsSesRegion(self):
            sesNotifier = SESNotifier()
            eventJson = CommonUtility.readJsonFromFile(self.__dir_path + self.__sampleInvokingEventFileName)
            with pytest.raises(Exception, message="AWS SES region not configured! Failed to send notification email!"):
                sesNotifier.processNotifiersUsing(eventJson, CONTEXT)
                pass

        @mock_ses
        def testSESNotifierWithoutSenderMail(self):
            sesNotifier = SESNotifier()
            os.environ['SES_AWS_REGION'] = self.__awsRegion
            eventJson = CommonUtility.readJsonFromFile(self.__dir_path + self.__sampleInvokingEventFileName)
            with pytest.raises(Exception, message="Sender Email address not configured! Failed to send notification email!"):
                sesNotifier.processNotifiersUsing(eventJson, CONTEXT)
                pass

        @mock_ses
        def testSESNotifierWithoutRecepientEmail(self):
            sesNotifier = SESNotifier()
            os.environ['SES_SENDER_MAIL_ID'] = self.__testMailId
            with pytest.raises(Exception, message="Recepient Email address not found in the input event! Failed to send notification email!"):
                sesNotifier.processNotifiersUsing(EVENTJSON_WITHOUT_TO_EMAIL, CONTEXT)
                pass

        @mock_ses
        def testSESNotifierWithoutNotifier(self):
            sesNotifier = SESNotifier()
            sesClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_SES, region_name=self.__awsRegion)
            sesClient.verify_email_identity(EmailAddress=self.__testMailId)
            sesClient.send_email = MagicMock(return_value=True)
            sesNotifier.processNotifiersUsing(EVENTJSON_WITHOUT_NOTIFIER, CONTEXT)

        @mock_ses
        def testSESNotifierForInvokingEvent(self):
            sesNotifier = SESNotifier()
            sesClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_SES, region_name=self.__awsRegion)
            sesClient.verify_email_identity(EmailAddress=self.__testMailId)
            sesClient.send_email = MagicMock(return_value=True)
            eventJson = CommonUtility.readJsonFromFile(self.__dir_path + self.__sampleInvokingEventFileName)
            sesNotifier.processNotifiersUsing(eventJson, CONTEXT)

        @mock_ses
        def testSESNotifierForScheduledEvent(self):
            sesNotifier = SESNotifier()
            sesClient = boto3.client(BotoConstants.BOTO_CLIENT_AWS_SES, region_name=self.__awsRegion)
            sesClient.verify_email_identity(EmailAddress=self.__testMailId)
            sesClient.send_email = MagicMock(return_value=True)
            eventJson = CommonUtility.readJsonFromFile(self.__dir_path + self.__sampleScheduledEventFileName)
            sesNotifier.processNotifiersUsing(eventJson, CONTEXT)
