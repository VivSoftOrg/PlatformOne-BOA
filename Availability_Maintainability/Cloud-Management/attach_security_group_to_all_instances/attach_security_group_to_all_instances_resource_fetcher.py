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
""" This module will fetch a list of instances for attaching security groups  """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.common_utility import CommonUtility, MappingsEncoder
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import AWSResourceClassConstants, BotoConstants, EC2Constants, ManagedCloudConstants
from attach_security_group_to_all_instances.attach_security_group_to_all_instances_constants import Constants


class AttachSecurityGroupToInstancesResourceFetcher(AbstractResourceFetcher):
    """ This class will return a list of instances for attaching security groups """

    def __parseObject(self, instanceObject, allGroups):
        """ This method will parse object """
        resourceId = instanceObject[EC2Constants.EC2_INSTANCE_ID]
        configItems = instanceObject
        configItems.update({Constants.ALL_SECURITY_GROUPS: allGroups})
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.EC2_INSTANCE, configItems=configItems)

    def __getallSecurityGroupsList(self, response):
        """ This mehtod will fetch all security groups"""
        securityGroupList = []
        for securityGroup in response[Constants.SECURITY_GROUPS]:
            securityGroupList.append(securityGroup[Constants.GROUP_ID])
        return securityGroupList

    def resourceFetcher(self):
        try:
            instancesList = []
            allSecurityGroups = []
            mappings = MappingsEncoder.getMappings(self._AbstractResourceFetcher__eventParam.configParam[Constants.INPUT_MAPPINGS])
            awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName

            if mappings:
                for region in mappings:
                    LoggerUtility.logInfo("Fetching security groups in {} region".format(region))
                    ec2Client = BotoUtility.getClient(
                        BotoConstants.BOTO_CLIENT_AWS_EC2,
                        self._AbstractResourceFetcher__eventParam.accNo,
                        BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                        awsPartitionName,
                        region
                    )
                    for vpc in mappings[region]:
                        vpcFilter = [{'Name': 'vpc-id', 'Values': [vpc]}]
                        allSecurityGroups = self.__getallSecurityGroupsList(
                            CommonUtility.changeDictionaryKeysToLowerCase(
                                ec2Client.describe_security_groups(Filters=vpcFilter)))
                        paginatorResponse = ec2Client.get_paginator('describe_instances')
                        filteredResponse = paginatorResponse.paginate(Filters=Constants.FILTER_INSTANCES + vpcFilter)
                        for response_iterator in filteredResponse:
                            response = CommonUtility.changeDictionaryKeysToLowerCase(response_iterator)
                            for reservation in response[EC2Constants.EC2_RESERVATIONS]:
                                for instance in reservation[EC2Constants.EC2_INSTANCE]:
                                    instance.update({ManagedCloudConstants.REGION_REFERENCE: region})
                                    eventItems = self.__parseObject(instance, allSecurityGroups)
                                    instancesList.append(eventItems)
            else:
                LoggerUtility.logError("Mapping is not provided.")
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
            LoggerUtility.logError("Error occured while fetching instance list for attaching security group. {}".format(e))
        return instancesList
