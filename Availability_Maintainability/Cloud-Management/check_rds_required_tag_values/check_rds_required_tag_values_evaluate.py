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
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants, TagsConstants, AWSResourceClassConstants, ComplianceConstants, ManagedCloudConstants
from common.rds_constants import RdsConstants
from common.common_utility import CommonUtility


class CheckRDSRequiredTagValuesEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """
    def __findValidTags(self, eventItem):
        """This method will find all valid tag values."""
        try:
            tagValues = {}
            for tag in eventItem.configItems[RdsConstants.RDS_TAG_NAME]:
                tagValues.update({tag[TagsConstants.EC2_REQUIRED_TAG_KEY]: tag[TagsConstants.EC2_REQUIRED_TAG_VALUE]})

            requiredTags = self._AbstractEvaluator__eventParam.configParam[TagsConstants.REQUIRED_TAG_REFERENCE]
            requiredTags = [item.strip() for item in requiredTags.split(',')]
            exposedTags = []
            validTags = ""
            missingTags = ""
            for key, value in tagValues.items():
                exposedTags.append(key)

            for reqTag in requiredTags:
                if reqTag not in exposedTags:
                    missingTags += reqTag + "," + "\n"
                else:
                    validTags += reqTag + "\n"

            return missingTags, validTags

        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            return False
        except Exception as e:
            LoggerUtility.logError("Error occured while finding valid tags. {}".format(e))
            return False

    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        errorMessage = ""
        try:
            if eventItem.resourceType not in [AWSResourceClassConstants.RDS_INSTANCE]:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The rule doesn't apply to resources of type {type} .").format(
                    type=eventItem.resourceType
                )
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult
            clusterIdentifier = None
            if eventItem.configItems.__contains__(RdsConstants.RDS_CLUSTER_IDENTIFIER):
                clusterIdentifier = eventItem.configItems[RdsConstants.RDS_CLUSTER_IDENTIFIER]
            if clusterIdentifier:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The RDS instance is part of DBCluster {}, therefor can't be validated.").format(clusterIdentifier)
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            if eventItem.configItems[RdsConstants.RDS_STATE_REFERENCE] == RdsConstants.RDS_TERMINATED_STATE_REFERENCE or \
                    eventItem.configItems[RdsConstants.RDS_STATE_REFERENCE] == RdsConstants.RDS_TERMINATING_STATE_REFERENCE:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The configurationItem was deleted and therefore cannot be validated.")
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            dbArn = eventItem.configItems[RdsConstants.RDS_ARN_KEY]
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            rdsClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_RDS,
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE])

            missingTags = ""
            validTags = ""
            try:
                tagValues = rdsClient.list_tags_for_resource(ResourceName=dbArn)
                tagResponse = CommonUtility.changeDictionaryKeysToLowerCase(tagValues)
                eventItem.configItems.update({RdsConstants.RDS_TAG_NAME: tagResponse['taglist']})
                missingTags, validTags = self.__findValidTags(eventItem)
            except ClientError as e:
                eventItem.configItems.update({RdsConstants.RDS_TAG_NAME: []})
                missingTags, validTags = self.__findValidTags(eventItem)
                LoggerUtility.logInfo("RDS instancs does not have tags!")

            if missingTags != "":
                LoggerUtility.logInfo("The instance is missing following required tags:\n" + missingTags)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("The instance does not have required tags.")
                eventItem.configItems.update({'missingTags': missingTags})
            else:
                LoggerUtility.logInfo("The instance has all required tags:\n" + validTags)
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("The instance has all the required tags:\n" + validTags)
                rdsClient.remove_tags_from_resource(ResourceName=dbArn,
                                                    TagKeys=[TagsConstants.REQUIRED_TAGS_EXPIRATION_DATE_TAG_KEY])

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
            errorMessage = "Error occured while evaluating user account. {}".format(e)

        if errorMessage:
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)

        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
