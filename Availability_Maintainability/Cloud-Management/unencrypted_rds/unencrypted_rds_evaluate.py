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
"""This module will Evaluate the Rule and mark resource as compliant or non_Compliant based on behaviour."""
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_evaluate import AbstractEvaluator
from common.common_utility import CommonUtility
from common.common_constants import ComplianceConstants, BotoConstants, ManagedCloudConstants
from common.rds_constants import RdsConstants
from common.framework_objects import EvaluationResult
from common.logger_utility import LoggerUtility


class UnencryptedRdsEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """
    def evaluate(self, eventItem):
        errorMessage = ""
        evaluationResult = EvaluationResult()
        try:

            if eventItem.configItems[RdsConstants.RDS_STORAGE_ENCRYPTED]:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = "The DB instance is encrypted"
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                LoggerUtility.logInfo("The DB instance {} is encrypted".format(eventItem.resourceId))

            else:
                awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
                dbArn = eventItem.configItems[RdsConstants.RDS_ARN_KEY]
                rdsClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_RDS,
                    self._AbstractEvaluator__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
                )
                try:
                    tagValues = CommonUtility.changeDictionaryKeysToLowerCase(rdsClient.list_tags_for_resource(ResourceName=dbArn))
                    LoggerUtility.logInfo(tagValues)
                    eventItem.configItems.update({'tags': tagValues['taglist']})
                except ClientError as e:
                    LoggerUtility.logError("Boto client error occured. {}".format(e))
                except Exception as e:
                    LoggerUtility.logInfo("The RDS instance - '{}' does not have tags!".format(eventItem.resourceId))

                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "The DB Instance is not encrypted"
                self._AbstractEvaluator__recommendationMessage = "Please create a snapshot of your DB instance, " \
                                                                 "and then create an encrypted copy of that snapshot. " \
                                                                 "You can then restore your DB instance from the encrypted snapshot. " \
                                                                 "However you don't need to encrypt an Amazon Aurora DB cluster snapshot, " \
                                                                 "in order to create an encrypted copy of that cluster just specify a KMS encryption key " \
                                                                 "when restoring from an unencrypted DB cluster snapshot."
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                LoggerUtility.logInfo("The DB Instance {} is not encrypted".format(eventItem.resourceId))

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while evaluating unencrypted RDS. {}".format(e)
        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = errorMessage
            self._AbstractEvaluator__evaluatorMessage = errorMessage
        return evaluationResult
