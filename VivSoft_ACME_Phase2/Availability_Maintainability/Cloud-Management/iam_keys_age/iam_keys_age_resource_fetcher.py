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
""" This module will fetch users access key details. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import AWSResourceClassConstants, BotoConstants
from common.IAMConstants import IAMConstants


class IamKeysAgeResourceFetcher(AbstractResourceFetcher):
    """ This class will fetch users access key details. """
    def __parseAndFetchAccessKeysDetails(self, accessKey, userId):
        """ This method will parse key details and return userid resource type and config. """
        configItems = accessKey
        configItems['username'] = accessKey['UserName']
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=userId, resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=configItems)

    def resourceFetcher(self):
        try:
            awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
            iamClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_IAM,
                self._AbstractResourceFetcher__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName
            )
            accessKeys = []
            paginator = iamClient.get_paginator('list_users')
            for usersResponse in paginator.paginate():
                for user in usersResponse[IAMConstants.IAM_USERS]:
                    response = iamClient.list_access_keys(UserName=user[IAMConstants.IAM_USER_NAME])[IAMConstants.IAM_ACCESS_KEY_METADATA]
                    for accessKey in response:
                        accessKeyId = accessKey[IAMConstants.IAM_ACCESS_KEY_ID]
                        lastUsedKeyResponse = iamClient.get_access_key_last_used(
                            AccessKeyId=accessKey[IAMConstants.IAM_ACCESS_KEY_ID])[IAMConstants.IAM_ACCESS_LAST_USED_KEY]

                        if IAMConstants.IAM_ACCESS_LAST_USED_DATE in lastUsedKeyResponse.keys():
                            accessKey[IAMConstants.IAM_ACCESS_LAST_USED_DATE] = lastUsedKeyResponse[IAMConstants.IAM_ACCESS_LAST_USED_DATE].strftime('%Y-%m-%d')
                        else:
                            accessKey[IAMConstants.IAM_ACCESS_LAST_USED_DATE] = 'Never Used'
                        accessKeys.append(self.__parseAndFetchAccessKeysDetails(accessKey, accessKeyId))
            return accessKeys

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
            LoggerUtility.logError("Error occured while fetching IAM access key. {}".format(e))
        return False
