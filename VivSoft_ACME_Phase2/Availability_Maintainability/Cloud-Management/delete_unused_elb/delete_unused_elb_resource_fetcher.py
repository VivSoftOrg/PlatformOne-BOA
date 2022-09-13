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

from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.boto_utility import BotoUtility
from common.common_constants import (AWSResourceClassConstants, BotoConstants,
                                     ManagedCloudConstants, ResourceConstants)
from common.common_utility import CommonUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.logger_utility import LoggerUtility
from delete_unused_elb.delete_unused_elb_constants import Constants
from common_constants.exception_constants import ExceptionMessages


class DeleteUnusedELBResourceFetcher(AbstractResourceFetcher):
    """ This class is created for Fetching the resource details using Boto Client and provide the reource details to EventItem. """

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
                LoggerUtility.logInfo('Fetching Classic ELBs in ' + region)
                paginator = elbClient.get_paginator('describe_load_balancers')
                for paginatorResponse in paginator.paginate():
                    response = CommonUtility.changeDictionaryKeysToLowerCase(paginatorResponse)
                    elasticLoadBalancers = []
                    if response.__contains__(Constants.ELB_DESCRIPTION_KEY):
                        elasticLoadBalancers = response[Constants.ELB_DESCRIPTION_KEY]

                    for loadBalancer in elasticLoadBalancers:
                        tagResponse = elbClient.describe_tags(LoadBalancerNames=[loadBalancer['loadbalancername']])['TagDescriptions'][0]['Tags']
                        tags = CommonUtility.changeDictionaryKeysToLowerCase(tagResponse)
                        loadBalancer.update({'tags': tags})
                        loadBalancerObject = loadBalancer
                        loadBalancerObject.update({ManagedCloudConstants.REGION_REFERENCE: region})
                        loadBalancerObject.update({'type': 'classic'})
                        resourceType = AWSResourceClassConstants.ELB_RESOURCE
                        eventItems = self.__parseAndFetchELBDetails(loadBalancerObject, resourceType)
                        loadBalancerList.append(eventItems)
        except ClientError as e:
            LoggerUtility.logError("Boto ClientError occurred while fetching classic elastic load balancers : {}".format(e))
            return False
        except Exception as e:
            LoggerUtility.logError("Error occurred while fetching classic elastic load balancers : {}".format(e))
            return False
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
                LoggerUtility.logInfo('Fetching Application/Network ELBs in ' + region)
                paginator = elbClient.get_paginator('describe_load_balancers')
                for paginatorResponse in paginator.paginate():
                    response = CommonUtility.changeDictionaryKeysToLowerCase(paginatorResponse)
                    elasticLoadBalancers = []
                    if response.__contains__(Constants.ELB_V2_DESCRIPTION_KEY):
                        elasticLoadBalancers = response[Constants.ELB_V2_DESCRIPTION_KEY]

                    for loadBalancer in elasticLoadBalancers:
                        tagResponse = elbClient.describe_tags(ResourceArns=[loadBalancer['loadbalancerarn']])['TagDescriptions'][0]['Tags']
                        tags = CommonUtility.changeDictionaryKeysToLowerCase(tagResponse)
                        loadBalancer.update({'tags': tags})
                        loadBalancerObject = loadBalancer
                        loadBalancerObject.update({ManagedCloudConstants.REGION_REFERENCE: region})
                        resourceType = AWSResourceClassConstants.ELB_V2_RESOURCE
                        eventItems = self.__parseAndFetchELBDetails(loadBalancerObject, resourceType)
                        loadBalancerList.append(eventItems)
        except ClientError as e:
            LoggerUtility.logError("Boto ClientError occurred while fetching application and network load balancers : {}".format(e))
            return False
        except Exception as e:
            LoggerUtility.logError("Error occurred while fetching application and network load balancers : {}".format(e))
            return False
        return loadBalancerList

    def __parseAndFetchELBDetails(self, instanceObject, resourceType):
        """ This method will be used to fetch and parse load balancer details. """
        resourceId = instanceObject[ResourceConstants.LOAD_BALANCER_NAME]
        configItems = instanceObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=resourceType, configItems=configItems)

    def resourceFetcher(self):
        loadBalancerList = []
        errorMessage = ""
        awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
        regions = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)
        try:
            # Fetch Classic Load Balancer
            loadBalancerList = self.__fetchClassicElbList(loadBalancerList, regions, awsPartitionName)

            # Fetch Application and Network Load Balancer
            loadBalancerList = self.__fetchApplicationAndNetworkElbList(loadBalancerList, regions, awsPartitionName)

        except ValueError as e:
            errorMessage = ExceptionMessages.VALUE_ERROR.format(e)
        except AttributeError as e:
            errorMessage = ExceptionMessages.ATTRIBUTE_ERROR.format(e)
        except TypeError as e:
            errorMessage = ExceptionMessages.TYPE_ERROR.format(e)
        except NameError as e:
            errorMessage = ExceptionMessages.NAME_ERROR.format(e)
        except ClientError as e:
            errorMessage = ExceptionMessages.CLIENT_ERROR.format(e)
        except Exception as e:
            errorMessage = "Error occured while {}".format(e)
        if errorMessage:
            LoggerUtility.logError(errorMessage)

        return loadBalancerList
