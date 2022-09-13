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
""" This module will take action to delete or disable access key.  """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.logger_utility import LoggerUtility
from common.IAMConstants import IAMConstants
from common.framework_objects import EvaluationResult
from common.common_constants import BotoConstants, ComplianceConstants, CommonKeywords


class IamKeysAgeAction(AbstractAction):
    """ This class will take action to delete or disable access key. """
    def performAction(self, eventItem):
        evaluationResult = EvaluationResult()
        errorMessage = ""
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            iamClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_IAM,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName
            )
            action = eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION]
            accessKeyId = eventItem.configItems[IAMConstants.IAM_ACCESS_KEY_ID]
            accessKeyStatus = eventItem.configItems[IAMConstants.IAM_ACCESS_KEY_STATUS]
            userName = eventItem.configItems[IAMConstants.IAM_USER_NAME]

            if action == CommonKeywords.DELETE:
                response = iamClient.delete_access_key(AccessKeyId=accessKeyId, UserName=userName)
                responseStatusCode = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]
                if responseStatusCode == 200:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = "IAM access key deleted."
                else:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = 'Failed to delete IAM access key. Response code {}'.format(responseStatusCode)
            elif action == CommonKeywords.DISABLE:
                actionMessage = "IAM access key deactivated."
                if accessKeyStatus == IAMConstants.IAM_KEY_ACTIVE:
                    response = iamClient.update_access_key(AccessKeyId=accessKeyId,
                                                           Status=IAMConstants.IAM_KEY_INACTIVE, UserName=userName)
                    responseStatusCode = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]
                    if responseStatusCode == 200:
                        evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                        evaluationResult.annotation = actionMessage
                    else:
                        errorMessage = 'IAM access key disable failed. Response code {}'.format(responseStatusCode)
                else:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = actionMessage
            elif action == CommonKeywords.DELETE_NOTIFICATION:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = "IAM access key will be deleted."
            elif action == CommonKeywords.DISABLE_NOTIFICATION:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = 'IAM access key will be deactivated.'

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type doesn't possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while performing action on IAM access key. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = errorMessage
        else:
            LoggerUtility.logInfo(evaluationResult.annotation)

        self._AbstractAction__actionMessage = evaluationResult.annotation
        return evaluationResult
