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
"""This module will perform action based on the Evaluation Result."""
from datetime import date, timedelta
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.framework_objects import EvaluationResult
from common.common_constants import ComplianceConstants, BotoConstants, ManagedCloudConstants
from dynamodb_table_expiration.dynamodb_table_expiration_constants import Constants


class DynamoDBTableAction(AbstractAction):
    """This class perform action as it stop Instances if it is non_compliant """
    def __deleteTable(self, tableClient, eventItem):
        """Method is used to delete Table"""
        try:
            response = tableClient.delete_table(TableName=eventItem.resourceId)

            requestStatus = response[Constants.DYNAMO_DB_RESPONSE_METADATA][Constants.DYNAMO_DB_HTTP_STATUS_CODE]
            if requestStatus == 200:
                message = "The DynamoDB table was expired, hence it has been deleted."
                self._AbstractAction__actionMessage = _(message)
                LoggerUtility.logInfo(message)
                return True

            else:
                message = "Error deleting the DynamoDB table : {}, HTTPStatus Code : {}.".format(eventItem.resourceId,
                                                                                                 requestStatus)
                self._AbstractAction__actionMessage = _(message)
                LoggerUtility.logError(message)
                return False
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            return False
        except Exception as e:
            LoggerUtility.logError("Error occured while deleting Table. {}".format(e))
            return False

    def __addExpirationDateTag(self, tableClient, eventItem):
        """Method will create Expirationdate to the Table."""
        try:
            defaultValidity = int(self._AbstractAction__eventParam.configParam[Constants.DYNAMO_DB_VALIDITY_RULE_PARAM])
            expirationDate = (date.today() + timedelta(days=defaultValidity)).isoformat()
            expirationTag = [
                {
                    'Key': Constants.DYNAMO_DB_EXPIRATION_TAG_REFERENCE,
                    'Value': expirationDate
                }
            ]

            response = tableClient.tag_resource(
                ResourceArn=eventItem.configItems['ARN'],
                Tags=expirationTag
            )
            requestStatus = response[Constants.DYNAMO_DB_RESPONSE_METADATA][Constants.DYNAMO_DB_HTTP_STATUS_CODE]

            if requestStatus == 200:
                self._AbstractAction__actionMessage = _("An ExpirationDate tag has been added to the table.")
                LoggerUtility.logInfo("An ExpirationDate tag has been added to `{}` with date `{}`"
                                      .format(eventItem.resourceId, expirationDate))
                return True

            else:
                message = "Error adding ExpirationDate tag to the DynamoDB table : {}, HTTPStatus Code : {}.".format(eventItem.resourceId, requestStatus)
                self._AbstractAction__actionMessage = _(message)
                LoggerUtility.logError(message)
                return False

        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            return False
        except Exception as e:
            LoggerUtility.logError("Error occured while adding ExpirationDate tag. {}".format(e))
            return False

    def performAction(self, eventItem):
        evaluationResult = EvaluationResult()
        errorMessage = ""
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            dynamoDBClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_DYNAMO_DB,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            response = False

            if eventItem.configItems['action'] == Constants.DYNAMO_DB_TABLE_VALIDITY_EXPIRED:
                response = self.__deleteTable(dynamoDBClient, eventItem)
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("The DynamoDB table was expired, hence it has been deleted.")
            elif eventItem.configItems['action'] == Constants.DYNAMO_DB_TABLE_EXPIRATION_DATE_NOT_FOUND or \
                eventItem.configItems['action'] == Constants.DYNAMO_DB_TABLE_EXPIRATION_DATE_LIMIT_EXCEEDED or \
                    eventItem.configItems['action'] == Constants.DYNAMO_DB_TABLE_EXPIRATION_DATE_INVALID:
                response = self.__addExpirationDateTag(dynamoDBClient, eventItem)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("An ExpirationDate tag has been added to the table.")
            elif eventItem.configItems['action'] == Constants.DYNAMO_DB_TABLE_ABOUT_TO_EXPIRE:
                response = self._AbstractAction__actionMessage = _(
                    "Please update the expiration date if you want to retain the table")
                LoggerUtility.logInfo("Please update the expiration date if you want to retain the table")
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("This DynamoDB table is about to expire.")

        except ValueError as e:
            errorMessage = "The content of the object that you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while deleting Dynamodb table for expiration date. {}".format(e)

        if errorMessage:
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = errorMessage

        self._AbstractAction__actionMessage = evaluationResult.annotation
        return evaluationResult
