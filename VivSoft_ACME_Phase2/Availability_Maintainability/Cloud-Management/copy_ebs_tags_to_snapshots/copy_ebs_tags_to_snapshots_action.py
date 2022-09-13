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
from common.common_constants import (BotoConstants, ComplianceConstants,
                                     ManagedCloudConstants)
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from copy_ebs_tags_to_snapshots.copy_ebs_tags_to_snapshots_constants import \
    Constants


class CopyEbsTagsToSnapshotsAction(AbstractAction):
    """This class perform action as it stop Instances if it is non_compliant """

    def performAction(self, eventItem):
        """ This method add tags to all the NON_COMPLIANT Snapshots. """
        evaluationResult = EvaluationResult()
        errorMessage = ""
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            for tags in eventItem.configItems[Constants.COPY_TAGS]:
                response = ec2Client.create_tags(
                    Resources=[tags[Constants.ID]],
                    Tags=tags[Constants.TAGS_TO_COPY]
                )

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while copying tags. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            self._AbstractAction__actionMessage = _(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)
        else:
            message = "Copied tags from volume to all its attached snapshots"
            LoggerUtility.logInfo(message)
            self._AbstractAction__actionMessage = _(message)
            evaluationResult.annotation = _(message)
            evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE

        return evaluationResult
