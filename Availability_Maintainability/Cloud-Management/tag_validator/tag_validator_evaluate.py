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
from os import environ

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from common.abstract_evaluate import AbstractEvaluator
from common.account_info import AccountInfo
from common.common_constants import ComplianceConstants, ManagedCloudConstants
from common.dynamo_db_utility import DynamoDbUtility
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from rules_common.aws_resource_utility.rules_constants import (MonitoredResourceConstants,
                                                               TagsConstants)
from tag_validator.tag_validator_constants import Constants
from utility.class_utility import ClassUtility
from utility.tag_utility import TagUtility


class TagValidatorEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """

    def __getUserNames(self):
        ''' Function to update the user names list based on either IAM users or the usernames provided as input '''
        userNames = self._AbstractEvaluator__eventParam.configParam.get(Constants.OWNER_TAG_KEY, None)
        if userNames is not None:
            if userNames == Constants.OWNER_AS_IAM_USERS:
                userNames = AccountInfo.getIamUsers(self._AbstractEvaluator__eventParam.accNo, self._AbstractEvaluator__eventParam.awsPartitionName)
            else:
                userNames = [item.strip() for item in userNames.split(',')]
        return userNames

    def __removeRetentionPeriodTag(self, eventItem):
        ''' Function to remove Retention Period Tag if it is present '''
        response = ClassUtility.getclassObject(
            "rules_common.aws_resource_utility",
            MonitoredResourceConstants.MONITERED_RESOURCES_DICT_REF[eventItem.resourceType],
            MonitoredResourceConstants.RESOURCE_UTILITY_REFERENCE,
            self._AbstractEvaluator__eventParam
        ).removeInstanceTag(eventItem.resourceId, eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE], Constants.RETENTION_PERIOD_TAG_KEY)
        if response:
            LoggerUtility.logInfo("Successfully removed the retentionPeriod tag")
        else:
            LoggerUtility.logInfo("Unable to remove the retentionPeriod tag")

    def __validateTags(self, eventItem):
        ''' Function to validate the tags based on the tag inputs recieved '''
        missingTags, invalidTags = [], []
        try:
            tagKeysToCheck = [item.strip() for item in self._AbstractEvaluator__eventParam.configParam['tagKeysToCheck'].split(',')]
            userNames = self.__getUserNames()

            if TagsConstants.TAGS_REFERENCE in eventItem.configItems:
                eventItem.configItems[TagsConstants.TAGS_REFERENCE] = TagUtility.fetchTagListAsDictionary(
                    eventItem.configItems[TagsConstants.TAGS_REFERENCE])
                for resourceTagKey, resourceTagValue in eventItem.configItems[TagsConstants.TAGS_REFERENCE].items():
                    if self._AbstractEvaluator__eventParam.configParam.get(resourceTagKey) and resourceTagKey in tagKeysToCheck:
                        if resourceTagKey == Constants.OWNER_TAG_KEY:
                            if resourceTagValue not in userNames:
                                invalidTags.append(resourceTagKey)
                        else:
                            validTagValues = [item.strip() for item in self._AbstractEvaluator__eventParam.configParam.get(resourceTagKey).split(',')]
                            if resourceTagValue not in validTagValues:
                                invalidTags.append(resourceTagKey)

                missingTags = set(tagKeysToCheck) - set(eventItem.configItems[TagsConstants.TAGS_REFERENCE])

            else:
                eventItem.configItems.update({TagsConstants.TAGS_REFERENCE: {}})
                missingTags = tagKeysToCheck
            return missingTags, invalidTags
        except Exception as e:
            LoggerUtility.logError("Error occurred: '{}' while validting tags for resource {}".format(e, eventItem.resourceId))
            return missingTags, invalidTags

    def evaluate(self, eventItem):
        ''' Function to evaluate tags of resources based on the inputs provided to the rule '''
        evaluationResult = EvaluationResult()
        errorMessage = ""
        recommendationMessage = "It is recommended to adhere the tagging standards set for your organization. Kindly refer internal policy documents to avoid resource termination."
        try:
            dynamoDBTagValidatorTable = environ[Constants.MONITORING_RESOURCES_DYNAMO_DB_TABLE]
            keyConditionAccountNo = Key('aws_account_no').eq(str(self._AbstractEvaluator__eventParam.accNo)) & Key('aws_resource_type').eq(eventItem.resourceType)
            monitoredResources = DynamoDbUtility.queryDynamodbData(dynamoDBTagValidatorTable, keyConditionAccountNo)

            applicableResources = [resource[MonitoredResourceConstants.RESOURCE_TYPE] for resource in monitoredResources]

            if eventItem.resourceType not in applicableResources:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The rule doesn't apply to resources of type {type} .").format(
                    type=eventItem.resourceType
                )
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            missingTags, invalidTags = self.__validateTags(eventItem)

            if missingTags or invalidTags:
                if missingTags:
                    LoggerUtility.logInfo("Resource '{}' does not have {} tags".format(eventItem.resourceId, missingTags))
                if invalidTags:
                    LoggerUtility.logInfo("Resource '{}' has {} invalid tags".format(eventItem.resourceId, invalidTags))

                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("Resource does not adhere to the tagging standards set for your organization.")
            else:
                LoggerUtility.logInfo("Resource '{}' adhere to the tagging standards set for your organization.".format(eventItem.resourceId))
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("Resource adhere to the tagging standards set for your organization.")
                if Constants.RETENTION_PERIOD_TAG_KEY in eventItem.configItems[TagsConstants.TAGS_REFERENCE].keys():
                    # Remove the retention period if present
                    self.__removeRetentionPeriodTag(eventItem)

            eventItem.configItems.update({
                Constants.MISSING_TAGS: ",".join(tag for tag in missingTags),
                Constants.INVALID_TAGS: ",".join(tag for tag in invalidTags)
            })

            self._AbstractEvaluator__recommendationMessage = _(recommendationMessage)
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

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
            errorMessage = "Error occured while evaluating resource. {}".format(e)
        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)

        return evaluationResult
