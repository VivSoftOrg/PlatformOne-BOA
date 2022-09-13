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
from rules_common.RuleConstants import RuleConstants


class CopyRdsTagsToSnapshotsAction(AbstractAction):
    """This class perform action as it stop Instances if it is non_compliant """

    def performAction(self, eventItem):
        """ This method add tags to all the NON_COMPLIANT Snapshots. """
        evaluationResult = EvaluationResult()
        errorMessage = ""
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            rdsClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_RDS,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            for tags in eventItem.configItems[RuleConstants.COPY_TAGS]:
                response = rdsClient.add_tags_to_resource(
                    ResourceName=tags[RuleConstants.ID],
                    Tags=tags[RuleConstants.TAGS_TO_COPY]
                )
            for tags in eventItem.configItems[RuleConstants.UPDATE_TAGS]:
                tagKeys = []
                for tag in tags[RuleConstants.TAGS_TO_COPY]:
                    tagKeys.append(tag[RuleConstants.RDS_TAG_VALUE])
                response = rdsClient.remove_tags_from_resource(
                    ResourceName=tags[RuleConstants.ID],
                    TagKeys=tagKeys
                )
                response = rdsClient.add_tags_to_resource(
                    ResourceName=tags[RuleConstants.ID],
                    Tags=tags[RuleConstants.TAGS_TO_COPY]
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

        message = ""
        complianceType = ""
        if errorMessage != "":
            message = errorMessage
            LoggerUtility.logError(message)
            complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
        else:
            message = "Copied tags from the instances to all the attached snapshots"
            LoggerUtility.logInfo(message)
            complianceType = ComplianceConstants.COMPLIANT_RESOURCE

        self._AbstractAction__actionMessage = _(message)
        evaluationResult.complianceType = complianceType
        evaluationResult.annotation = _(message)

        return evaluationResult
