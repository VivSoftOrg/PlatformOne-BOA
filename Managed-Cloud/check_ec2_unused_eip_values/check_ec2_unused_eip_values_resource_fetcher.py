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
""" This module will fetch all the elastic IP-addresses from all the available regions. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import AWSResourceClassConstants, BotoConstants, ResourceConstants, TagsConstants, ManagedCloudConstants
from common.common_utility import CommonUtility
from check_ec2_unused_eip_values.check_ec2_unused_eip_values_constants import Constants


class CheckEc2UnusedEIPValuesResourceFetcher(AbstractResourceFetcher):
    """ This class is responsible for fetching the resources """
    def __parseAndFetchAddressDetails(self, addressObject):
        """ This method will fetch and parse elastic IP addresses details """
        resourceId = addressObject[Constants.ALLOCATION_ID_REFERENCE]
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.EC2_EIP, configItems=addressObject)

    def resourceFetcher(self):
        addressList = []
        errorMessage = ""
        awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
        regions = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)
        try:
            for region in regions:
                ec2Client = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_EC2,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )
                LoggerUtility.logInfo('Fetching EIP in region: {}'.format(region))
                response = CommonUtility.changeDictionaryKeysToLowerCase(ec2Client.describe_addresses())
                addresses = response[Constants.RESPONSE_ADDRESSES_KEYWORD]
                for address in addresses:
                    addressObject = address
                    tags = CommonUtility.changeDictionaryKeysToLowerCase(ec2Client.describe_tags(
                        Filters=[
                            {
                                BotoConstants.BOTO_CLIENT_AWS_EC2_NAME: ResourceConstants.RESOURCE_ID_REFERNCE,
                                BotoConstants.BOTO_CLIENT_AWS_EC2_VALUES: [addressObject[Constants.ALLOCATION_ID_REFERENCE]]
                            }
                        ]
                    ))
                    addressObject.update({ManagedCloudConstants.REGION_REFERENCE: region})
                    addressObject.update({TagsConstants.EC2_INSTANCE_TAGS: tags[TagsConstants.EC2_INSTANCE_TAGS]})
                    eventItems = self.__parseAndFetchAddressDetails(addressObject)
                    addressList.append(eventItems)

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
            errorMessage = "Error occured while {}".format(e)
        if errorMessage:
            LoggerUtility.logError(errorMessage)

        return addressList
