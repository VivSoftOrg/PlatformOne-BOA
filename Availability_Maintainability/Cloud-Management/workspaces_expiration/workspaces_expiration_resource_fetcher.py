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
from common.common_constants import BotoConstants, ResourceConstants, AWSResourceClassConstants
from workspaces_expiration.workspaces_expiration_constants import Constants


class WorkSpacesResourceFetcher(AbstractResourceFetcher):
    """ This class is created for Fetching the resource details using Boto Client and provide the reource details to EventItem. """

    def __parseAndFetchResource(self, clientObject, workspaceDetails, region):
        """Method will fetch instance details and assign it to configItems."""
        resourceId = workspaceDetails['WorkspaceId']
        bundleId = workspaceDetails['BundleId']
        bundleName = clientObject.describe_workspace_bundles(BundleIds=[bundleId])['Bundles'][0]['Name']
        workspaceState = workspaceDetails['State']
        tagList = clientObject.describe_tags(ResourceId=resourceId)['TagList']

        configItems = {
            'resourceName': bundleName,
            'Tags': tagList,
            'region': region,
            'State': workspaceState,
            ResourceConstants.RESOURCE_TYPE_NAME: Constants.RESOURCE_NAME
        }

        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.WORKSPACES_RESOURCE, configItems=configItems)

    def resourceFetcher(self):
        workspacesList = []
        errorMessage = ""
        try:
            awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
            regions = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)
            for region in regions:
                try:
                    WSClient = BotoUtility.getClient(
                        BotoConstants.BOTO_CLIENT_AWS_WORKSPACE,
                        self._AbstractResourceFetcher__eventParam.accNo,
                        BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                        awsPartitionName,
                        region
                    )

                    LoggerUtility.logInfo('Fetching Workspaces in region {}.'.format(region))

                    response = WSClient.describe_workspaces()[Constants.RESOURCE_NAME.capitalize()]
                    for workspace in response:
                        workspacesList.append(self.__parseAndFetchResource(WSClient, workspace, region))
                except Exception as e:
                    LoggerUtility.logWarning(e)

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
            errorMessage = "Error occured while fetching Workspaces. {}".format(e)
        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
        return workspacesList
