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
""" This module will retrieve details of cloudfronts. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.common_utility import CommonUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import BotoConstants, AWSResourceClassConstants
from cloudfront_distribution_expiration.cloudfront_distribution_expiration_constants import Constants


class CloudFrontDistributionResourceFetcher(AbstractResourceFetcher):
    """ This class will retrieve details of cloudfronts. """
    __webDistributionReference = {
        'DistributionType': Constants.WEB_DISTRIBUTION_TYPE_REFERENCE,
        'ConfigType': Constants.WEB_DISTRIBUTION_CONFIG_REFERENCE,
        'WaiterType': Constants.WEB_DISTRIBUTION_WAITER_TYPE,
        'ListFunction': Constants.WEB_DISTRIBUTION_LIST_FUNCTION,
        'GetConfigFunction': Constants.WEB_DISTRIBUTION_GET_CONFIG_FUNCTION,
        'UpdateFunction': Constants.WEB_DISTRIBUTION_UPDATE_FUNCTION,
        'DeleteFunction': Constants.WEB_DISTRIBUTION_DELETE_FUNCTION
    }

    __StreamingDistributionReference = {
        'DistributionType': Constants.STREAMING_DISTRIBUTION_TYPE_REFERENCE,
        'ConfigType': Constants.STREAMING_DISTRIBUTION_CONFIG_REFERENCE,
        'WaiterType': Constants.STREAMING_DISTRIBUTION_WAITER_TYPE,
        'ListFunction': Constants.STREAMING_DISTRIBUTION_LIST_FUNCTION,
        'GetConfigFunction': Constants.STREAMING_DISTRIBUTION_GET_CONFIG_FUNCTION,
        'UpdateFunction': Constants.STREAMING_DISTRIBUTION_UPDATE_FUNCTION,
        'DeleteFunction': Constants.STREAMING_DISTRIBUTION_DELETE_FUNCTION
    }

    def __parseAndFetchResource(self, clientObject, distribution, resourceReference):
        """ This method will parse and fetch distribution details. """
        resourceId = distribution['Id']
        configItems = distribution
        tagList = CommonUtility.changeDictionaryKeysToLowerCase(clientObject.list_tags_for_resource(Resource=distribution['ARN'])['Tags']['Items'])
        configItems.update({'tags': tagList})
        configItems.update(resourceReference)

        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.CLOUDFRONT_DISTRIBUTION, configItems=configItems)

    def __getDistributionList(self, clientObject, resourceReference):
        """ This method will retrieve distribution list. """
        resourceList = []

        paginator = clientObject.get_paginator(resourceReference['ListFunction'])

        for page in paginator.paginate():
            response = page[resourceReference['DistributionType']]

            if 'Items' not in response:
                return []

            for distribution in response['Items']:
                resourceList.append(self.__parseAndFetchResource(clientObject, distribution, resourceReference))

            while response['IsTruncated']:
                response = getattr(clientObject, 'ListFunction')(Marker=response['Marker'])[resourceReference['DistributionType']]
                for distribution in response['Items']:
                    resourceList.append(self.__parseAndFetchResource(clientObject, distribution, resourceReference))

        return resourceList

    def resourceFetcher(self):
        distributionList = []
        errorMessage = ""
        try:
            awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
            CFClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_CLOUDFRONT,
                self._AbstractResourceFetcher__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName
            )

            LoggerUtility.logInfo('Fetching Distributions.')

            distributionList += self.__getDistributionList(CFClient, self.__webDistributionReference)

            distributionList += self.__getDistributionList(CFClient, self.__StreamingDistributionReference)

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
            errorMessage = "Error occurred while fetching cloudfront list. {}".format(e)

        if errorMessage:
            LoggerUtility.logError(errorMessage)

        return distributionList
