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
""" This module will fetch launch configurations from all the available regions. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import ResourceConstants, ManagedCloudConstants, BotoConstants, AWSResourceClassConstants


class DeleteUnusedLaunchConfigurationsFetcher(AbstractResourceFetcher):
    """ This class is responsible for fetching the resources """
    def __parseAndFetchInstanceDetails(self, launchConfigurationObject):
        """ This method will be used to fetch and parse instance details. """
        resourceId = launchConfigurationObject[ResourceConstants.LAUNCH_CONFIGURATION_NAME]
        configItems = launchConfigurationObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.LAUNCH_CONFIGURATION_RESOURCE, configItems=configItems)

    def resourceFetcher(self):
        launchConfigurationsList = []
        try:
            awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
            regions = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)
            for region in regions:
                asgClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_ASC,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )

                paginator = asgClient.get_paginator(ResourceConstants.LAUNCH_CONFIGURATION_METHOD_NAME)
                for paginatorResponse in paginator.paginate():
                    response = CommonUtility.changeDictionaryKeysToLowerCase(paginatorResponse)
                    launchConfigurations = []
                    if response.__contains__(ResourceConstants.LAUNCH_CONFIGURATIONS):
                        launchConfigurations = response[ResourceConstants.LAUNCH_CONFIGURATIONS]

                    for launchConfiguration in launchConfigurations:
                        launchConfigurationObject = launchConfiguration
                        launchConfigurationObject.update({ManagedCloudConstants.REGION_REFERENCE: region})
                        eventItems = self.__parseAndFetchInstanceDetails(launchConfigurationObject)
                        launchConfigurationsList.append(eventItems)

        except AttributeError as e:
            LoggerUtility.logError("AttributeError occurred while fetcing the launch configurations {} ".format(e))
        except ValueError as e:
            LoggerUtility.logError("ValueError occurred while fetcing the launch configurations {} ".format(e))
        except KeyError as e:
            LoggerUtility.logError("KeyError occurred while fetcing the launch configurations {} ".format(e))
        except ClientError as e:
            LoggerUtility.logError("Boto ClientError occurred while fetcing the launch configurations {} ".format(e))
        except Exception as e:
            LoggerUtility.logError("Error occurred while fetcing the launch configurations {} ".format(e))
        return launchConfigurationsList
