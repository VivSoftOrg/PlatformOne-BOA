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
""" This module will retrieve details of elastic search service. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import AWSResourceClassConstants, BotoConstants, ResourceConstants


class ElasticSearchServiceResourceFetcher(AbstractResourceFetcher):
    """ This class will retrieve details of elastic search service. """
    def __parseAndFetchResource(self, clientObject, domainName, region):
        """ This method will parse and fetch details of elastic search and domain details. """
        domainDetails = clientObject.describe_elasticsearch_domain(DomainName=domainName)['DomainStatus']
        resourceId = domainDetails['DomainId']
        resourceArn = domainDetails['ARN']
        isDomainDeleted = domainDetails['Deleted']
        tagList = clientObject.list_tags(ARN=resourceArn)['TagList']
        tags = CommonUtility.changeDictionaryKeysToLowerCase(tagList)

        configItems = {
            'resourceName': domainName,
            'tags': tags,
            'ARN': resourceArn,
            'region': region,
            'Deleted': isDomainDeleted,
            ResourceConstants.RESOURCE_TYPE_NAME: 'ElasticSearch Service'
        }

        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.ELASTICSEARCH_SERVICE, configItems=configItems)

    def resourceFetcher(self):
        domainNames = []
        try:
            awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
            regions = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)
            for region in regions:
                ESClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_ELASTICSEARCH,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )

                LoggerUtility.logInfo('Fetching Domains in region {}.'.format(region))

                response = ESClient.list_domain_names()['DomainNames']
                for domain in response:
                    domainNames.append(self.__parseAndFetchResource(ESClient, domain['DomainName'], region))

        except ValueError as e:
            LoggerUtility.logError("The content of the object you tried to assign the value is Invalid. {}".format(e))
        except AttributeError as e:
            LoggerUtility.logError("Trying to access or call an attribute of a particular object type doesn't possess. {}".format(e))
        except TypeError as e:
            LoggerUtility.logError("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
        except NameError as e:
            LoggerUtility.logError("Trying to access a variable that you have not defined properly. {}".format(e))
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
        except Exception as e:
            LoggerUtility.logError("Error occurred while fetching elastic search service list. {}".format(e))

        return domainNames
