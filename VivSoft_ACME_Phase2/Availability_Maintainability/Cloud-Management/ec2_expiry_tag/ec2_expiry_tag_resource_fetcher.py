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
""" This module is used to fetch all the EC2 instances present in available regions """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import AWSResourceClassConstants, EC2Constants, BotoConstants, ResourceConstants, ManagedCloudConstants


class Ec2ExpiryTagFetcher(AbstractResourceFetcher):
    """ This class is responsible for fetching the resources """

    def __parseAndFetchInstanceDetails(self, instanceObject):
        """ This method is used to fetch and parse EC2 instance details """
        resourceId = instanceObject[EC2Constants.EC2_INSTANCE_ID]
        configItems = instanceObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.EC2_INSTANCE, configItems=configItems)

    def resourceFetcher(self):
        ec2InstancesList = []
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
                LoggerUtility.logInfo('Fetching Instances in region: {}'.format(region))
                paginatorResponse = ec2Client.get_paginator(ResourceConstants.DESCRIBE_INSTANCES_REFERENCE)
                for response in paginatorResponse.paginate(Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped', 'pending']}]):
                    instanceResponse = CommonUtility.changeDictionaryKeysToLowerCase(response)
                    instanceReservations = instanceResponse[EC2Constants.EC2_RESERVATIONS]
                    for reservation in instanceReservations:
                        instanceObject = reservation[EC2Constants.EC2_INSTANCE][0]
                        instanceObject.update({ManagedCloudConstants.REGION_REFERENCE: region})
                        instanceObject.update({ResourceConstants.RESOURCE_TYPE_NAME: 'Ec2 Instance'})
                        eventItems = self.__parseAndFetchInstanceDetails(instanceObject)
                        ec2InstancesList.append(eventItems)

        except ValueError as e:
            LoggerUtility.logError("The content of the object you tried to assign the value is Invalid. {}".format(e))
        except AttributeError as e:
            LoggerUtility.logError("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
        except TypeError as e:
            LoggerUtility.logError("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
        except NameError as e:
            LoggerUtility.logError("Trying to access a variable that you have not defined properly. {}".format(e))
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
        except Exception as e:
            LoggerUtility.logError("Error occured while fetching for EC2 instance list for  ec2_expiray_tag rule. {}".format(e))

        return ec2InstancesList
