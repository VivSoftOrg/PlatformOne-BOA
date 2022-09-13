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
""" This module will fetch the EC2 Instance resource details and send it to Evaluator.  """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import BotoConstants, AWSResourceClassConstants, ManagedCloudConstants


class StopInstancesOverWeekendResourceFetcher(AbstractResourceFetcher):
    """ This class is created for Fetching the resource details using Boto Client and provide the reource details to EventItem. """

    def __parseAndFetchInstanceDetails(self, instanceObject):
        """Method will fetch instance details and assign it to configItems."""
        resourceId = instanceObject["instanceid"]
        configItems = instanceObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.EC2_INSTANCE, configItems=configItems)

    def resourceFetcher(self):
        ec2InstancesList = []
        awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
        regions = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)
        for region in regions:
            try:
                ec2Client = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_EC2,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )
                LoggerUtility.logInfo('Fetching Instances in region: {}'.format(region))
                paginatorResponse = ec2Client.get_paginator('describe_instances')
                for response in paginatorResponse.paginate(Filters=[{'Name': BotoConstants.BOTO_CLIENT_AWS_EC2_INSTANCE_STATE_NAME,
                                                                     'Values': [BotoConstants.BOTO_CLIENT_AWS_EC2_RUNNING_STATE]}]):
                    instanceResponse = CommonUtility.changeDictionaryKeysToLowerCase(response)
                    instanceReservations = instanceResponse[BotoConstants.BOTO_CLIENT_AWS_EC2_RESERVATION]
                    for reservation in instanceReservations:
                        instanceObject = reservation[BotoConstants.BOTO_CLIENT_AWS_EC2_INSTANCES][0]
                        instanceObject.update({ManagedCloudConstants.REGION_REFERENCE: region})
                        eventItems = self.__parseAndFetchInstanceDetails(instanceObject)
                        ec2InstancesList.append(eventItems)
            except ValueError as e:
                LoggerUtility.logError("The content of the object you tried to assign the value is Invalid. {}".format(e))
                return False
            except AttributeError as e:
                LoggerUtility.logError("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
                return False
            except TypeError as e:
                LoggerUtility.logError("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
                return False
            except NameError as e:
                LoggerUtility.logError("Trying to access a variable that you have not defined properly. {}".format(e))
                return False
            except ClientError as e:
                LoggerUtility.logError("Boto client error occured. {}".format(e))
                return False
            except Exception as e:
                LoggerUtility.logError("Error occured while fetching EC2 Instances. {}".format(e))
                return False

        return ec2InstancesList
