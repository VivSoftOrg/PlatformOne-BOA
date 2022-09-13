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
""" This module will remove unused route table. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.framework_objects import EvaluationResult
from common.common_constants import ComplianceConstants, ManagedCloudConstants, BotoConstants


class DeleteUnusedRouteTablesAction(AbstractAction):
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
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            response = ec2Client.delete_route_table(
                RouteTableId=eventItem.resourceId
            )

            if response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = "Route table is removed"
                self._AbstractAction__actionMessage = _("Route table is removed")
                LoggerUtility.logInfo("Route table is removed: {}".format(eventItem.resourceId))
            else:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "Could not remove route table"
                self._AbstractAction__actionMessage = _("Could not remove route table")
                LoggerUtility.logError("Could not remove route table: {}, HTTPStatus Code : {}.".format(
                    eventItem.resourceId,
                    response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]))

        except ValueError as e:
            LoggerUtility.logError(
                "ValueError occurred while removing route table : {id}. Exception Raised : {error}".format(
                    id=eventItem.resourceId,
                    error=e))
            self._AbstractAction__actionMessage = _("Error occurred while removing route table")
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except KeyError as e:
            LoggerUtility.logError(
                "KeyError occurred while removing route table : {id}. Exception Raised : {error}".format(
                    id=eventItem.resourceId,
                    error=e))
            self._AbstractAction__actionMessage = _("Error occurred while removing route table")
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except AttributeError as e:
            LoggerUtility.logError(
                "AttributeError occurred while removing route table : {id}. Exception Raised : {error}".format(
                    id=eventItem.resourceId,
                    error=e))
            self._AbstractAction__actionMessage = _("Error occurred while removing route table")
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except ClientError as e:
            self._AbstractAction__actionMessage = _("Error occurred while removing route table")
            LoggerUtility.logError(
                "Boto ClientError occurred while removing route table : {id}. Exception Raised : {error}".format(
                    id=eventItem.resourceId,
                    error=e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except Exception as e:
            self._AbstractAction__actionMessage = _("Error occurred while removing route table")
            LoggerUtility.logError(
                "Error occurred while removing route table : {id}. Exception Raised : {error}".format(
                    id=eventItem.resourceId,
                    error=e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        return evaluationResult
