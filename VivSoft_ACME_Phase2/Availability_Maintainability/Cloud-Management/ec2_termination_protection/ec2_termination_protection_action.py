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
""" This module will enable termination protection to the EC2 instances. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.logger_utility import LoggerUtility
from common.common_constants import ComplianceConstants, ManagedCloudConstants, BotoConstants, TagsConstants
from common.framework_objects import EvaluationResult


class Ec2TerminationProtectionAction(AbstractAction):
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

            response = ec2Client.modify_instance_attribute(
                DisableApiTermination={
                    TagsConstants.TAG_VALUE_REFERENCE: True},
                InstanceId=eventItem.resourceId)

            if response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = "Termination protection is enabled"
                self._AbstractAction__actionMessage = "Termination protection is enabled"
                LoggerUtility.logInfo("Termination protection is enabled")
            else:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "Could not enable termination protection"
                self._AbstractAction__actionMessage = "Could not enable termination protection for the Instance: {}, HTTPStatus Code : {}.".format(
                    eventItem.resourceId,
                    response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE])
                LoggerUtility.logError("Could not enable termination protection for the Instance: {}, HTTPStatus Code : {}.".format(
                    eventItem.resourceId,
                    response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]))

        except KeyError as e:
            LoggerUtility.logError("KeyError occurred while enabling termination protection for the Instance : {id}. Exception Raised : {error}".format(
                id=eventItem.resourceId,
                error=e))
            self._AbstractAction__actionMessage = "Error occurred while enabling termination protection for the Instance"
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except ValueError as e:
            LoggerUtility.logError("ValueError occurred while enabling termination protection for the Instance : {id}. Exception Raised : {error}".format(
                id=eventItem.resourceId,
                error=e))
            self._AbstractAction__actionMessage = "Error occurred while enabling termination protection for the Instance"
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except AttributeError as e:
            LoggerUtility.logError("AttributeError occurred while enabling termination protection for the Instance : {id}. Exception Raised : {error}".format(
                id=eventItem.resourceId,
                error=e))
            self._AbstractAction__actionMessage = "Error occurred while enabling termination protection for the Instance"
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except ClientError as e:
            LoggerUtility.logError("Boto ClientError occurred while enabling termination protection for the Instance : {id}. Exception Raised : {error}".format(
                id=eventItem.resourceId,
                error=e))
            self._AbstractAction__actionMessage = "Error occurred while enabling termination protection for the Instance"
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except Exception as e:
            LoggerUtility.logError("Error occurred while enabling termination protection for the Instance : {id}. Exception Raised : {error}".format(
                id=eventItem.resourceId,
                error=e))
            self._AbstractAction__actionMessage = "Error occurred while enabling termination protection for the Instance"
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        return evaluationResult
