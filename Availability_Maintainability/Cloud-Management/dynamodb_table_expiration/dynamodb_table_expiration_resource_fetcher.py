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
""" This module will fetch the resource details. """
import traceback
import sys
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.common_utility import CommonUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import BotoConstants, AWSResourceClassConstants
from dynamodb_table_expiration.dynamodb_table_expiration_constants import Constants


class DynamoDBTableResourceFetcher(AbstractResourceFetcher):
    """ This class is created for Fetching the resource details using Boto Client and provide the reource details to EventItem. """
    def __parseTableObjectAndFetchTags(self, tableResourceObject, region, botoResource):
        """Method will fetch resource details and assign it to configItems."""
        resourceName = tableResourceObject.table_name
        resourceARN = tableResourceObject.table_arn
        tableTagList = botoResource.meta.client.list_tags_of_resource(ResourceArn=resourceARN)
        tableTagList = CommonUtility.changeDictionaryKeysToLowerCase(tableTagList)
        configItems = {
            'tags': tableTagList['tags'],
            'region': region,
            'resourceName': resourceName,
            'ARN': resourceARN
        }
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceName, resourceType=AWSResourceClassConstants.DYNAMO_DB_RESOURCE, configItems=configItems)

    def resourceFetcher(self):
        tablesList = []
        awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
        regions = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)

        try:
            for region in regions:
                dynamoDBResource = None
                dynamoDBResource = BotoUtility.getResource(
                    resourceType=BotoConstants.BOTO_CLIENT_AWS_DYNAMO_DB,
                    accNo=self._AbstractResourceFetcher__eventParam.accNo,
                    roleType=BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName=awsPartitionName,
                    region=region
                )

                LoggerUtility.logInfo('Fetching Table Names in region {}'.format(region))
                tablesIterator = dynamoDBResource.tables.all()
                for table in tablesIterator:
                    if table.table_status == Constants.DYNAMO_DB_ACTIVE_STATUS_REF:
                        response = self.__parseTableObjectAndFetchTags(table, region, dynamoDBResource)
                        tablesList.append(response)

        except ValueError as e:
            LoggerUtility.logError("The content of the object you tried to assign the value is Invalid. {}".format(e))
        except AttributeError as e:
            LoggerUtility.logError("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
        except TypeError as e:
            LoggerUtility.logError("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
        except NameError as e:
            LoggerUtility.logError("Trying to access a variable that you have not defined properly. {}".format(e))
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
        except Exception as e:
            LoggerUtility.logError("Error occured while fetching Dynamodb tables. {}".format(e))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)

        return tablesList
