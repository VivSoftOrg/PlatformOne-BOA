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
""" This module will create evaluation result on the basis of  iam access key's age """
from common.IAMConstants import IAMConstants
from common.abstract_evaluate import AbstractEvaluator
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.common_utility import CommonUtility
from common.common_constants import AWSResourceClassConstants, ComplianceConstants, CommonKeywords, TagsConstants


class IamKeysAgeEvaluate(AbstractEvaluator):
    """ This class will evaluate iam access key on the basis of age and status, and return evaluation result """

    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        errorMessage = ""
        try:
            if eventItem.resourceType not in [AWSResourceClassConstants.IAM_RESOURCE]:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The rule doesn't apply to resources of type {type} .").format(
                    type=eventItem.resourceType
                )
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            iamKeyValidity = int(self._AbstractEvaluator__eventParam.configParam[IAMConstants.IAM_KEY_VALIDITY])
            eventItem.configItems[IAMConstants.IAM_KEY_VALIDITY] = iamKeyValidity
            notifyDaysBeforeExpire = int(self._AbstractEvaluator__eventParam.configParam[IAMConstants.IAM_KEY_NOTIFY_BEFORE_VALID_DAYS])
            notifyDaysAfterExpire = int(self._AbstractEvaluator__eventParam.configParam[IAMConstants.IAM_KEY_NOTIFY_AFTER_VALID_DAYS])
            createDate = eventItem.configItems[CommonKeywords.CREATE_DATE]
            resourceAge = CommonUtility.resourceAgeFromNow(createDate)
            resourceAgeInDays = resourceAge.days
            eventItem.configItems.update({TagsConstants.TAG_LIST: [{TagsConstants.EC2_REQUIRED_TAG_KEY: 'Owner', TagsConstants.EC2_REQUIRED_TAG_VALUE: eventItem.configItems['username']}]})

            if resourceAgeInDays > iamKeyValidity:
                if eventItem.configItems['Status'] == 'Active':
                    evaluationResult.annotation = "Active IAM access key is older than {} days.".format(iamKeyValidity)
                    self._AbstractEvaluator__recommendationMessage = "Please rotate your IAM access keys in every {} days,\
                    to prevent them from getting deactivated in future".format(iamKeyValidity)
                    eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] = CommonKeywords.DISABLE
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    eventItem.configItems[IAMConstants.IAM_KEY_AGE_IN_DAYS] = resourceAgeInDays
                    deletionDays = (iamKeyValidity + notifyDaysAfterExpire) - resourceAgeInDays
                    eventItem.configItems[IAMConstants.IAM_KEY_DELETION_DAYS] = deletionDays if deletionDays > 0 else 0
                    LoggerUtility.logInfo("IAM access key is older than {} days.".format(iamKeyValidity))
                else:
                    if resourceAgeInDays > (iamKeyValidity + notifyDaysAfterExpire):
                        evaluationResult.annotation = "Deactivated IAM access key has reached the maximum age limit ({} days).\
                        ".format(iamKeyValidity + notifyDaysAfterExpire)
                        eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] = CommonKeywords.DELETE
                        evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                        eventItem.configItems[IAMConstants.IAM_KEY_AGE_IN_DAYS] = resourceAgeInDays
                        self._AbstractEvaluator__recommendationMessage = "Please rotate your IAM access keys in every {} days,\
                        to prevent them from getting deleted in future".format(iamKeyValidity)
                        LoggerUtility.logInfo(evaluationResult.annotation)
                    else:
                        evaluationResult.annotation = "Deactivated IAM access key is older than {} days".format(iamKeyValidity)
                        self._AbstractEvaluator__recommendationMessage = "Please rotate your IAM access keys to prevent them from getting deleted"
                        evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                        eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] = CommonKeywords.DELETE_NOTIFICATION
                        eventItem.configItems[IAMConstants.IAM_KEY_AGE_IN_DAYS] = resourceAgeInDays
                        deletionDays = (iamKeyValidity + notifyDaysAfterExpire) - resourceAgeInDays
                        eventItem.configItems[IAMConstants.IAM_KEY_DELETION_DAYS] = deletionDays if deletionDays > 0 else 0
            elif resourceAgeInDays > (iamKeyValidity - notifyDaysBeforeExpire):
                evaluationResult.annotation = "IAM access key is about to expire."
                self._AbstractEvaluator__recommendationMessage = "Please rotate your IAM access keys to prevent them from getting disabled"
                eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] = CommonKeywords.DISABLE_NOTIFICATION
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                eventItem.configItems[IAMConstants.IAM_KEY_AGE_IN_DAYS] = resourceAgeInDays
                expirationDays = iamKeyValidity - resourceAgeInDays
                eventItem.configItems[IAMConstants.IAM_KEY_EXPIRY_DAYS] = expirationDays if expirationDays > 0 else 0
                LoggerUtility.logInfo("IAM access key is older than {} days.".format(iamKeyValidity - notifyDaysBeforeExpire))
            else:
                eventItem.configItems[IAMConstants.IAM_KEY_AGE_IN_DAYS] = resourceAgeInDays
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("Access key age is less than {} days".format(iamKeyValidity))
                LoggerUtility.logInfo("Access key age is less than %s" % iamKeyValidity)

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type doesn't possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except Exception as e:
            errorMessage = "Error occurred while evaluating IAM key age. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = errorMessage

        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
