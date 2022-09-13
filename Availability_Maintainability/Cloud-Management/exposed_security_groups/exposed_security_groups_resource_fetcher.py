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
""" This module will fetch details of instances from reservations.  """
from botocore.exceptions import ClientError

from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.boto_utility import BotoUtility
from common.common_constants import AWSResourceClassConstants, BotoConstants, ManagedCloudConstants
from common.common_utility import CommonUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.logger_utility import LoggerUtility


class ExposedSecurityGroupsResourceFetcher(AbstractResourceFetcher):
    """ This class will fetch details of instances from reservations. """

    def __parseAndFetchInstanceDetails(self, groupObject):
        """ This method will fetch and parse instance details """
        resourceId = groupObject['groupid']
        configItems = groupObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.SG_RESOURCE, configItems=configItems)

    def resourceFetcher(self):
        securityGroupList = []
        groupObject = {}
        try:
            awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
            regions = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)
            for region in regions:
                LoggerUtility.logInfo('Fetching Security groups in region: {}'.format(region))
                ec2Client = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_EC2,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )
                paginatorResponse = ec2Client.get_paginator('describe_security_groups')
                for response in paginatorResponse.paginate():
                    groupResponse = CommonUtility.changeDictionaryKeysToLowerCase(response)
                    for group in groupResponse['securitygroups']:
                        groupObject = group
                        groupObject.update({ManagedCloudConstants.REGION_REFERENCE: region})
                        eventItems = self.__parseAndFetchInstanceDetails(groupObject)
                        securityGroupList.append(eventItems)

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
            LoggerUtility.logError("Error occurred while fetching for ec2 list for ec2 exposed instances. {}".format(e))

        return securityGroupList
