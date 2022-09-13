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
from common.common_constants import AWSResourceClassConstants, BotoConstants, ComplianceConstants, ManagedCloudConstants
from copy_ec2_tags_to_ebs.copy_ec2_tags_to_ebs_constants import Constants


class CopyEc2TagsToEbsEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """
    __applicableResources = [AWSResourceClassConstants.EC2_INSTANCE]

    def __get_tags_hash(self, tag_set):
        """ This method will be used to convert the tag set from key value set to a hash set """
        tags = {}
        for tag in tag_set:
            tags[tag['Key']] = tag['Value']
        return tags

    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        errorMessage = ""
        try:
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            ec2Resource = BotoUtility.getResource(
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

            tagsToCopy = self._AbstractEvaluator__eventParam.configParam[Constants.EC2_TAGS_TO_COPY]
            tagsToCopy = [item.strip() for item in tagsToCopy.split(',')]
            copyTags = False
            eventItem.configItems['VolumesTags'] = []

            instance = ec2Resource.Instance(eventItem.resourceId)
            if instance.tags:
                instance_tags = self.__get_tags_hash(instance.tags)

                for volume in instance.volumes.all():
                    tagToAddToVolume = []

                    if volume.tags:
                        volume_tags = self.__get_tags_hash(volume.tags)
                    else:
                        volume_tags = {}

                    for tag in tagsToCopy:
                        if tag in instance_tags:
                            if not instance_tags[tag]:
                                LoggerUtility.logInfo("The '{}' tag is insufficent, cannot copy tag for: {} in {}".format(tag,
                                                                                                                          instance.id,
                                                                                                                          eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]))
                            elif tag in volume_tags:
                                continue
                            else:
                                tag_pair = {Constants.EC2_TAG_KEY: tag, Constants.EC2_TAG_VALUE: instance_tags[tag]}
                                if tag_pair not in tagToAddToVolume:
                                    tagToAddToVolume.append(tag_pair)
                                else:
                                    continue
                        else:
                            LoggerUtility.logInfo("There is no '{}' tag defined for instance with ID {}".format(tag, instance.id))

                    if tagToAddToVolume:
                        eventItem.configItems['VolumesTags'].append({
                            Constants.EC2_VOLUME_ID: volume.id,
                            Constants.EC2_TAGS_TO_COPY: tagToAddToVolume
                        })
                        copyTags = True

                if copyTags:
                    evaluationResult.annotation = _("One of the Volume attached to the Instance does not have all the specified tags.")
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                else:
                    evaluationResult.annotation = _("All the Volumes attached to the Instance have all the specified tags.")
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE

            else:
                evaluationResult.annotation = _("The Instance {} does not have any tags.".format(instance.id))
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

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
            errorMessage = "Error occured while evaluating user account. {}".format(e)
        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)

        return evaluationResult
