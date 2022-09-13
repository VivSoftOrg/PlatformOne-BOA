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
"""LOG AND NOTIFY KINESIS CONSUMER"""
import os
import json
import traceback
import boto3
from common.logger_utility import LoggerUtility
from common.common_constants import AWSKinesisConstants, AWSCloudwatchConstants, BotoConstants, ManagedCloudConstants, ResourceConstants


def lambda_handler(event, context):
    """This Is An Entry Point for events coming from Kinesis Data Streams"""
    # Catch any exception at runtime to avoid unwanted re-processing of Kinesis batch
    try:
        LoggerUtility.setLevel()
        records_from_stream = event[AWSKinesisConstants.KINESIS_RECORD_KEYWORD_REFERENCE]
        lambda_client = boto3.client(BotoConstants.BOTO_CLIENT_AWS_LAMBDA)
        for kinesis_record in records_from_stream:
            LoggerUtility.logInfo("KINESIS SEQUENCE NUMBER: " + str(kinesis_record[AWSKinesisConstants.KINESIS_KEYWORD_REFERENCE][AWSKinesisConstants.KINESIS_SEQUENCE_NUMBER_REFERENCE]) + " || KINESIS EVENT ID: " + str(kinesis_record[AWSKinesisConstants.KINESIS_EVENT_ID_REFERENCE]))
            lambda_client.invoke(
                FunctionName=os.environ[ManagedCloudConstants.MNC_RULE_PROCESSOR_LAMBDA_FUNCTION_NAME_ENV_VAR],
                InvocationType=ResourceConstants.EVENT,
                Payload=json.dumps({AWSCloudwatchConstants.CLOUDWATCH_AWS_LOGS_REFERENCE: kinesis_record[AWSKinesisConstants.KINESIS_KEYWORD_REFERENCE]})
            )
        LoggerUtility.logInfo("Triggered mnc rule processor for " + str(len(records_from_stream)) + " kinesis records!")
    except Exception as kinesis_batch_error:
        LoggerUtility.logError("Failed to process batch: " + str(event))
        LoggerUtility.logError("EXCEPTION: " + str(kinesis_batch_error) + ";STACKTRACE: " + str(traceback.format_exc()))
