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
""" This module will retrieve instances from all regions. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import AWSResourceClassConstants, BotoConstants, ResourceConstants, EC2Constants, ManagedCloudConstants
from enable_delete_on_termination_ebs.enable_delete_on_termination_ebs_constants import Constants


class EnableDeleteOnTerminationEBSResourceFetcher(AbstractResourceFetcher):
    """ This class will retrieve instances from all regions. """

    def __parseAndFetchResource(self, instanceObject, region):
        """ This method will parse and fetch instances details. """
        instanceObject.update({ManagedCloudConstants.REGION_REFERENCE: region})
        resourceId = instanceObject[EC2Constants.EC2_INSTANCE_ID]
        configItems = instanceObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.EC2_INSTANCE, configItems=configItems)

    def resourceFetcher(self):
        ec2Instances = []
        errorMessage = ""
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

                LoggerUtility.logInfo('Fetching EC2 in region {}.'.format(region))
                paginatorResponse = ec2Client.get_paginator(ResourceConstants.DESCRIBE_INSTANCES_REFERENCE)
                for responsePage in paginatorResponse.paginate(Filters=Constants.FILTER_EC2):
                    response = CommonUtility.changeDictionaryKeysToLowerCase(responsePage)
                    for instances in response[EC2Constants.EC2_RESERVATIONS]:
                        for instance in instances[EC2Constants.EC2_INSTANCE]:
                            instance.update({ManagedCloudConstants.REGION_REFERENCE: region})
                            ec2Instances.append(self.__parseAndFetchResource(instance, region))

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
            errorMessage = "Error error occurred while fetching ec2 list for enabling delete on termination  {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)

        return ec2Instances
