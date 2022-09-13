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
""" This module will fetch route tables from all the available regions. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import AWSResourceClassConstants, ManagedCloudConstants, ResourceConstants, BotoConstants


class DeleteUnusedRouteTablesFetcher(AbstractResourceFetcher):
    """ This class is responsible for fetching the resources """
    def __parseAndFetchRouteTableDetails(self, routeTableObject):
        """ This method will be used fetch and parse  """
        resourceId = routeTableObject[ResourceConstants.RESOURCE_ROUTE_TABLE_ID]
        configItems = routeTableObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.ROUTE_TABLE_RESOURCE, configItems=configItems)

    def resourceFetcher(self):
        routeTableList = []
        try:
            awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
            regions = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)

            for region in regions:
                ec2Client = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_EC2,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )
                response = CommonUtility.changeDictionaryKeysToLowerCase(ec2Client.describe_route_tables())
                routeTables = []
                if response.__contains__(ResourceConstants.RESOURCE_ROUTE_TABLES):
                    routeTables = response[ResourceConstants.RESOURCE_ROUTE_TABLES]
                LoggerUtility.logInfo("Fetching resources....")
                for routeTable in routeTables:
                    routeTableObject = routeTable
                    routeTableObject.update({ManagedCloudConstants.REGION_REFERENCE: region})
                    eventItems = self.__parseAndFetchRouteTableDetails(routeTableObject)
                    routeTableList.append(eventItems)

        except AttributeError as e:
            LoggerUtility.logError("AttributeError occurred while fetching the route tables: {}".format(e))
        except KeyError as e:
            LoggerUtility.logError("KeyError occurred while fetching the route tables: {}".format(e))
        except ValueError as e:
            LoggerUtility.logError("ValueError occurred while fetching the route tables: {}".format(e))
        except ClientError as e:
            LoggerUtility.logError("Boto ClientError occurred while fetching the route tables: {}".format(e))
        except Exception as e:
            LoggerUtility.logError("Error occurred while fetching the route tables: {}".format(e))
        return routeTableList
