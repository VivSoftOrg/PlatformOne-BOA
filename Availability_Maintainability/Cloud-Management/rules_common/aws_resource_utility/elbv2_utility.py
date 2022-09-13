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
""" This module will fetch the ELBv2 resource details  """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.common_constants import BotoConstants, ManagedCloudConstants, ComplianceConstants
from common.common_utility import CommonUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.logger_utility import LoggerUtility
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common_constants.exception_constants import ExceptionMessages
from rules_common.aws_resource_utility.rules_constants import RulesConstants


class Elbv2Utility():
    """ This class is created for Fetching the target group resource details. """

    @staticmethod
    def parseAndFetchTargetGroupDetails(targetGroup):
        """Method will fetch target group details and assign it to configItems."""
        resourceId = targetGroup['targetgrouparn']
        configItems = targetGroup
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, configItems=configItems)

    @staticmethod
    def fetchTargetGroups(eventParam):
        """ This method fetches all the target group details """
        targetGroupList = []
        errorMessage = ""
        awsPartitionName = eventParam.awsPartitionName
        regions = BotoUtility.getRegions(eventParam.accNo, awsPartitionName)
        try:
            for region in regions:
                elbV2Client = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_ELB_V2,
                    eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )
                LoggerUtility.logInfo('Fetching target groups in region: {}'.format(region))
                paginator = elbV2Client.get_paginator('describe_target_groups')
                for paginatorResponse in paginator.paginate():
                    response = CommonUtility.changeDictionaryKeysToLowerCase(paginatorResponse)
                    targetGroups = response[RulesConstants.TARGET_GROUPS]
                    for targetGroup in targetGroups:
                        targetGroup.update({ManagedCloudConstants.REGION_REFERENCE: region})
                        eventItems = Elbv2Utility.parseAndFetchTargetGroupDetails(targetGroup)
                        targetGroupList.append(eventItems)

        except ValueError as e:
            errorMessage = ExceptionMessages.VALUE_ERROR.format(e)
        except AttributeError as e:
            errorMessage = ExceptionMessages.ATTRIBUTE_ERROR.format(e)
        except TypeError as e:
            errorMessage = ExceptionMessages.TYPE_ERROR.format(e)
        except NameError as e:
            errorMessage = ExceptionMessages.NAME_ERROR.format(e)
        except ClientError as e:
            errorMessage = ExceptionMessages.CLIENT_ERROR.format(e)
        except Exception as e:
            errorMessage = "Error occured while fetching target groups {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)

        return targetGroupList

    @staticmethod
    def deleteTargetGroup(eventParam, eventItem):
        """ This method will delete non compliant target group and returns evaluation result """
        evaluationResult = EvaluationResult()
        errorMessage = ""
        try:
            awsPartitionName = eventParam.awsPartitionName
            elbv2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_ELB_V2,
                eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            response = elbv2Client.delete_target_group(TargetGroupArn=eventItem.resourceId)
            requestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]
            if requestStatus == 200:
                LoggerUtility.logInfo("Successfully deleted target group {}".format(eventItem.resourceId))
                evaluationResult.annotation = _("Successfully deleted target group")
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
            else:
                LoggerUtility.logError(_("Unable to deleted target group {}".format(eventItem.resourceId)))
                evaluationResult.annotation = _("Unable to deleted target group")
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE

        except ValueError as e:
            errorMessage = ExceptionMessages.VALUE_ERROR.format(e)
        except AttributeError as e:
            errorMessage = ExceptionMessages.ATTRIBUTE_ERROR.format(e)
        except TypeError as e:
            errorMessage = ExceptionMessages.TYPE_ERROR.format(e)
        except NameError as e:
            errorMessage = ExceptionMessages.NAME_ERROR.format(e)
        except ClientError as e:
            errorMessage = ExceptionMessages.CLIENT_ERROR.format(e)
        except Exception as e:
            errorMessage = "Error occured while deleting target group. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.annotation = _(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION

        return evaluationResult
