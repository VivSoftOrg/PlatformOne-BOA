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
"""
    This module will Evaluates target groups associated with alb's on the basis of tags.
    Method will first that Key and Value are same on target group as per ALB/NLB, if not it will
    check in excludeTags (list). If above both conditions are false it will add to missing tags list
"""
from botocore.exceptions import ClientError

from common.abstract_evaluate import AbstractEvaluator
from common.boto_utility import BotoUtility
from common.common_constants import (BotoConstants, ResourceConstants,
                                     ComplianceConstants, ManagedCloudConstants)
from common.common_utility import CommonUtility
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from rules_common.aws_resource_utilities.elbv2_utility import Elbv2Utility
from rules_common.aws_resource_utilities.rules_constants import RulesTagsConstants, ELBv2Constants
from copy_alb_nlb_tags_to_target_groups.copy_alb_nlb_tags_to_target_groups_constants import ALBConstants
from utility.tag_utility import TagUtility


class CopyAlbNlbTagsToTargetGroupsEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will target groups associated with alb's on the basis of tags. """

    def evaluate(self, eventItem):
        """ This method evaluates all the ALB's  & NLB's"""
        evaluationResult = EvaluationResult()
        errorMessage = ""
        albTags = []
        targetGroups = ""
        allMissingTagsList = []
        missingTagsTargetGroups = []
        try:
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            albClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_ELB_V2,
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            excludeTags = self._AbstractEvaluator__eventParam.configParam[ALBConstants.EXCLUDE_TAGS]
            excludeTags = [item.strip() for item in excludeTags.split(',')]

            albArn = eventItem.configItems[ResourceConstants.LOAD_BALANCER_ARN]
            if ALBConstants.SUPPLEMENTARY_CONFIGURATION in eventItem.configItems:
                if ALBConstants.TAGS_LOWER_CASE in eventItem.configItems[ALBConstants.SUPPLEMENTARY_CONFIGURATION]:
                    albTags = eventItem.configItems[ALBConstants.SUPPLEMENTARY_CONFIGURATION][ALBConstants.TAGS_LOWER_CASE]
            else:
                albTags = CommonUtility.changeDictionaryKeysToLowerCase(Elbv2Utility.describeTags(elbV2Client=albClient, resourceArnList=[albArn])[0][ALBConstants.TAGS_PASCAL_CASE])
            targetGroups = Elbv2Utility.describeTargetGroupsForElb(elbV2Client=albClient, elbV2Arn=albArn)
            targetGroupsArn = [targetGroup[ALBConstants.TARGET_GROUP_ARN] for targetGroup in targetGroups]
            targetGroupsTags = Elbv2Utility.describeTags(elbV2Client=albClient, resourceArnList=targetGroupsArn)

            for targetGroupTag in targetGroupsTags:
                if targetGroupTag[ALBConstants.TAGS_PASCAL_CASE]:
                    targetGroupTag[ALBConstants.TAGS_PASCAL_CASE] = CommonUtility.changeDictionaryKeysToLowerCase(targetGroupTag[ALBConstants.TAGS_PASCAL_CASE])

                missingTags = TagUtility.getMissingTagListWithValues(sourceTagList=albTags, destinationTagList=targetGroupTag[ALBConstants.TAGS_PASCAL_CASE], excludeTagKeys=excludeTags, checkValues=True)
                targetGroupTag.update({RulesTagsConstants.TAGS_TO_ADD: missingTags})

                if missingTags:
                    missingTagsTargetGroups.append(targetGroupTag)

            if missingTagsTargetGroups:
                evaluationResult.annotation = _("All target groups does not have all same tags as per respective ALB or NLB.")
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                targetGroupsNameList = []
                eventItem.configItems.update({ALBConstants.MISSING_TAGS_TARGET_GROUPS: missingTagsTargetGroups})
                for missingTagTargetGroup in missingTagsTargetGroups:
                    targetGroupsNameList.append(missingTagTargetGroup['ResourceArn'].split('/')[-2])
                    for tags in missingTagTargetGroup['tagsToAdd']:
                        allMissingTagsList.append(tags['key'])

                eventItem.configItems.update({ELBv2Constants.TARGET_GROUPS: str(targetGroupsNameList).strip('[]').replace("'", "")})
                eventItem.configItems.update({RulesTagsConstants.MISSING_TAGS: str(set(allMissingTagsList)).strip('{}').replace("'", "")})
            else:
                evaluationResult.annotation = _("All target groups have all same tags as respective ALB or NLB.")
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE

            recommendationMessage = "It is recommended all target groups to have same tags as ALB's or NLB's "
            self._AbstractEvaluator__recommendationMessage = _(recommendationMessage)
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is Invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type doesn't possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of the incorrect type. {}".format(e)
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
