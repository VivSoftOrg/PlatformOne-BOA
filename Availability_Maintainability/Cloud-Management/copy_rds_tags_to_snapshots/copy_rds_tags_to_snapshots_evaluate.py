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

from common.abstract_evaluate import AbstractEvaluator
from common.boto_utility import BotoUtility
from common.common_constants import (AWSResourceClassConstants, BotoConstants,
                                     ComplianceConstants, ManagedCloudConstants)
from common.common_utility import CommonUtility
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from rules_common.RuleConstants import RuleConstants


class CopyRdsTagsToSnapshotsEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """
    __applicableResources = [AWSResourceClassConstants.RDS_INSTANCE]

    def __get_tags_hash(self, tag_set):
        """ This method will be used to convert the tag set from key value set to a hash set """
        tags = {}
        for tag in tag_set:
            tags[tag[RuleConstants.RDS_TAG_KEY]] = tag[RuleConstants.RDS_TAG_VALUE]
        return tags

    def evaluate(self, eventItem):
        """ This method evaluates the RDS Instance """
        evaluationResult = EvaluationResult()
        errorMessage = ""
        try:
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            rdsClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_RDS,
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            if eventItem.resourceType not in self.__applicableResources:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _(
                    "The rule doesn't apply to resources of type {type} ."
                ).format(type=eventItem.resourceType)
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            if RuleConstants.EVENTITEM_TAGS_KEY not in eventItem.configItems:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _(
                    "The RDS instance: {} does not have a tag attached to it ."
                ).format(
                    eventItem.configItems[RuleConstants.RDS_INSTANCE_ID]
                )
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            copyTags = False
            updTags = False
            eventItem.configItems[RuleConstants.COPY_TAGS] = []
            eventItem.configItems[RuleConstants.UPDATE_TAGS] = []
            if eventItem.configItems[RuleConstants.EVENTITEM_TAGS_KEY]:
                dbInstanceTags = self.__get_tags_hash(
                    eventItem.configItems[RuleConstants.EVENTITEM_TAGS_KEY][0]
                )
            else:
                dbInstanceTags = {}

            dbSnapshots = rdsClient.describe_db_snapshots(
                DBInstanceIdentifier=eventItem.resourceId
            )[RuleConstants.RDS_SNAPSHOTS]
            dbSnapshots = CommonUtility.changeDictionaryKeysToLowerCase(dbSnapshots)

            if dbSnapshots:
                for dbSnapshot in dbSnapshots:
                    dbSnapshotTags = rdsClient.list_tags_for_resource(
                        ResourceName=dbSnapshot[RuleConstants.RDS_SNAPSHOT_ARN]
                    )[RuleConstants.RDS_TAG_LIST]
                    dbSnapshotTags = self.__get_tags_hash(dbSnapshotTags)

                    tagsToAddToSnapshot = []
                    tagsToUpdateOnSnapshot = []

                    for instTag in dbInstanceTags:
                        if instTag in dbSnapshotTags:
                            LoggerUtility.logInfo("Tag: {} is present in snapshot: {}".format(
                                instTag, dbSnapshot[RuleConstants.RDS_SNAPSHOT_ID]))
                            if dbInstanceTags[instTag] != dbSnapshotTags[instTag]:
                                tag_pair = {
                                    RuleConstants.RDS_TAG_KEY: instTag,
                                    RuleConstants.RDS_TAG_VALUE: dbInstanceTags[instTag]
                                }
                                if tag_pair not in tagsToUpdateOnSnapshot:
                                    tagsToUpdateOnSnapshot.append(tag_pair)
                        else:
                            tag_pair = {
                                RuleConstants.RDS_TAG_KEY: instTag,
                                RuleConstants.RDS_TAG_VALUE: dbInstanceTags[instTag]
                            }
                            if tag_pair not in tagsToAddToSnapshot:
                                tagsToAddToSnapshot.append(tag_pair)

                    if tagsToAddToSnapshot:
                        eventItem.configItems[RuleConstants.COPY_TAGS].append({
                            RuleConstants.ID: dbSnapshot[RuleConstants.RDS_SNAPSHOT_ARN],
                            RuleConstants.TAGS_TO_COPY: tagsToAddToSnapshot
                        })
                        copyTags = True
                    if tagsToUpdateOnSnapshot:
                        eventItem.configItems[RuleConstants.UPDATE_TAGS].append({
                            RuleConstants.ID: dbSnapshot[RuleConstants.RDS_SNAPSHOT_ARN],
                            RuleConstants.TAGS_TO_COPY: tagsToUpdateOnSnapshot
                        })
                        updTags = True

                if copyTags:
                    evaluationResult.annotation = _("At least one of the snapshots attached to the RDS instance does not have all the tags specified on the instance.")
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                if updTags:
                    evaluationResult.annotation = _("At least one of the snapshots attached to the RDS instance has a tag with a value different than specified on the instance.")
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                if not copyTags and not updTags:
                    evaluationResult.annotation = _("All of the snapshots attached to the RDS instance have all the tags specified on the instance.")
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE

                LoggerUtility.logInfo("Evaluation result is:  {}".format(evaluationResult))
            else:
                evaluationResult.annotation = _("The instance {} does not have any snapshots.".format(eventItem.resourceId))
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

            LoggerUtility.logInfo("Final Evaluation Result is:  {}".format(evaluationResult))

            LoggerUtility.logInfo(evaluationResult.annotation)
            recommendationMessage = "It is recommended to adhere the tagging standards set for your organization. Kindly refer internal policy documents."
            self._AbstractEvaluator__recommendationMessage = _(recommendationMessage)
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

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
            errorMessage = "Error occured while Evaluating user account. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)

        return evaluationResult
