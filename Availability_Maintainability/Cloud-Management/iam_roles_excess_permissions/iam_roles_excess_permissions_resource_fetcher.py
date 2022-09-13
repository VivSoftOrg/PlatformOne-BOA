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
""" This module fetches the iam user list """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import BotoConstants, AWSResourceClassConstants
from common_constants.exception_constants import ExceptionMessages
from iam_roles_excess_permissions.iam_roles_excess_permissions_constants import IamConstants


class IamRolesAccessPermissionsResourceFetcher(AbstractResourceFetcher):
    """ This class is responsible for fetching the resources """

    def __parseAndFetchUserDetails(self, iamRoleObject):
        """ This method is used to fetch and parse IAM roles details """
        configItems = iamRoleObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=iamRoleObject[IamConstants.ROLE_ID], resourceType=AWSResourceClassConstants.IAM_ROLE, configItems=configItems)

    def resourceFetcher(self):
        errorMessage = ""
        try:
            iamClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_IAM,
                self._AbstractResourceFetcher__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                self._AbstractResourceFetcher__eventParam.awsPartitionName
            )
            iamRoles = []
            LoggerUtility.logInfo("Fetching of IAM roles started")
            paginator = iamClient.get_paginator('list_roles')
            for paginatorResponse in paginator.paginate():
                response = CommonUtility.changeDictionaryKeysToLowerCase(paginatorResponse)
                for role in response[IamConstants.IAM_ROLES]:
                    eventItems = self.__parseAndFetchUserDetails(role)
                    iamRoles.append(eventItems)

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
            errorMessage = "Error occured while fetching roles for rule - IAM roles execess permission {}".format(e)

        if not iamRoles:
            LoggerUtility.logInfo("No IAM roles found")
        if errorMessage:
            LoggerUtility.logError(errorMessage)

        return iamRoles
