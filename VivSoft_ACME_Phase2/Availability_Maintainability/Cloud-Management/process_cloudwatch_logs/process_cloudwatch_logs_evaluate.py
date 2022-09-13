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
# pylint: disable=W0621
""" Evalute Cloudwatch Event"""
import boto3
import yaml
from common.abstract_evaluate import AbstractEvaluator
from common.framework_objects import EvaluationResult
from common.common_constants import ComplianceConstants
from common.common_constants import BotoConstants
from common.common_constants import ResourceConstants
from common.common_constants import ManagedCloudConstants
from common.logger_utility import LoggerUtility
from common.common_utility import CommonUtility
from common.account_info import AccountInfo


class ProcessCloudwatchLogsEvaluate(AbstractEvaluator):
    """ Evalute Cloudwatch Event"""

    def __getEventItemDetails(self, eventItemDictionary):
        """ Method to get event item details """
        complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
        eventName = eventItemDictionary['cloudwatchMessage']['eventName']
        eventSource = eventItemDictionary['cloudwatchMessage']['eventSource']
        if "InternetGateway" in eventName:
            ruleName = "Federal - IGW - Notify and Log"
            violationMessage = "Internet gateway is either created, updated or deleted."
        elif "Vpn" in eventName:
            ruleName = "Federal - VPN tunnels - Notify and Log"
            violationMessage = "VPN tunnel is either created, updated or deleted."
        elif "Subnet" in eventName:
            ruleName = "Federal - Subnet - Notify and Log"
            violationMessage = "Subnet is either created, updated or deleted."
        elif "AttachVolume" in eventName:
            ruleName = "Federal - EBS attachments to EC2 - Notify and Log"
            violationMessage = "EBS volume has been attached to EC2 instance."
        elif "Vpc" in eventName:
            ruleName = "Federal - VPC - Notify and Log"
            violationMessage = "VPC is either created, updated or deleted."
        elif "SecurityGroupIngress" in eventName and "ipPermissions" in eventItemDictionary['cloudwatchMessage']["requestParameters"]:
            ruleName = "Federal - Security Groups Source Change - Notify and Log"
            violationMessage = "Security group source changed."
        elif "SecurityGroup" in eventName:
            ruleName = "Federal - Security Groups - Notify and Log"
            violationMessage = "Security group is either created, updated or deleted."
        elif "RouteTable" in eventName:
            ruleName = "Federal - Route Table - Notify and Log"
            violationMessage = "Route table is either created, updated or deleted."
        elif "errorCode" in eventItemDictionary['cloudwatchMessage']:
            ruleName = "Federal - Failed API Calls - Notify and Log"
            violationMessage = "Failed API calls has been created by the IAM user or IAM role."
        elif "ConsoleLogin" in eventName:
            ruleName = "Federal - Failed Logins - Notify and Log"
            violationMessage = "The IAM or root user has a failed AWS console login."
        elif "lambda" in eventSource:
            ruleName = "Federal - Lambdas-VPC - Notify and Log"
            violationMessage = "The lambda is not present in a VPC."
        elif "config" in eventSource:
            ruleName = "Federal - AWS Config changes - Notify and Log"
            violationMessage = "AWS Config has been updated."
        elif "iam" in eventSource:
            ruleName = "Federal - IAM Policy Changes - Notify and Log"
            violationMessage = "IAM policy has been changed."
        elif "CreateDBInstance" in eventName:
            ruleName = "Federal - Unencrypted RDS Instance - Notify and Log"
            violationMessage = "An unencrypted RDS has been created."
        elif "CreateVolume" in eventName:
            ruleName = "Federal - Unencrypted EBS - Notify and Log"
            violationMessage = "Unencrypted EBS has been created."
        elif "Policy" in eventName and "s3" in eventSource:
            ruleName = "Federal - S3 Bucket Policy Changes - Notify and Log"
            violationMessage = "S3 bucket policy has been changed."
        elif "Instances" in eventName:
            ruleName = "Federal - EC2 Instance Changes - Notify and Log"
            violationMessage = "EC2 instance has been either created, updated or deleted."
            complianceType = self.__processEc2InstanceChanges(eventItemDictionary)
        else:
            ruleName = "Unknown Rule"
            violationMessage = "Changes were occurred in unknown resource."

        return ruleName, violationMessage, complianceType

    def __processEc2InstanceChanges(self, eventItemDictionary):
        """ method to evaluate ec2 instance changes """
        try:
            complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
            accountId = AccountInfo.getAwsAccountNumber()
            s3BucketName = ManagedCloudConstants.MNC_ACCOUNT_DETAILS_BUCKET_NAME.format(accountId)
            objectData = CommonUtility.getDataFromS3Bucket(s3BucketName, ManagedCloudConstants.MNC_CLOUDWATCH_INPUT_VARIABLES_FILE_NAME)
            inputData = yaml.load(objectData)
            excludeSubnetIds = inputData[ResourceConstants.EXCLUDE_SUBNET_IDS].split(',')
            ec2Client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_EC2)
            response = ec2Client.describe_instances(InstanceIds=[eventItemDictionary['cloudwatchMessage']["responseElements"]["instancesSet"]["items"][0]["instanceId"]])
            subnetId = response["Reservations"][0]["Instances"][0]["SubnetId"]
            if subnetId in excludeSubnetIds:
                complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
            return complianceType
        except Exception as e:
            LoggerUtility.logError("Error occurred while processing ec2 instance changes : {}".format(e))

    def evaluate(self, eventItem):
        eventItemDictionary = vars(eventItem)
        eventItem.ruleName, eventItem.violationMessage, complianceType = self.__getEventItemDetails(eventItemDictionary)
        evaluationResult = EvaluationResult()
        evaluationResult.complianceType = complianceType
        evaluationResult.annotation = "The Resource is not compliant"
        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        return evaluationResult
