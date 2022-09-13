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
""" This module will fetch the ALB resource details and send it to Evaluator.  """
from os import environ

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.dynamo_db_utility import DynamoDbUtility
from common.logger_utility import LoggerUtility
from rules_common.aws_resource_utility.rules_constants import MonitoredResourceConstants
from utility.class_utility import ClassUtility
from tag_validator.tag_validator_constants import Constants


class TagValidatorResourceFetcher(AbstractResourceFetcher):
    """ This class is created for Fetching the resource details, which will be passed to Evaluator for validating Tags."""

    def resourceFetcher(self):
        """ This method fetches all the configured resources and paases them to evaluator"""
        try:
            resourceList = []
            errorMessage = "No Resources are available."
            eventParam = self._AbstractResourceFetcher__eventParam

            dynamoDBTagValidatorTable = environ[Constants.MONITORING_RESOURCES_DYNAMO_DB_TABLE]
            keyConditionAccountNo = Key('aws_account_no').eq(str(eventParam.accNo))
            resourcesToCheck = DynamoDbUtility.queryDynamodbData(dynamoDBTagValidatorTable, keyConditionAccountNo)

            for resource in resourcesToCheck:
                resourceList += ClassUtility.getclassObject(
                    "rules_common.aws_resource_utility",
                    MonitoredResourceConstants.MONITERED_RESOURCES_DICT_REF[resource[MonitoredResourceConstants.RESOURCE_TYPE]],
                    MonitoredResourceConstants.RESOURCE_UTILITY_REFERENCE,
                    eventParam
                ).fetchResources()
            return resourceList

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is Invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type doesn't possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying2 to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while {}".format(e)
        if not resourceList:
            LoggerUtility.logError(errorMessage)
            return False

        return resourceList
