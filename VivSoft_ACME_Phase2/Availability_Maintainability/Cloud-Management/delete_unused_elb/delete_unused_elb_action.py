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
"""This module will perform action based on the Evaluation Result."""
from botocore.exceptions import ClientError

from common.abstract_action import AbstractAction
from common.boto_utility import BotoUtility
from common.common_constants import (AWSResourceClassConstants, BotoConstants,
                                     ComplianceConstants,
                                     ManagedCloudConstants, ResourceConstants)
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from delete_unused_elb.delete_unused_elb_constants import Constants
from common_constants.exception_constants import ExceptionMessages


class UnusedELBAction(AbstractAction):
    """This class deletes Load Balancers if they are not sending traffic to any instances or target groups """

    def performAction(self, eventItem):
        evaluationResult = EvaluationResult()
        errorMessage = ""
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName

            if eventItem.resourceType == AWSResourceClassConstants.ELB_RESOURCE:
                elbClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_ELB,
                    self._AbstractAction__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                    awsPartitionName,
                    eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
                )
                loadBalancerName = eventItem.resourceId
                response = elbClient.delete_load_balancer(LoadBalancerName=loadBalancerName)

            else:
                elbClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_ELB_V2,
                    self._AbstractAction__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                    awsPartitionName,
                    eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
                )
                loadBalancerArn = eventItem.configItems[ResourceConstants.LOAD_BALANCER_ARN]
                response = elbClient.delete_load_balancer(LoadBalancerArn=loadBalancerArn)

            responseStatusCode = response[Constants.ELB_STATUS_CODE_RESPONSE_METADATA][Constants.ELB_HTTP_STATUS_CODE]
            if responseStatusCode == 200:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("{} deleted successfully.".format(ResourceConstants.ELB_KEYWORD))
                self._AbstractAction__actionMessage = _("{} Deleted".format(ResourceConstants.ELB_KEYWORD))
                LoggerUtility.logInfo("{} deleted successfully.".format(ResourceConstants.ELB_KEYWORD))
            else:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("failed to delete {}.".format(ResourceConstants.ELB_KEYWORD))
                self._AbstractAction__actionMessage = _("Could not delete {} {}. Response status code {}".format(ResourceConstants.ELB_KEYWORD, eventItem.resourceId, responseStatusCode))
                LoggerUtility.logInfo("failed to delete Unused {}.".format(ResourceConstants.ELB_KEYWORD))

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
            errorMessage = "Error occured while deleting unused {}. {}".format(ResourceConstants.ELB_KEYWORD, e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            self._AbstractAction__actionMessage = errorMessage
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)

        return evaluationResult
