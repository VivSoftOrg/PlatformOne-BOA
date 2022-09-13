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
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.framework_objects import EvaluationResult
from common.common_constants import BotoConstants, ComplianceConstants, ManagedCloudConstants


class StopInstancesOverWeekendAction(AbstractAction):
    """This class perform action as it stop Instances if it is non_compliant """
    def performAction(self, eventItem):
        evaluationResult = EvaluationResult()
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )
            response = ec2Client.stop_instances(
                InstanceIds=[
                    eventItem.resourceId,
                ], Force=True)

            if response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                LoggerUtility.logInfo("Instance Stopped")
                self._AbstractAction__actionMessage = _("Instance Stopped")
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = ('Instances do not have NoShutdown tag, stopping instances.')
            else:
                LoggerUtility.logInfo("Could not stop instance")
                self._AbstractAction__actionMessage = _("Could not stop instance")
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = ('Instances do not have NoShutdown tag, Unable to stop instances.')

        except ValueError as e:
            LoggerUtility.logError("The content of the object you tried to assign the value is invalid. {}".format(e))
            self._AbstractAction__actionMessage = _("The content of the object you tried to assign the value is invalid. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _("The content of the object you tried to assign the value is invalid. {}".format(e))
        except AttributeError as e:
            LoggerUtility.logError("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
            self._AbstractAction__actionMessage = _("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
        except TypeError as e:
            LoggerUtility.logError("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
            self._AbstractAction__actionMessage = _("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
        except NameError as e:
            LoggerUtility.logError("Trying to access a variable that you have not defined properly. {}".format(e))
            self._AbstractAction__actionMessage = _("Trying to access a variable that you have not defined properly. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _("Trying to access a variable that you have not defined properly. {}".format(e))
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            self._AbstractAction__actionMessage = _("Boto client error occured. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _("Boto client error occured. {}".format(e))
        except Exception as e:
            LoggerUtility.logError("Error occured while stopping instances. {}".format(e))
            self._AbstractAction__actionMessage = _("Error occured while stopping instances. {}".format(e))
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _("Error occured while stopping instances. {}".format(e))

        return evaluationResult
