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
""" This module revokes the iam user who has excess permissions """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.common_utility import CommonUtility
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants, ComplianceConstants
from common.framework_objects import EvaluationResult
from common.common_constants import ActionMessages
from common_constants.exception_constants import ExceptionMessages
from iam_roles_excess_permissions.iam_roles_excess_permissions_constants import IamConstants


class IamRolesAccessPermissionsAction(AbstractAction):
    """This class perform action as it stop Instances if it is non_compliant """

    def __deleteRole(self, iamClient, roleName):
        """ This method is used to delete role """
        try:
            errorWhileDeletingRole = ""
            response = iamClient.delete_role(RoleName=roleName)
            requestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]
            if requestStatus == 200:
                infoMessage = "IAM Role Deleted."
                LoggerUtility.logInfo(infoMessage)
            else:
                errorWhileDeletingRole = ActionMessages.RESOURCE_ACTION_ERROR_MESSAGE.format('deleting', 'IAM role', roleName, requestStatus)

        except Exception as e:
            errorWhileDeletingRole = _("Exception occurred while deleting the IAM Role {}".format(e))

        return errorWhileDeletingRole

    def __deleteInstanceProfile(self, iamClient, instanceProfileName):
        """ This method is used to delete instance profile """
        returnValue = False
        try:
            response = iamClient.delete_instance_profile(InstanceProfileName=instanceProfileName)
            requestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]

            if requestStatus == 200:
                LoggerUtility.logInfo("Instance Profile '{}' deleted".format(instanceProfileName))
                returnValue = True
            else:
                LoggerUtility.logError(ActionMessages.RESOURCE_ACTION_ERROR_MESSAGE.format('deleting', 'IAM Instance Profile', instanceProfileName, requestStatus))

        except Exception as e:
            LoggerUtility.logError(e)
            self._AbstractAction__actionMessage = _("Exception occurred while deleting the Instance profile {}".format(instanceProfileName))
        return returnValue

    def __detachRolesFromInstanceProfile(self, iamClient, instanceProfile):
        """ This method is used to detach roles from Instance Profile """
        errorWhileDetatchingAnyRole = False
        try:
            for role in instanceProfile[IamConstants.IAM_ROLES]:
                iamClient.remove_role_from_instance_profile(
                    InstanceProfileName=instanceProfile[IamConstants.INSTANCE_PROFILE_NAME],
                    RoleName=role[IamConstants.ROLE_NAME])
        except Exception as e:
            errorWhileDetatchingAnyRole = True
            LoggerUtility.logError("Error occoured while detaching roles from instance profile {}".format(e))

        return errorWhileDetatchingAnyRole

    def __detachManagedPolicies(self, iamClient, eventItem):
        """ This method is used to detach Managed Policies """
        errorWhileDetatchingAnyPolicy = ""
        for policy in eventItem.configItems[IamConstants.AWS_MANAGED_POLICIES]:
            try:
                iamClient.detach_role_policy(RoleName=eventItem.configItems[IamConstants.ROLE_NAME], PolicyArn=policy[IamConstants.POLICY_ARN])
            except Exception as e:
                errorWhileDetatchingAnyPolicy = "Error occoured while detaching manged policies {}.".format(e)

        return errorWhileDetatchingAnyPolicy

    def __deleteInlinePolicies(self, iamClient, roleName, inlinePolicies):
        """ This method is used to delete Inline Policies """
        errorWhileDeletingAnyPolicies = ""
        for policyName in inlinePolicies:
            try:
                iamClient.delete_role_policy(RoleName=roleName, PolicyName=policyName)
            except Exception as e:
                errorWhileDeletingAnyPolicies = "Error occoured while deleting inline policies {}".format(e)

        return errorWhileDeletingAnyPolicies

    def performAction(self, eventItem):
        try:
            errorMessage = ""
            infoMessage = ""
            errorDetachPolicyResponse = ""
            errorDeletePolicyResponse = ""
            evaluationResult = EvaluationResult()
            iamClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_IAM,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                self._AbstractAction__eventParam.awsPartitionName
            )

            roleName = eventItem.configItems[IamConstants.ROLE_NAME]
            inlinePolicies = eventItem.configItems[IamConstants.INLINE_POLICIES]
            paginator = iamClient.get_paginator('list_instance_profiles_for_role')
            operation_parameters = {"RoleName": roleName}
            page_iterator = paginator.paginate(**operation_parameters)
            for page in page_iterator:
                for instanceProfile in page[IamConstants.INSTANCE_PROFILES]:
                    instanceProfile = CommonUtility.changeDictionaryKeysToLowerCase(instanceProfile)
                    self.__detachRolesFromInstanceProfile(iamClient, instanceProfile)
                    self.__deleteInstanceProfile(iamClient, instanceProfile[IamConstants.INSTANCE_PROFILE_NAME])

            errorDetachPolicyResponse = self.__detachManagedPolicies(iamClient, eventItem)
            errorDeletePolicyResponse = self.__deleteInlinePolicies(iamClient, roleName, inlinePolicies)

            if not errorDetachPolicyResponse and not errorDeletePolicyResponse:
                errorDeleteIamRole = self.__deleteRole(iamClient, roleName)
                if errorDeleteIamRole:
                    errorMessage = errorDeleteIamRole
                else:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = "IAM Role successfully deleted"

            else:
                errorMessage = "IAM role not deleted because error occured while remove all the policies attached to the role - {}  {}.".format(errorDetachPolicyResponse, errorDeletePolicyResponse)

        except AttributeError as e:
            errorMessage = ExceptionMessages.ATTRIBUTE_ERROR.format(e)
        except TypeError as e:
            errorMessage = ExceptionMessages.TYPE_ERROR.format(e)
        except NameError as e:
            errorMessage = ExceptionMessages.NAME_ERROR.format(e)
        except ClientError as e:
            errorMessage = ExceptionMessages.CLIENT_ERROR.format(e)
        except Exception as e:
            errorMessage = "Error occured while performing action for IAM roles execess permissions rule {}".format(e)

        if errorMessage:
            LoggerUtility.logError(errorMessage)
            evaluationResult.annotation = errorMessage
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION

        self._AbstractAction__actionMessage = evaluationResult.annotation
        return evaluationResult
