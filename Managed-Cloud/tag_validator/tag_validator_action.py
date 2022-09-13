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
from os import environ

from boto3.dynamodb.conditions import Key

from common.abstract_action import AbstractAction
from common.common_constants import ComplianceConstants
from common.dynamo_db_utility import DynamoDbUtility
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from rules_common.aws_resource_utility.rules_constants import \
    MonitoredResourceConstants
from utility.class_utility import ClassUtility
from tag_validator.tag_validator_constants import Constants


class TagValidatorAction(AbstractAction):
    """This class perform actions on non_compliant """

    def performAction(self, eventItem):
        """ This method performs action on Non Compliant resources """
        evaluationResult = EvaluationResult()
        exceptionMessage = ''
        try:
            dynamoDBTagValidatorTable = environ[Constants.MONITORING_RESOURCES_DYNAMO_DB_TABLE]
            keyConditionAccountNo = Key('aws_account_no').eq(str(self._AbstractAction__eventParam.accNo)) & Key('aws_resource_type').eq(eventItem.resourceType)
            performActionOnResources = DynamoDbUtility.queryDynamodbData(dynamoDBTagValidatorTable, keyConditionAccountNo)
            eventParam = self._AbstractAction__eventParam

            if performActionOnResources and 'dry_run' in performActionOnResources[0] and performActionOnResources[0]['dry_run']:
                evaluationResult, self._AbstractAction__actionMessage = ClassUtility.getclassObject(
                    "rules_common.aws_resource_utility",
                    MonitoredResourceConstants.MONITERED_RESOURCES_DICT_REF[eventItem.resourceType],
                    MonitoredResourceConstants.RESOURCE_UTILITY_REFERENCE,
                    eventParam
                ).executeTagNonComplianceAction(evaluationResult, eventItem)

            else:
                evaluationResult.complianceType = ComplianceConstants.INSUFFICIENT_RESOURCE_DATA
                evaluationResult.annotation = _("Unable to fetch configuration details about resource type {}".format(eventItem.resourceType))
                self._AbstractAction__actionMessage = _("Unable to fetch configuration details about resource type {}".format(eventItem.resourceType))

        except ValueError as e:
            exceptionMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            exceptionMessage = "Trying to access or call an attribute of a particular object type doesn't possess. {}".format(e)
        except TypeError as e:
            exceptionMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            exceptionMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except Exception as e:
            exceptionMessage = "Error occured while performing action on resource. {}".format(e)

        if exceptionMessage != '':
            LoggerUtility.logError(exceptionMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(exceptionMessage)
            self._AbstractAction__actionMessage = _(exceptionMessage)

        return evaluationResult
