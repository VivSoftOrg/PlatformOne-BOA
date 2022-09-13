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
""" This module will remove NoShutdown tag from the EC2 instances. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.logger_utility import LoggerUtility
from common.framework_objects import EvaluationResult
from common.common_constants import BotoConstants
from common.common_constants import ComplianceConstants
from common.common_constants import TagsConstants
from ec2_noshutdown_tag.ec2_noshutdown_tag_constants import NoShutDownTagConstants


class Ec2NoshutdownTagAction(AbstractAction):
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
                eventItem.configItems[NoShutDownTagConstants.REGION_KEYWORD]
            )

            response = ec2Client.delete_tags(
                Resources=[eventItem.resourceId],
                Tags=[{TagsConstants.TAG_KEY_REFERENCE: eventItem.configItems[NoShutDownTagConstants.NOSHUTDOWN_KEY]}])

            if response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = "NoShutdown tag is removed."
                self._AbstractAction__actionMessage = "NoShutdown tag is removed."
                LoggerUtility.logInfo("NoShutdown tag is removed from instance : {}".format(eventItem.resourceId))
            else:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "Could not remove NoShutdown tag."
                self._AbstractAction__actionMessage = "Could not remove NoShutdown tag."
                LoggerUtility.logError("Could not remove NoShutdown tag from instance: {}, HTTPStatus Code : {}.".format(
                    eventItem.resourceId,
                    response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]))

        except ValueError as e:
            LoggerUtility.logError("ValueError occurred while removing NoShutdown tag : {}".format(e))
            self._AbstractAction__actionMessage = "Error occurred while removing NoShutdown tag."
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except KeyError as e:
            LoggerUtility.logError("KeyError occurred while removing NoShutdown tag : {}".format(e))
            self._AbstractAction__actionMessage = "Error occurred while removing NoShutdown tag."
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except AttributeError as e:
            LoggerUtility.logError("AttributeError occurred while removing NoShutdown tag : {}".format(e))
            self._AbstractAction__actionMessage = "Error occurred while removing NoShutdown tag."
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except ClientError as e:
            LoggerUtility.logError("Boto ClientError occurred while removing NoShutdown tag : {}".format(e))
            self._AbstractAction__actionMessage = "Error occurred while removing NoShutdown tag."
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except Exception as e:
            LoggerUtility.logError("Error occurred while removing NoShutdown tag : {}".format(e))
            self._AbstractAction__actionMessage = "Error occurred while removing NoShutdown tag."
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        return evaluationResult
