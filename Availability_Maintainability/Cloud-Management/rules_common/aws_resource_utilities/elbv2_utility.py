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
""" This module will fetch the ALB resource details and send it to Evaluator.  """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.common_constants import (AWSResourceClassConstants, BotoConstants, ComplianceConstants, TagsConstants,
                                     ManagedCloudConstants, ResourceConstants)
from common.common_utility import CommonUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.logger_utility import LoggerUtility
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from rules_common.aws_resource_utilities.rules_constants import RulesTagsConstants
from copy_alb_nlb_tags_to_target_groups.copy_alb_nlb_tags_to_target_groups_constants import ALBConstants


class Elbv2Utility():
    """ This class is created for Fetching the alb resource details. """

    @staticmethod
    def parseAndFetchALBDetails(albObject):
        """Method will fetch ALB/NLB details and assign it to configItems."""
        resourceId = albObject[ResourceConstants.LOAD_BALANCER_ARN]
        configItems = albObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.ELB_V2_RESOURCE, configItems=configItems)

    @staticmethod
    def describeLoadBalancers(eventParam):
        """ This method elb v2 loadbalancers i.e. ALB's and NLB's """
        albsList = []
        errorMessage = ''
        awsPartitionName = eventParam.awsPartitionName
        regions = BotoUtility.getRegions(eventParam.accNo, awsPartitionName)
        try:
            for region in regions:
                albClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_ELB_V2,
                    eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )
                LoggerUtility.logInfo('Fetching ALB\'s in region: {}'.format(region))
                paginator = albClient.get_paginator('describe_load_balancers')
                for paginatorResponse in paginator.paginate():
                    response = CommonUtility.changeDictionaryKeysToLowerCase(paginatorResponse)
                    albs = response[ResourceConstants.LOAD_BALANCERS]
                    for alb in albs:
                        alb.update({ManagedCloudConstants.REGION_REFERENCE: region})
                        eventItems = Elbv2Utility.parseAndFetchALBDetails(alb)
                        albsList.append(eventItems)

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
            errorMessage = "Error occured while {}".format(e)

        if errorMessage != '':
            LoggerUtility.logError(errorMessage)

        return albsList

    @staticmethod
    def addTagsToResource(eventParam, eventItem, resourceListWithTags):
        """
            This method will add tags to ALBs, NLBs or target groups.
            'resourceListWithTags' will contains list of dictionary with keys ResourceArn & tagsToAdd
            e.g.
                resourceListWithTags = [
                    {"ResourceArn":"resourceArn1", tagsToAdd = [{'key': 'Project', 'value': 'MNC'}, {'key': 'Owner', 'value': 'vaibhav.menkudale'},
                    {"ResourceArn":"resourceArn1", tagsToAdd = [{'key': 'Name', 'value': 'Name1'}, {'key': 'Environment', 'value': 'testing'}
                    ]
        """
        errorMessage = ""
        evaluationResult = EvaluationResult()
        try:
            awsPartitionName = eventParam.awsPartitionName
            albClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_ELB_V2,
                eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            for resource in resourceListWithTags:
                tagsToAdd = [dict((key.capitalize(), value) for key, value in tag.items()) for tag in resource[RulesTagsConstants.TAGS_TO_ADD]]
                response = albClient.add_tags(ResourceArns=[resource[ALBConstants.RESOURCE_ARN]], Tags=tagsToAdd)

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
            errorMessage = "Error occured while adding tags. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)
        else:
            message = "Tags added successfully."
            LoggerUtility.logInfo(message)
            evaluationResult.annotation = _(message)
            evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE

        return evaluationResult

    @staticmethod
    def describeTargetGroupsForElb(elbV2Client, elbV2Arn):
        """ This method will be used to describe target groups for ALB's/NLB's, NLB's with albArn """
        try:
            targetGroups = []
            targetGroupsResponse = elbV2Client.describe_target_groups(LoadBalancerArn=elbV2Arn)
            if targetGroupsResponse[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                targetGroups = targetGroupsResponse[ALBConstants.TARGET_GROUPS]
            else:
                LoggerUtility.logError('Unable to describe target groups for ALB or NLB with arn {}'.format(elbV2Arn))
        except Exception as e:
            LoggerUtility.logError('Error {} occoured while describing target groups for ALB or NLB with arn {}'.format(e, elbV2Arn))

        return targetGroups

    @staticmethod
    def describeTags(elbV2Client, resourceArnList):
        """This method will return list of tags for ALB, NLB or target group  """
        try:
            tags = []

            describeTagsResponse = elbV2Client.describe_tags(ResourceArns=resourceArnList)

            if describeTagsResponse[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                tags = describeTagsResponse[TagsConstants.TAG_DESCRIPTIONS]
            else:
                LoggerUtility.logError('Unable to describe target groups for resource arns {}'.format(resourceArnList))
        except Exception as e:
            LoggerUtility.logError('Error {} occoured while describing target groups for resource arns {}'.format(e, resourceArnList))

        return tags
