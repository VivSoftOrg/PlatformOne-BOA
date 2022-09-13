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
""" Pefrom Action on Heal Event"""
import os
import boto3
from common.abstract_action import AbstractAction
from common.framework_objects import EvaluationResult
from common.common_constants import BotoConstants, ComplianceConstants, ResourceConstants
from common.logger_utility import LoggerUtility
from common.boto_utility import BotoUtility
from common.i18n import Translation as _
from common.aws_common_utility import awsCommonUtility


class ProcessHealEventsAction(AbstractAction):
    """ Pefrom Action on Datadog Event"""
    def performAction(self, eventItem):
        """ perform action for the datadog events """
        evaluationResult = EvaluationResult()
        try:
            region = self._AbstractAction__eventParam.region
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            Instances = []
            parameterStoreKeyValueDict = {}
            instance_id_for_ssm = (eventItem.resourceId).strip()
            Instances.append(instance_id_for_ssm)
            if eventItem.smDocumentName == ResourceConstants.REMOTE_SCRIPT_DOCUMENT_NAME:
                smDocumentArn = eventItem.smDocumentName
            else:
                smDocumentArn = 'arn:' + awsPartitionName + ':' + 'ssm:' + region + ':' + self._AbstractAction__eventParam.lambdaAccNo + ':' + 'document/' + eventItem.smDocumentName

            ssmClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_SSM,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                region
            )
            ssmMaster = boto3.client(BotoConstants.BOTO_CLIENT_AWS_SSM)
            try:
                documentResponse = ssmMaster.describe_document(
                    Name=eventItem.smDocumentName
                )
                parameterKeyForSendCommand = "/" + self._AbstractAction__eventParam.accNo + "/"
                parameterDefaultKeyForSendCommand = "/" + ResourceConstants.SM_DEFAULT_KEY_REFERENCE + "/"
                parameterResponseForAccount = ssmMaster.get_parameters_by_path(Path=parameterKeyForSendCommand, Recursive=True, WithDecryption=True)
                parameterResponseForDefault = ssmMaster.get_parameters_by_path(Path=parameterDefaultKeyForSendCommand, Recursive=True, WithDecryption=True)

                for parameterKeyDetails in documentResponse[ResourceConstants.SM_DOCUMENT][ResourceConstants.SM_PARAMETER]:
                    try:
                        parameterKey = parameterKeyDetails[ResourceConstants.SM_PARAMETER_NAME]
                        key = parameterKeyForSendCommand + parameterKey
                        parameterKeyValue = None
                        for parameterAccounts in parameterResponseForAccount[ResourceConstants.SM_PARAMETER]:
                            if parameterAccounts[ResourceConstants.SM_PARAMETER_NAME] == key:
                                parameterKeyValue = parameterAccounts[ResourceConstants.SM_PARAMETER_VALUE]
                                break

                        if not parameterKeyValue:
                            key = parameterDefaultKeyForSendCommand + parameterKey
                            for parameterDefault in parameterResponseForDefault[ResourceConstants.SM_PARAMETER]:
                                if parameterDefault[ResourceConstants.SM_PARAMETER_NAME] == key:
                                    parameterKeyValue = parameterDefault[ResourceConstants.SM_PARAMETER_VALUE]
                                    break

                        if parameterKeyValue:
                            parameterStoreKeyValueDict[parameterKey] = [parameterKeyValue]

                    except Exception as e:
                        LoggerUtility.logError("Unable to find {}, {} the key combinations in parameter store".format(parameterKeyForSendCommand, parameterDefaultKeyForSendCommand))
                        LoggerUtility.logError(e)
                smExecutionLogBucketName = os.environ[ResourceConstants.SM_EXECUTION_LOG_BUCKET]
                mncHealingScripts = os.environ[ResourceConstants.MNC_HEAL_BUCKET]
                awsCommonUtility.modifySmDocumentPermission(True, eventItem.smDocumentName, self._AbstractAction__eventParam.accNo)
                if eventItem.smDocumentName == ResourceConstants.REMOTE_SCRIPT_DOCUMENT_NAME:
                    response = ssmClient.send_command(
                        InstanceIds=Instances,
                        DocumentName=smDocumentArn,
                        Comment=ResourceConstants.SM_DOCUMENT_EXECUTION_COMMENT,
                        Parameters={"sourceType": ["S3"],
                                    "sourceInfo": ["{\"path\": \"" + ResourceConstants.PATH.format(mncHealingScripts) + eventItem.s3BucketPath + "\"}"],
                                    "commandLine": [eventItem.scriptName]},
                        OutputS3BucketName=smExecutionLogBucketName,
                        OutputS3KeyPrefix=self._AbstractAction__eventParam.accNo
                    )
                else:
                    response = ssmClient.send_command(
                        InstanceIds=Instances,
                        DocumentName=smDocumentArn,
                        Comment=ResourceConstants.SM_DOCUMENT_EXECUTION_COMMENT,
                        Parameters=parameterStoreKeyValueDict,
                        OutputS3BucketName=smExecutionLogBucketName,
                        OutputS3KeyPrefix=self._AbstractAction__eventParam.accNo)
                    # Updating sm parameters.
                    eventItem.parameters = parameterStoreKeyValueDict
                eventItem.commandId = response[ResourceConstants.COMMAND_REFERENCE][ResourceConstants.COMMAND_ID]

                if response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                    LoggerUtility.logInfo("Command successfully send to host with id {}".format(eventItem.resourceId))
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Command successfully send to SM.")
                    self._AbstractAction__actionMessage = evaluationResult.annotation
                else:
                    LoggerUtility.logInfo("Error:Command not send to host with id {}".format(eventItem.resourceId))
                awsCommonUtility.modifySmDocumentPermission(False, eventItem.smDocumentName, self._AbstractAction__eventParam.accNo)

            except Exception as e:
                awsCommonUtility.modifySmDocumentPermission(False, eventItem.smDocumentName, self._AbstractAction__eventParam.accNo)
                errorMessage = "Error occured while sending sm-document/sm-script to host."
                LoggerUtility.logError(errorMessage)
                LoggerUtility.logInfo("Error is {}".format(str(e)))
                evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
                evaluationResult.annotation = _(errorMessage)
                self._AbstractAction__actionMessage = evaluationResult.annotation
        except Exception as e:
            errorMessage = "Failed to perform Action on the Host {}.".format(eventItem.resourceId)
            LoggerUtility.logError(errorMessage)
            LoggerUtility.logInfo("Error is {}".format(str(e)))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)
            self._AbstractAction__actionMessage = evaluationResult.annotation

        return evaluationResult
