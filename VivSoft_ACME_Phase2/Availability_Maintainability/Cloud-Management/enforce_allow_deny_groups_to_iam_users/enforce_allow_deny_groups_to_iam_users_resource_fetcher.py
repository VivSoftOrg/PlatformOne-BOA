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
""" This mmodule will fetch users details. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.logger_utility import LoggerUtility
from common.common_constants import AWSResourceClassConstants, BotoConstants
from active_iam_users.active_iam_users_constants import IamConstants


class EnforceAllowAndDenyGroupsResourceFetcher(AbstractResourceFetcher):
    """ This class will fetch and parse users id and details. """
    def __parseAndFetchUserDetails(self, iamUserObject):
        """ This method will parse and fetch users id and  details. """
        configItems = iamUserObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=iamUserObject[IamConstants.IAM_USER_ID], resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=configItems)

    def resourceFetcher(self):
        """ This method will fetch users details."""
        iamUsers = []
        try:
            awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
            iamClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_IAM,
                self._AbstractResourceFetcher__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName
            )
            for paginatorResponse in iamClient.get_paginator('list_users').paginate():
                response = CommonUtility.changeDictionaryKeysToLowerCase(paginatorResponse)
                for user in response[IamConstants.IAM_USERS]:
                    eventItems = self.__parseAndFetchUserDetails(user)
                    iamUsers.append(eventItems)

                if response[BotoConstants.BOTO_RESPONSE_IS_TRUNCATED]:
                    Marker = response[BotoConstants.BOTO_RESPONSE_MARKER]
                    while Marker:
                        response = CommonUtility.changeDictionaryKeysToLowerCase(iamClient.list_users(Marker=Marker))
                        for user in response[IamConstants.IAM_USERS]:
                            eventItems = self.__parseAndFetchUserDetails(user)
                            iamUsers.append(eventItems)
                        if response[BotoConstants.BOTO_RESPONSE_IS_TRUNCATED]:
                            Marker = response[BotoConstants.BOTO_RESPONSE_MARKER]
                        else:
                            Marker = None

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
            LoggerUtility.logError("Error occurred while fetching iamUsers list for enforce allow deny group to iamUsers. {}".format(e))

        return iamUsers
