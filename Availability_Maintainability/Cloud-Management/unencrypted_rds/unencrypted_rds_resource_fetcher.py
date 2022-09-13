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
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import BotoConstants, AWSResourceClassConstants, ManagedCloudConstants
from common.rds_constants import RdsConstants


class UnencryptedRdsResourceFetcher(AbstractResourceFetcher):
    """ This class is created for Fetching the resource details using Boto Client and provide the reource details to EventItem. """
    def __parseAndFetchInstanceDetails(self, instanceObject):
        """Method will fetch instance details and assign it to configItems."""
        resourceId = instanceObject[RdsConstants.RDS_RESOURCE_ID]
        configItems = instanceObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.RDS_INSTANCE, configItems=configItems)

    def resourceFetcher(self):
        unencryptedRDS = []
        errorMessage = "No resource are found."
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
                LoggerUtility.logInfo('Fetching RDS Instances in region: {}'.format(region))
                paginator = rdsClient.get_paginator('describe_db_instances')
                for paginatorResponse in paginator.paginate():
                    response = CommonUtility.changeDictionaryKeysToLowerCase(paginatorResponse)
                    dbInstances = response[RdsConstants.RDS_RESPONSE_KEY]
                    for dbInstance in dbInstances:
                        dbInstance.update({ManagedCloudConstants.REGION_REFERENCE: region})
                        eventItems = self.__parseAndFetchInstanceDetails(dbInstance)
                        unencryptedRDS.append(eventItems)

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is Invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while fetching RDS Instances. {}".format(e)
        if not unencryptedRDS:
            LoggerUtility.logError(errorMessage)

        return unencryptedRDS
