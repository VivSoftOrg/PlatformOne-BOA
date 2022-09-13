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
""" This module will fetch the RDS Instance resource details and send it to Evaluator.  """
from botocore.exceptions import ClientError

from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.boto_utility import BotoUtility
from common.common_constants import (AWSResourceClassConstants, BotoConstants,
                                     ManagedCloudConstants)
from common.common_utility import CommonUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.logger_utility import LoggerUtility
from rules_common.RuleConstants import RuleConstants


class CopyRdsTagsToSnapshotsResourceFetcher(AbstractResourceFetcher):
    """ This class is created for Fetching the resource details using Boto Client and provide the reource details to EventItem. """

    def __parseAndFetchDbInstanceDetails(self, dbInstanceObject, dbInstTags):
        """Method will fetch instance details and assign it to configItems."""
        resourceId = dbInstanceObject[RuleConstants.RDS_INSTANCE_ID]
        configItems = dbInstanceObject
        configItems[RuleConstants.EVENTITEM_TAGS_KEY] = []
        if dbInstTags:
            configItems[RuleConstants.EVENTITEM_TAGS_KEY].append(dbInstTags)
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(
            resourceId=resourceId,
            resourceType=AWSResourceClassConstants.RDS_INSTANCE,
            configItems=configItems
        )

    def resourceFetcher(self):
        """ This method fetches all the RDS Instances """
        rdsInstancesList = []
        errorMessage = ""
        awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
        regions = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)
        try:
            for region in regions:
                rdsClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_RDS,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )
                LoggerUtility.logInfo('Fetching Instances in region: {}'.format(region))
                paginator = rdsClient.get_paginator('describe_db_instances')
                for paginatorResponse in paginator.paginate():
                    response = CommonUtility.changeDictionaryKeysToLowerCase(paginatorResponse)

                    dbInstances = response[RuleConstants.RDS_INSTANCES_REFERENCE]
                    for dbInstance in dbInstances:
                        dbInstance.update({ManagedCloudConstants.REGION_REFERENCE: region})
                        rdsTags = rdsClient.list_tags_for_resource(
                            ResourceName=dbInstance[RuleConstants.RDS_INSTANCE_ARN]
                        )[RuleConstants.RDS_TAG_LIST]
                        eventItem = self.__parseAndFetchDbInstanceDetails(dbInstance, rdsTags)
                        rdsInstancesList.append(eventItem)

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is Invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type doesn't possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while {}".format(e)
        if errorMessage:
            LoggerUtility.logError(errorMessage)

        return rdsInstancesList
