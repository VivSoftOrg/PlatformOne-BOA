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
""" This module will evaluate resource on the basis of an expiration date. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_evaluate import AbstractEvaluator
from common.i18n import Translation as _
from common.date_validation_util import DateValidationUtil
from common.framework_objects import EvaluationResult
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants, ResourceConstants, ComplianceConstants, EvaluationMessages
from cloudfront_distribution_expiration.cloudfront_distribution_expiration_constants import Constants


class CloudFrontDistributionEvaluate(AbstractEvaluator):
    """ This class will evaluate resource on the basis of an expiration date. """

    def __getDistributionState(self, CFClient, eventItem):
        """ This method will get distribution state. """
        configResponse = getattr(CFClient, eventItem.configItems['GetConfigFunction'])(Id=eventItem.resourceId)

        if configResponse[eventItem.configItems['ConfigType']][Constants.DISTRIBUTION_ENABLED_STATE_REFERENCE]:
            configData = configResponse[eventItem.configItems['ConfigType']]
            configData.update({'Enabled': False})
            configArgument = {eventItem.configItems['ConfigType']: configData}

            eventItem.configItems.update(
                {
                    'configArgument': configArgument,
                    ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_ENABLED_STATE_REFERENCE),
                    'ETag': configResponse['ETag']
                }
            )
            return Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_ENABLED_STATE_REFERENCE)

        elif not eventItem.configItems['Status'] == Constants.DISTRIBUTION_DEPLOYED_STATUS_REFERENCE:
            eventItem.configItems.update({ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: Constants.DISTRIBUTION_NOT_DEPLOYED_EVALUATE})
            return Constants.DISTRIBUTION_NOT_DEPLOYED_EVALUATE

        else:
            eventItem.configItems.update(
                {
                    ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION: Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_DISABLED_STATE_REFERENCE),
                    'ETag': configResponse['ETag']
                }
            )
            return Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_DISABLED_STATE_REFERENCE)

    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        errorMessage = ""
        recommendationMessage = ""
        try:
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            CFClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_CLOUDFRONT,
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName
            )
            expirationDateLimit = int(self._AbstractEvaluator__eventParam.configParam[ResourceConstants.RESOURCE_EXPIRATION_DATE_LIMIT_RULE_PARAM])
            response = DateValidationUtil.updateEventActionBasedOnDate(eventItem, expirationDateLimit)

            if response == ResourceConstants.RESOURCE_HAS_VALIDITY:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _(EvaluationMessages.RESOURCE_COMPLIANT.format(Constants.RESOURCE_NAME))

            elif response == ResourceConstants.RESOURCE_EXPIRATION_DATE_LIMIT_EXCEEDED:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _(EvaluationMessages.RESOURCE_EXPIRATION_TAG_REPLACED.format(expirationDateLimit))
                LoggerUtility.logInfo(EvaluationMessages.RESOURCE_EXPIRATION_TAG_REPLACED.format(expirationDateLimit))
                recommendationMessage = "Update valid ExpirationDate tag on distribution."

            elif response == ResourceConstants.RESOURCE_ABOUT_TO_EXPIRE:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _(EvaluationMessages.RESOURCE_ABOUT_TO_EXPIRE.format(
                    Constants.RESOURCE_NAME, '',
                    eventItem.configItems[ResourceConstants.RESOURCE_REMAINING_VALIDITY]
                ))
                recommendationMessage = "Update valid ExpirationDate tag on distribution."

            elif response == ResourceConstants.RESOURCE_VALIDITY_EXPIRED:
                LoggerUtility.logInfo(EvaluationMessages.RESOURCE_EXPIRED.format(Constants.RESOURCE_NAME, eventItem.resourceId))
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                response = self.__getDistributionState(CFClient, eventItem)
                evaluationResult.annotation = _(response)
                recommendationMessage = "Update valid ExpirationDate tag on distribution."

            elif response == ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("The {} does not have ExpirationDate tag.".format(Constants.RESOURCE_NAME))
                LoggerUtility.logInfo(EvaluationMessages.RESOURCE_EXPIRATION_TAG_NOT_FOUND.format(Constants.RESOURCE_NAME, eventItem.resourceId))
                recommendationMessage = "Add valid ExpirationDate tag to distribution."

            elif response == ResourceConstants.RESOURCE_EXPIRATION_DATE_INVALID:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _(EvaluationMessages.RESOURCE_EXPIRATION_DATE_INVALID.format(Constants.RESOURCE_NAME, eventItem.resourceId))
                recommendationMessage = "Add valid ExpirationDate tag to distribution."

            if recommendationMessage:
                self._AbstractEvaluator__recommendationMessage = recommendationMessage

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
            errorMessage = "Error occurred while evaluating CloudFront service for an ExpirationDate tag. {}".format(e)

        if errorMessage:
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)
        else:
            LoggerUtility.logInfo(evaluationResult.annotation)

        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
