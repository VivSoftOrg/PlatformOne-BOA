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
                                     ComplianceConstants,
                                     ManagedCloudConstants)
from common.common_utility import CommonUtility
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from copy_ebs_tags_to_snapshots.copy_ebs_tags_to_snapshots_constants import \
    Constants


class CopyEbsTagsToSnapshotsEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """
    __applicableResources = [AWSResourceClassConstants.EBS_VOLUME]

    def __get_tags_hash(self, tag_set):
        """ This method will be used to convert the tag set from key value set to a hash set """
        tags = {}
        for tag in tag_set:
            tags[tag['key']] = tag['value']
        return tags

    def evaluate(self, eventItem):
        """ This method evaluates all the EBS Volumes """
        evaluationResult = EvaluationResult()
        accountNumber = self._AbstractEvaluator__eventParam.accNo
        errorMessage = ""
        try:
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            if eventItem.resourceType not in self.__applicableResources:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The rule doesn't apply to resources of type {type} .").format(
                    type=eventItem.resourceType
                )
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            if 'tags' not in eventItem.configItems:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The volume does not have a tag attached to it .")
                LoggerUtility.logInfo("The volume Id: {} does not have a tag attached to it .".format(eventItem.configItems['volumeid']))
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            tagsToCopy = self._AbstractEvaluator__eventParam.configParam[Constants.TAGS_TO_COPY]
            tagsToCopy = [item.strip() for item in tagsToCopy.split(',')]
            eventItem.configItems[Constants.COPY_TAGS] = []
            copyTags = False

            volumeId = eventItem.configItems['volumeid']
            snapshots = ec2Client.describe_snapshots(Filters=[{
                'Name': 'volume-id',
                'Values': [volumeId]
            }, {
                'Name': 'owner-id',
                'Values': [accountNumber]
            }])

            volumeTags = self.__get_tags_hash(eventItem.configItems['tags'])
            snapshots = CommonUtility.changeDictionaryKeysToLowerCase(snapshots)

            for snapshot in snapshots['snapshots']:
                if 'tags' in snapshot:
                    snapshotTags = self.__get_tags_hash(snapshot['tags'])
                else:
                    snapshotTags = {}
                tagToAddToVolume = []

                for tags in tagsToCopy:
                    if tags not in volumeTags:
                        LoggerUtility.logInfo("Not all the tags are present on the volume to copy.")
                        evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                        evaluationResult.annotation = _("Not all the tags are present on the volume to copy.")
                        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                        return evaluationResult

                    elif tags in snapshotTags:
                        LoggerUtility.logInfo("Tag: {} is present in snapshot: {}".format(tags, snapshot['snapshotid']))
                        continue
                    else:
                        tag_pair = {Constants.EC2_TAG_KEY: tags, Constants.EC2_TAG_VALUE: volumeTags[tags]}
                        if tag_pair not in tagToAddToVolume:
                            tagToAddToVolume.append(tag_pair)
                        else:
                            continue

                if tagToAddToVolume:
                    eventItem.configItems[Constants.COPY_TAGS].append({
                        Constants.ID: snapshot['snapshotid'],
                        Constants.TAGS_TO_COPY: tagToAddToVolume
                    })

                    copyTags = True

            if copyTags:
                evaluationResult.annotation = _("Standard Tags are missing on snapshots.")
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
            else:
                evaluationResult.annotation = _("All the Snapshots attached to the volumes have all the specified tags.")
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE

            recommendationMessage = "Please add the missing standard tags to the below snapshots to adhere the tagging standards set for your organization. Kindly refer internal policy documents."
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
            errorMessage = "Error occured while evaluating user account. {}".format(e)
        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)

        return evaluationResult
