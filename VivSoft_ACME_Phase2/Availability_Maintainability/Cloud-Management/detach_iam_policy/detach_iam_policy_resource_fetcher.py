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
""" This module will fetch the resource details. """
from botocore.exceptions import ClientError

from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.boto_utility import BotoUtility
from common.common_constants import AWSResourceClassConstants, BotoConstants
from common.compliance_object_factory import ComplianceObjectFactory
from common.logger_utility import LoggerUtility


class DetachIamPolicyResourceFetcher(AbstractResourceFetcher):
    """ This class is created for Fetching the resource details using Boto Client and provide the reource details to EventItem. """

    def __parseAndFetchUserDetails(self, instanceObject):
        """Method will fetch instance details and assign it to configItems."""
        configItems = instanceObject
        configItems['username'] = instanceObject['UserName']
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=instanceObject['UserId'], resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=configItems)

    def resourceFetcher(self):
        """ This mehtod will fetch all IAM user"""
        users = []
        errorMessage = ""
        try:
            awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
            iamClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_IAM,
                self._AbstractResourceFetcher__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName
            )
            paginator = iamClient.get_paginator('list_users')
            for usersResponse in paginator.paginate():
                for user in usersResponse['Users']:
                    eventItems = self.__parseAndFetchUserDetails(user)
                    users.append(eventItems)

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is Invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while {}".format(e)
        if errorMessage != "":
            LoggerUtility.logError(errorMessage)

        return users
