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
""" This module will fetch EC2 instances present in all the available regions. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.common_utility import CommonUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import AWSResourceClassConstants
from common.common_constants import BotoConstants
from common.common_constants import ResourceConstants
from ec2_noshutdown_tag.ec2_noshutdown_tag_constants import NoShutDownTagConstants


class Ec2NoshutdownTagFetcher(AbstractResourceFetcher):
    """ This class is responsible for fetching the resources """
    def __parseAndFetchInstanceDetails(self, instanceObject):
        """ This method will be used fetch and parse ec2 instance details. """
        resourceId = instanceObject[NoShutDownTagConstants.EC2_INSTANCE_ID]
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
                paginatorResponse = ec2Client.get_paginator(ResourceConstants.DESCRIBE_INSTANCES_REFERENCE)
                for response in paginatorResponse.paginate(Filters=[
                        {
                            NoShutDownTagConstants.NAME_KEYWORD: NoShutDownTagConstants.INSTANCE_STATE_NAME,
                            NoShutDownTagConstants.VALUES_KEYWORD: [NoShutDownTagConstants.RUNNING_KEYWORD, NoShutDownTagConstants.STOPPED_KEYWORD]
                        }
                    ]):  # noqa
                    instanceResponse = CommonUtility.changeDictionaryKeysToLowerCase(response)
                    instanceReservations = []

                    if instanceResponse.__contains__(NoShutDownTagConstants.EC2_RESERVATION_KEYWORD):
                        instanceReservations = instanceResponse[NoShutDownTagConstants.EC2_RESERVATION_KEYWORD]

                    for reservation in instanceReservations:
                        instanceObject = reservation[NoShutDownTagConstants.EC2_INSTANCES_KEYWORD][0]
                        instanceObject.update({NoShutDownTagConstants.REGION_KEYWORD: region})
                        eventItems = self.__parseAndFetchInstanceDetails(instanceObject)
                        ec2InstancesList.append(eventItems)

        except AttributeError as e:
            LoggerUtility.logError("AttributeError occurred while fetching EC2 instances")
        except KeyError as e:
            LoggerUtility.logError("KeyError occurred while fetching EC2 instances")
        except ValueError as e:
            LoggerUtility.logError("ValueError occurred while fetching EC2 instances")
        except ClientError as e:
            LoggerUtility.logError("Boto ClientError occurred while fetching EC2 instances")
        except Exception as e:
            LoggerUtility.logError("Error occurred while fetching EC2 instances")
        return ec2InstancesList
