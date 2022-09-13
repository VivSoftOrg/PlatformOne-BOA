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
"""This module will evaluate the alerts coming from dataDog."""
import os
import re
import json
import boto3
from boto3.dynamodb.conditions import Key
from common.abstract_evaluate import AbstractEvaluator
from common.framework_objects import EvaluationResult
from common.common_constants import BotoConstants, ComplianceConstants, ManagedCloudConstants, ResourceConstants
from common.logger_utility import LoggerUtility
from common.i18n import Translation as _


class ProcessHealEventsEvaluate(AbstractEvaluator):
    """This class will Evaluate the data and makes decision for taking Action."""

    def evaluate(self, eventItem):
        """evalute the event"""
        evaluationResult = EvaluationResult()
        alertScriptList = []
        smDocumentList = []
        logDictionary = {}
        logDictionary[ResourceConstants.SM_HOST_ID] = eventItem.resourceId
        s3BucketPathList = []
        scrpitName = []
        awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
        try:
            dynamoDBResource = boto3.resource(BotoConstants.BOTO_CLIENT_AWS_DYNAMO_DB)
            awsAccountNumber = self._AbstractEvaluator__eventParam.accNo
            AlertScriptMappingTableName = os.environ[ManagedCloudConstants.MNC_ALERT_SCRIPT_MAPPING_TABLE]
            table = dynamoDBResource.Table(AlertScriptMappingTableName)
            response = table.query(KeyConditionExpression=Key(ManagedCloudConstants.MNC_PRODUCT_REFERENCE).eq(ManagedCloudConstants.MNC_HEAL))
            processingAlert = eventItem.processingAlert
            evaluateresponse = response[ResourceConstants.RESPONSE_ITEMS][0]
            alertScriptList = evaluateresponse[ResourceConstants.AWS_ACCOUNT_NO][awsAccountNumber]
            for oneAlert in alertScriptList:
                match = re.match(oneAlert[ResourceConstants.ALERT_MATCH_CONTAIN_PATTERN], processingAlert)
                if match:
                    logDictionary[ResourceConstants.SM_PATTERN_TO_MATCH] = oneAlert[ResourceConstants.ALERT_MATCH_CONTAIN_PATTERN]
                    dryRun = oneAlert[ResourceConstants.SM_DRY_RUN_ACTION_STATUS]
                    if ManagedCloudConstants.MNC_SCRIPT_PATH in oneAlert:
                        smDocumentList.append(ResourceConstants.REMOTE_SCRIPT_DOCUMENT_NAME)
                        logDictionary[ResourceConstants.SM_RULES_MATCHED] = smDocumentList
                        s3BucketPathList.append(oneAlert[ManagedCloudConstants.MNC_SCRIPT_PATH])
                    else:
                        smDocumentList.append(oneAlert[ResourceConstants.SM_DOCUMENT_NAME])
                        logDictionary[ResourceConstants.SM_RULES_MATCHED] = smDocumentList

            if len(smDocumentList) == 1:
                eventItem.smDocumentName = smDocumentList[0]
                if len(s3BucketPathList) == 1:
                    eventItem.s3BucketPath = s3BucketPathList[0]
                    script = eventItem.s3BucketPath.split("/")
                    eventItem.scriptName = script[len(script) - 1]
                LoggerUtility.logInfo("Pattern matched for Alert. Sending SM-Document to SM.")
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("Pattern matched for Alert. Sending SM-Document to SM.")
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                try:
                    if self._AbstractEvaluator__eventParam.eventParamType != ManagedCloudConstants.MNC_CLOUDWATCH_ALARM_KEYWORD:
                        eventItem.dryRun = dryRun
                    if eventItem.dryRun is True:
                        logDictionary[ResourceConstants.SM_ACTION_STATUS] = ResourceConstants.SM_DRY_RUN_ACTION_STATUS
                    else:
                        logDictionary[ResourceConstants.SM_ACTION_STATUS] = ResourceConstants.SM_EXECUTED_ACTION_STATUS
                except Exception as e:
                    eventItem.dryRun = False
            elif len(smDocumentList) > 1:
                LoggerUtility.logInfo("Multiple scripts found. Script list is: ", smDocumentList)
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                evaluationResult.annotation = _("Multiple scripts found.")
                logDictionary[ResourceConstants.SM_ACTION_STATUS] = ResourceConstants.SM_SKIPPED_ACTION_STATUS
            else:
                LoggerUtility.logInfo("Failed to match Pattern for alert.")
                evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
                evaluationResult.annotation = _("Failed to match Pattern for alert.")
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        except Exception as e:
            LoggerUtility.logInfo("Error While Evaluating Datadog alert.")
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _("Error While Evaluating DataDog alert.")
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        LoggerUtility.logInfo("Rule Execution Status: %s" % json.dumps(logDictionary))
        return evaluationResult
