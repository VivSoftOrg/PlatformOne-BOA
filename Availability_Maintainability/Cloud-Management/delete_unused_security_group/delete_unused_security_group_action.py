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
""" This module will remove unused security groups. """
from botocore.exceptions import ClientError

from common.abstract_action import AbstractAction
from common.boto_utility import BotoUtility
from common.common_constants import BotoConstants, ComplianceConstants
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from delete_unused_security_group.delete_unused_security_group_constants import \
    SecurityGroupConstants


class DeleteUnusedSGAction(AbstractAction):
    """ This class will be responsible for performing action if the resource is non-compliant. """

    def performAction(self, eventItem):
        try:
            evaluationResult = EvaluationResult()
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[SecurityGroupConstants.REGION_KEYWORD]
            )

            response = ec2Client.delete_security_group(GroupId=eventItem.resourceId)

            if response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = "Deleted unused security group"
                self._AbstractAction__actionMessage = _("Deleted unused security group")
                LoggerUtility.logInfo("Deleted unused security group : {}".format(eventItem.resourceId))
            else:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "Could not delete unused security group"
                self._AbstractAction__actionMessage = _("Could not delete unused security group : {}, HTTPStatus Code : {}.".format(
                    eventItem.resourceId,
                    response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]))
                LoggerUtility.logError("Could not delete unused security group: {}, HTTPStatus Code : {}.".format(
                    eventItem.resourceId,
                    response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]))
            LoggerUtility.logInfo('Deleted unused security group : {}'.format(eventItem.resourceId))

        except AttributeError as e:
            LoggerUtility.logError("AttributeError occurred while deleting the security group {}. Exception Raised : {}".format(eventItem.resourceId, e))
            self._AbstractAction__actionMessage = _("Error occurred while deleting the security group")
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except ValueError as e:
            LoggerUtility.logError("ValueError occurred while deleting the security group {}. Exception Raised : {}".format(eventItem.resourceId, e))
            self._AbstractAction__actionMessage = _("Error occurred while deleting the security group")
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except KeyError as e:
            LoggerUtility.logError("KeyError occurred while deleting the security group {}. Exception Raised : {}".format(eventItem.resourceId, e))
            self._AbstractAction__actionMessage = _("Error occurred while deleting the security group")
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except ClientError as e:
            LoggerUtility.logError("Boto ClientError occurred while deleting the security group {}. Exception Raised : {}".format(eventItem.resourceId, e))
            self._AbstractAction__actionMessage = _("Error occurred while deleting the security group")
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except Exception as e:
            LoggerUtility.logError("Error occurred while deleting the security group {}. Exception Raised : {}".format(eventItem.resourceId, e))
            self._AbstractAction__actionMessage = _("Error occurred while deleting the security Ggroup")
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        return evaluationResult
