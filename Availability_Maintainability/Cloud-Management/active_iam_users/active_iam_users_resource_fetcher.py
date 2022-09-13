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
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import BotoConstants, AWSResourceClassConstants
from active_iam_users.active_iam_users_constants import IamConstants
from common_constants.exception_constants import ExceptionMessages


class ActiveIamUsersResourceFetcher(AbstractResourceFetcher):
    """ This class is created for Fetching the resource details using Boto Client and provide the reource details to EventItem. """
    def __parseAndFetchUserDetails(self, iamUserObject):
        """Method will fetch instance details and assign it to configItems and return EventItem."""
        configItems = iamUserObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=configItems[IamConstants.IAM_USER_ID], resourceType=AWSResourceClassConstants.IAM_RESOURCE, configItems=configItems)

    def resourceFetcher(self):
        try:
            errorMessage = ''
            awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
            iamClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_IAM,
                self._AbstractResourceFetcher__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName
            )
            iamUsers = []
            response = CommonUtility.changeDictionaryKeysToLowerCase(iamClient.list_users())
            for user in response[IamConstants.IAM_USERS]:
                eventItems = self.__parseAndFetchUserDetails(user)
                iamUsers.append(eventItems)

            if response[BotoConstants.BOTO_RESPONSE_IS_TRUNCATED] is True:
                Marker = response[BotoConstants.BOTO_RESPONSE_MARKER]
                while Marker:
                    response = CommonUtility.changeDictionaryKeysToLowerCase(iamClient.list_users(Marker=Marker))
                    for user in response[IamConstants.IAM_USERS]:
                        eventItems = self.__parseAndFetchUserDetails(user)
                        iamUsers.append(eventItems)
                    if response[BotoConstants.BOTO_RESPONSE_IS_TRUNCATED] is True:
                        Marker = response[BotoConstants.BOTO_RESPONSE_MARKER]
                    else:
                        Marker = None

        except ValueError as e:
            errorMessage = ExceptionMessages.VALUE_ERROR.format(e)
        except AttributeError as e:
            errorMessage = ExceptionMessages.ATTRIBUTE_ERROR.format(e)
        except TypeError as e:
            errorMessage = ExceptionMessages.TYPE_ERROR.format(e)
        except NameError as e:
            errorMessage = ExceptionMessages.NAME_ERROR.format(e)
        except ClientError as e:
            errorMessage = ExceptionMessages.CLIENT_ERROR.format(e)
        except Exception as e:
            errorMessage = "Error occured while fetching IAM Users{}".format(e)

        if errorMessage:
            LoggerUtility.logError(errorMessage)

        return iamUsers
