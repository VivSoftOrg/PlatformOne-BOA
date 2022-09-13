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
""" This module fetches the RDS instances """
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import AWSResourceClassConstants, BotoConstants, ResourceConstants, ManagedCloudConstants


class RdsExpiryTagFetcher(AbstractResourceFetcher):
    """ This class is used to fetch details of an RDS Instance """

    def __parseAndFetchInstanceDetails(self, instanceObject):
        """ This method is used to fetch and parse EC2 instance details """
        resourceId = instanceObject['dbiresourceid']
        configItems = instanceObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.RDS_INSTANCE, configItems=configItems)

    def __getTagsFromRDS(self, dbInstanceARN, rdsClient):
        """ This method is used to fetch the tags of instance """
        tagList = {}
        tagsResponse = rdsClient.list_tags_for_resource(ResourceName=dbInstanceARN)
        tagsResponse = CommonUtility.changeDictionaryKeysToLowerCase(tagsResponse)
        tagList.update({'tags': tagsResponse['taglist']})
        return tagList

    def resourceFetcher(self):
        """ This metho is used to fetch resources relate to RDS """
        rdsInstancesList = []
        try:
            awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
            regions = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)
            for region in regions:
                rdsClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_RDS,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )
                paginatorResponse = rdsClient.get_paginator('describe_db_instances')
                for response in paginatorResponse.paginate():
                    rdsInstanceResponse = CommonUtility.changeDictionaryKeysToLowerCase(response)
                    for instances in rdsInstanceResponse['dbinstances']:
                        instanceObject = instances
                        dbInstanceARN = instanceObject['dbinstancearn']
                        instanceObject.update({ManagedCloudConstants.REGION_REFERENCE: region})
                        tagList = self.__getTagsFromRDS(dbInstanceARN, rdsClient)
                        instanceObject.update(tagList)
                        instanceObject.update({ResourceConstants.RESOURCE_TYPE_NAME: 'RDS Instance'})
                        eventItems = self.__parseAndFetchInstanceDetails(instanceObject)
                        rdsInstancesList.append(eventItems)
        except Exception as e:
            LoggerUtility.logError("Error occurred while fetching EC2 instances : {}".format(e))
            return False

        return rdsInstancesList
