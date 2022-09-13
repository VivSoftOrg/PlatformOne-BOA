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
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import BotoConstants, AWSResourceClassConstants, ManagedCloudConstants


class EC2ExposedInstancesResourceFetcher(AbstractResourceFetcher):
    """ This class will fetch details of instances from reservations. """

    def __parseAndFetchInstanceDetails(self, instanceObject):  # pragma: no cover
        """ This method will fetch and parse instance details """
        resourceId = instanceObject['instanceid']
        configItems = instanceObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.EC2_INSTANCE, configItems=configItems)

    def resourceFetcher(self):
        ec2InstancesList = []
        try:
            for region in self._AbstractResourceFetcher__eventParam.region:
                awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
                ec2Client = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_EC2,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )
                response = CommonUtility.changeDictionaryKeysToLowerCase(ec2Client.describe_instances())
                paginatorResponse = ec2Client.get_paginator('describe_instances')
                for response in paginatorResponse.paginate():
                    instanceResponse = CommonUtility.changeDictionaryKeysToLowerCase(response)
                    instanceReservations = instanceResponse[BotoConstants.BOTO_CLIENT_AWS_EC2_RESERVATION]
                    for reservation in instanceReservations:
                        instanceObject = reservation['instances'][0]
                        instanceObject.update({ManagedCloudConstants.REGION_REFERENCE: region})
                        eventItems = self.__parseAndFetchInstanceDetails(instanceObject)
                        ec2InstancesList.append(eventItems)

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

        return ec2InstancesList
