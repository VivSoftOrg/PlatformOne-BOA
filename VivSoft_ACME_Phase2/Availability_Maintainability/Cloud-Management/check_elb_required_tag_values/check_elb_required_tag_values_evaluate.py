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
""" This script will mark Load Balancer as either compliant or non-compliant based on the tags present. """
from botocore.exceptions import ClientError

from check_elb_required_tag_values.evaluate_elb_expiration import EvaluateELBExpiration
from common.abstract_evaluate import AbstractEvaluator
from common.boto_utility import BotoUtility
from common.common_constants import (AWSResourceClassConstants, BotoConstants,
                                     ComplianceConstants, ResourceConstants,
                                     TagsConstants, ManagedCloudConstants)
from common.common_utility import CommonUtility
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility


class CheckELBRequiredTagValuesEvaluate(AbstractEvaluator):
    """ This class will be responsible for evaluating the resources. """

    def __getApplicationElbClient(self, eventItem):
        """ This method will be used to get the application or network type Load Balancer client """
        awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
        elbClient = BotoUtility.getClient(
            BotoConstants.BOTO_CLIENT_AWS_ELB_V2,
            self._AbstractEvaluator__eventParam.accNo,
            BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
            awsPartitionName,
            eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE])
        return elbClient

    def __getClassicElbClient(self, eventItem):
        """ This method will be used to get the classic type Load Balancer client """
        awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
        elbClient = BotoUtility.getClient(
            BotoConstants.BOTO_CLIENT_AWS_ELB,
            self._AbstractEvaluator__eventParam.accNo,
            BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
            awsPartitionName,
            eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE])
        return elbClient

    def __getClassicElbTags(self, eventItem):
        """ This method will be used to get the tags of classic load balancer """
        elbClient = self.__getClassicElbClient(eventItem)
        tagValues = CommonUtility.changeDictionaryKeysToLowerCase(
            elbClient.describe_tags(LoadBalancerNames=[eventItem.resourceId])[TagsConstants.TAG_DESCRIPTIONS][0])
        return tagValues

    def __getApplicationAndNetworkElbTags(self, eventItem):
        """ This method will be used to get the tags of application or network load balancer """  # noqa
        elbClient = self.__getApplicationElbClient(eventItem)
        tagValues = CommonUtility.changeDictionaryKeysToLowerCase(
            elbClient.describe_tags(ResourceArns=[eventItem.configItems[ResourceConstants.LOAD_BALANCER_ARN]])[TagsConstants.TAG_DESCRIPTIONS][0])
        return tagValues

    def __findMissingAndValidTags(self, eventItem):
        """ This method will be used to find the missing tags from elastic load balancer """
        tagValues = {}
        for tag in eventItem.configItems[TagsConstants.TAG_LIST]:
            tagValues.update({tag[TagsConstants.EC2_REQUIRED_TAG_KEY]: tag[TagsConstants.EC2_REQUIRED_TAG_VALUE]})

        requiredTags = self._AbstractEvaluator__eventParam.configParam[TagsConstants.REQUIRED_TAG_REFERENCE]
        requiredTags = [item.strip() for item in requiredTags.split(',')]
        exposedTags = []
        validTags = ""
        missingTags = ""
        for key, value in tagValues.items():
            exposedTags.append(key)

        for requiredTag in requiredTags:
            if requiredTag not in exposedTags:
                missingTags += requiredTag + "," + "\n"
            else:
                validTags += requiredTag + "\n"

        return missingTags, validTags

    def evaluate(self, eventItem):
        errorMessage = ''
        try:
            evaluationResult = EvaluationResult()
            eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME] = ResourceConstants.ELB_KEYWORD
            if eventItem.resourceType not in [AWSResourceClassConstants.ELB_RESOURCE, AWSResourceClassConstants.ELB_V2_RESOURCE]:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The rule doesn't apply to resources of type {type} .".format(
                    type=eventItem.resourceType
                ))
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            if eventItem.resourceType == AWSResourceClassConstants.ELB_RESOURCE:
                tagValues = self.__getClassicElbTags(eventItem)
            else:
                tagValues = self.__getApplicationAndNetworkElbTags(eventItem)

            eventItem.configItems.update({TagsConstants.TAG_LIST: tagValues[TagsConstants.TAG_LIST]})

            missingTags, validTags = self.__findMissingAndValidTags(eventItem)
            if missingTags != "":
                LoggerUtility.logInfo("The {} is missing following required tags:\n{}".format(ResourceConstants.ELB_KEYWORD, missingTags))
                expirationDateLimit = int(self._AbstractEvaluator__eventParam.configParam[ResourceConstants.RESOURCE_EXPIRATION_DATE_LIMIT_RULE_PARAM])
                response = EvaluateELBExpiration.getEvaluationResult(
                    evaluationResult, expirationDateLimit, eventItem, TagsConstants.EXPIRATION_DATE_TAG_KEY)
                evaluationResult = response[ResourceConstants.RESULT]
                eventItem.configItems.update({TagsConstants.MISSING_TAGS: missingTags})
            else:
                LoggerUtility.logInfo("The {} has all required tags:\n{}".format(ResourceConstants.ELB_KEYWORD, validTags))
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("The {} has all the required tags.".format(ResourceConstants.ELB_KEYWORD))

                if eventItem.resourceType == AWSResourceClassConstants.ELB_RESOURCE:
                    elbClient = self.__getClassicElbClient(eventItem)
                    elbClient.remove_tags(
                        LoadBalancerNames=[eventItem.resourceId], Tags=[{TagsConstants.TAG_KEY_REFERENCE: TagsConstants.REQUIRED_TAGS_EXPIRATION_DATE_TAG_KEY}])
                else:
                    elbClient = self.__getApplicationElbClient(eventItem)
                    elbClient.remove_tags(
                        ResourceArns=[eventItem.configItems[ResourceConstants.LOAD_BALANCER_ARN]],
                        TagKeys=[TagsConstants.REQUIRED_TAGS_EXPIRATION_DATE_TAG_KEY])

            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is Invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while evaluating user account. {}".format(e)

        if errorMessage:
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = errorMessage

        return evaluationResult
