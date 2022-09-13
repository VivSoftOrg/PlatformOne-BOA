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
""" This module will fetch all types of load balancers for the available regions. """
from botocore.exceptions import ClientError

from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.boto_utility import BotoUtility
from common.common_constants import (AWSResourceClassConstants, BotoConstants,
                                     ResourceConstants, ManagedCloudConstants)
from common.common_utility import CommonUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.logger_utility import LoggerUtility


class CheckELBRequiredTagValuesResourceFetcher(AbstractResourceFetcher):
    """ This class is responsible for fetching the resources """
    def __fetchClassicElbList(self, loadBalancerList, regions, awsPartitionName):
        """ This method will be used to fetch classic load balancers. """
        try:
            for region in regions:
                elbClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_ELB,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )
                LoggerUtility.logInfo('Fetching elbs...')
                response = CommonUtility.changeDictionaryKeysToLowerCase(elbClient.describe_load_balancers())
                elasticLoadBalancers = []
                if response.__contains__(ResourceConstants.LOAD_BALANCER_DESCRIPTIONS):
                    elasticLoadBalancers = response[ResourceConstants.LOAD_BALANCER_DESCRIPTIONS]

                for loadBalancer in elasticLoadBalancers:
                    loadBalancerObject = loadBalancer
                    loadBalancerObject.update({ManagedCloudConstants.REGION_REFERENCE: region})
                    resourceType = AWSResourceClassConstants.ELB_RESOURCE
                    eventItems = self.__parseAndFetchELBDetails(loadBalancerObject, resourceType)
                    loadBalancerList.append(eventItems)
        except ClientError as e:
            LoggerUtility.logError("Boto ClientError occurred while fetching elastic load balancers : {}".format(e))
        except Exception as e:
            LoggerUtility.logError("Error occurred while fetching elastic load balancers : {}".format(e))
        return loadBalancerList

    def __fetchApplicationAndNetworkElbList(self, loadBalancerList, regions, awsPartitionName):
        """ This method will be used to fetch application and network load balancers. """
        try:
            for region in regions:
                elbClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_ELB_V2,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )
                LoggerUtility.logInfo('Fetching albs...')
                response = CommonUtility.changeDictionaryKeysToLowerCase(elbClient.describe_load_balancers())
                elasticLoadBalancers = []
                if response.__contains__(ResourceConstants.LOAD_BALANCERS):
                    elasticLoadBalancers = response[ResourceConstants.LOAD_BALANCERS]

                for loadBalancer in elasticLoadBalancers:
                    loadBalancerObject = loadBalancer
                    loadBalancerObject.update({ManagedCloudConstants.REGION_REFERENCE: region})
                    resourceType = AWSResourceClassConstants.ELB_V2_RESOURCE
                    eventItems = self.__parseAndFetchELBDetails(loadBalancerObject, resourceType)
                    loadBalancerList.append(eventItems)
        except ClientError as e:
            LoggerUtility.logError("Boto ClientError occurred while fetching application and network load balancers : {}".format(e))
        except Exception as e:
            LoggerUtility.logError("Error occurred while fetching application and network load balancers : {}".format(e))
        return loadBalancerList

    def __parseAndFetchELBDetails(self, instanceObject, resourceType):
        """ This method will be used to fetch and parse load balancer details. """
        resourceId = instanceObject[ResourceConstants.LOAD_BALANCER_NAME]
        configItems = instanceObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=resourceType, configItems=configItems)

    def resourceFetcher(self):
        loadBalancerList = []
        awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
        regions = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)
        try:
            loadBalancerList = self.__fetchClassicElbList(loadBalancerList, regions, awsPartitionName)
            loadBalancerList = self.__fetchApplicationAndNetworkElbList(loadBalancerList, regions, awsPartitionName)
        except Exception as e:
            LoggerUtility.logError("Error occurred while fetching the resources : {}".format(e))
        return loadBalancerList
