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
""" This module will remove unused launch configuration """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants, ManagedCloudConstants, ComplianceConstants
from common.framework_objects import EvaluationResult


class DeleteUnusedLaunchConfigurationsAction(AbstractAction):
    """ This class will be responsible for performing action if the resource is non-compliant. """
    def performAction(self, eventItem):
        try:
            evaluationResult = EvaluationResult()
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            asgClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_ASC,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            response = asgClient.delete_launch_configuration(
                LaunchConfigurationName=eventItem.resourceId)

            if response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = ('The launch configuration is deleted.')
                self._AbstractAction__actionMessage = _("Launch configuration is deleted.")
                LoggerUtility.logInfo("Launch configuration '{}' is deleted".format(eventItem.resourceId))
                return evaluationResult
            else:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = ('Could not delete launch configuration.')
                self._AbstractAction__actionMessage = _("Could not delete launch configuration")
                LoggerUtility.logError("Could not delete launch configuration '{}', HTTPStatus Code : {}.".format(
                    eventItem.resourceId,
                    response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]))

        except AttributeError as e:
            LoggerUtility.logError(
                "AttributeError occurred while deleting launch configuration : {id}. Exception Raised : {error}".format(
                    id=eventItem.resourceId,
                    error=e))
            self._AbstractAction__actionMessage = _("Error occurred while deleting launch configuration")
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except ValueError as e:
            LoggerUtility.logError(
                "ValueError occurred while deleting launch configuration : {id}. Exception Raised : {error}".format(
                    id=eventItem.resourceId,
                    error=e))
            self._AbstractAction__actionMessage = _("Error occurred while deleting launch configuration")
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except KeyError as e:
            LoggerUtility.logError(
                "KeyError occurred while deleting launch configuration : {id}. Exception Raised : {error}".format(
                    id=eventItem.resourceId,
                    error=e))
            self._AbstractAction__actionMessage = _("Error occurred while deleting launch configuration")
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except ClientError as e:
            LoggerUtility.logError(
                "Boto ClientError occurred while deleting launch configuration : {id}. Exception Raised : {error}".format(
                    id=eventItem.resourceId,
                    error=e))
            self._AbstractAction__actionMessage = _("Error occurred while deleting launch configuration")
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except Exception as e:
            self._AbstractAction__actionMessage = _("Error occurred while deleting launch configuration")
            LoggerUtility.logError(
                "Error occurred while deleting launch configuration : {id}. Exception Raised : {error}".format(
                    id=eventItem.resourceId,
                    error=e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        return evaluationResult
