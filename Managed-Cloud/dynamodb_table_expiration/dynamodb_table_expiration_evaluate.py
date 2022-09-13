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
from datetime import date
from common.framework_objects import EvaluationResult
from common.abstract_evaluate import AbstractEvaluator
from common.common_constants import ComplianceConstants
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from dynamodb_table_expiration.dynamodb_table_expiration_constants import Constants


class DynamoDBTableEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """
    __daysRemainingBeforeExpiration = 10

    def __getExpirationDate(self, eventItem):
        """method returns Expiration date"""
        tags = {}
        try:
            for tag in eventItem.configItems['tags']:
                tags.update({tag[Constants.DYNAMO_DB_TAG_KEY]: tag[Constants.DYNAMO_DB_TAG_VALUE]})

            if Constants.DYNAMO_DB_EXPIRATION_TAG_REFERENCE in tags and bool(tags[Constants.DYNAMO_DB_EXPIRATION_TAG_REFERENCE]):
                return tags[Constants.DYNAMO_DB_EXPIRATION_TAG_REFERENCE]
            else:
                return False
        except Exception as e:
            LoggerUtility.logError("Error occured while fetching ExpirationDate. {}".format(e))
            return False

    def __getValidity(self, dateString):
        """method returns validity for the date."""
        try:
            splitDateString = dateString.split('-')
            year = int(splitDateString[0])
            month = int(splitDateString[1])
            day = int(splitDateString[2])
            return (date(year, month, day) - date.today()).days
        except Exception as e:
            LoggerUtility.logError("Error occured while getting date validity. {}".format(e))
            return False

    def __validateExpirationDate(self, eventItem):
        """Method will validate the Expiration Date."""
        try:
            resourceExpirationDate = self.__getExpirationDate(eventItem)

            if bool(resourceExpirationDate):
                validity = self.__getValidity(resourceExpirationDate)

                if validity:
                    self.__daysRemainingBeforeExpiration = validity
                else:
                    eventItem.configItems.update({'action': Constants.DYNAMO_DB_TABLE_EXPIRATION_DATE_INVALID})
                    return Constants.DYNAMO_DB_TABLE_EXPIRATION_DATE_INVALID

                if self.__daysRemainingBeforeExpiration > 0:

                    expirationDateLimit = int(
                        self._AbstractEvaluator__eventParam.configParam[Constants.DYNAMO_DB_EXPIRATION_DATE_LIMIT_RULE_PARAM]
                    )
                    if self.__daysRemainingBeforeExpiration <= 3:
                        eventItem.configItems.update({'action': Constants.DYNAMO_DB_TABLE_ABOUT_TO_EXPIRE})
                        return Constants.DYNAMO_DB_TABLE_ABOUT_TO_EXPIRE

                    elif self.__daysRemainingBeforeExpiration > expirationDateLimit:
                        eventItem.configItems.update({'action': Constants.DYNAMO_DB_TABLE_EXPIRATION_DATE_LIMIT_EXCEEDED})
                        return Constants.DYNAMO_DB_TABLE_EXPIRATION_DATE_LIMIT_EXCEEDED
                    else:
                        return Constants.DYNAMO_DB_TABLE_HAS_VALIDITY

                else:
                    eventItem.configItems.update({'action': Constants.DYNAMO_DB_TABLE_VALIDITY_EXPIRED})
                    return Constants.DYNAMO_DB_TABLE_VALIDITY_EXPIRED

            else:
                eventItem.configItems.update({'action': Constants.DYNAMO_DB_TABLE_EXPIRATION_DATE_NOT_FOUND})
                return Constants.DYNAMO_DB_TABLE_EXPIRATION_DATE_NOT_FOUND
        except Exception as e:
            LoggerUtility.logError("Error occured while {}".format(e))
            return False

    def evaluate(self, eventItem):
        errorMessage = ""
        recommendationMessage = ""
        evaluationResult = EvaluationResult()
        try:
            response = self.__validateExpirationDate(eventItem)

            if response == Constants.DYNAMO_DB_TABLE_HAS_VALIDITY:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("This DynamoDB table is compliant.")

            elif response == Constants.DYNAMO_DB_TABLE_EXPIRATION_DATE_LIMIT_EXCEEDED:
                LoggerUtility.logInfo('The DynamoDB table ExpirationDate tag limit exceeded')
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("Replacing the ExpirationDate tag.")
                recommendationMessage = "It is recommended to update your DynamoDB table with a valid ExpirationDate tag to avoid deletion of the table."

            elif response == Constants.DYNAMO_DB_TABLE_ABOUT_TO_EXPIRE:
                LoggerUtility.logInfo('The DynamoDB table `{}` will expire after {} days.'.format(eventItem.resourceId, self.__daysRemainingBeforeExpiration))
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("The DynamoDB table will expire.")
                recommendationMessage = "It is recommended to update your DynamoDB table with a valid ExpirationDate tag to avoid deletion of the table."

            elif response == Constants.DYNAMO_DB_TABLE_VALIDITY_EXPIRED:
                LoggerUtility.logInfo('The DynamoDB table `{}` has expired.'.format(eventItem.resourceId))
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _('The DynamoDB table has expired.')
                recommendationMessage = "It is recommended to update your DynamoDB table with a valid ExpirationDate tag to avoid deletion of the table."

            elif response == Constants.DYNAMO_DB_TABLE_EXPIRATION_DATE_NOT_FOUND:
                LoggerUtility.logInfo('The DynamoDB table `{}` does not have `ExpirationDate` tag.'.format(eventItem.resourceId))
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _('The DynamoDB table does not have ExpirationDate tag.')
                recommendationMessage = "It is recommended to update your DynamoDB table with a valid ExpirationDate tag to avoid deletion of the table."

            elif response == Constants.DYNAMO_DB_TABLE_EXPIRATION_DATE_INVALID:
                LoggerUtility.logInfo('The DynamoDB table `{}` has invalid expiration date.'.format(eventItem.resourceId))
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _('The DynamoDB table has invalid expiration date.')
                recommendationMessage = "It is recommended to update your DynamoDB table with a valid ExpirationDate tag to avoid deletion of the table."
            else:
                errorMessage = "Failed while evaluting dynamodb table for expiration date."

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while evaluating for dynamodb table expiration config rule. {}".format(e)

        if errorMessage:
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)

        if recommendationMessage:
            self._AbstractEvaluator__recommendationMessage = _(recommendationMessage)

        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
