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
"""This module will perform action if the Evaluation Result is non_compliant."""
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.i18n import Translation as _
from common.framework_objects import EvaluationResult
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants, ComplianceConstants, ActionMessages
from active_iam_users.active_iam_users_constants import IamConstants
from common_constants.exception_constants import ExceptionMessages


class ActiveIamUsersAction(AbstractAction):
    """This class perform action if the resource is non_compliant as per the standards """

    def __disableConsoleAccess(self, iamClient, userName):
        ''' Function to diable console access for user if it is enabled '''
        try:
            response = iamClient.delete_login_profile(UserName=userName)
            requestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]

            if requestStatus == 200:
                infoMessage = "Console access is disabled for the user."
                LoggerUtility.logInfo(infoMessage)
                return True, infoMessage
            else:
                errorMessage = ActionMessages.RESOURCE_ACTION_ERROR_MESSAGE.format('deleting login profile of', 'user', userName, requestStatus)  # noqa
                LoggerUtility.logError(errorMessage)
                return False, errorMessage

        except Exception as expMsg:
            exceptionMessage = 'Exception occured {} while deleting login profile of {} IAM user.'.format(expMsg, userName)
            LoggerUtility.logError(exceptionMessage)
            return False, exceptionMessage

    def __deleteUser(self, passwordDisabled, iamClient, userName):
        ''' function to delete iam user '''
        try:
            iamClient.get_user(UserName=userName)

            accesskeymetadata = iamClient.list_access_keys(UserName=userName)[
                'AccessKeyMetadata']
            for accessKey in accesskeymetadata:
                accessKeyId = accessKey.get("AccessKeyId")
                iamClient.delete_access_key(
                    UserName=userName,
                    AccessKeyId=accessKeyId)

            policyList = iamClient.list_attached_user_policies(
                UserName=userName)['AttachedPolicies']
            for policy in policyList:
                iamClient.detach_user_policy(
                    UserName=userName, PolicyArn=policy['PolicyArn'])

            groupList = iamClient.list_groups_for_user(
                UserName=userName)['Groups']
            for group in groupList:
                iamClient.remove_user_from_group(
                    GroupName=group['GroupName'], UserName=userName)

            signingCertificateList = iamClient.list_signing_certificates(
                UserName=userName)['Certificates']
            for certificate in signingCertificateList:
                iamClient.delete_signing_certificate(
                    CertificateId=certificate['CertificateId'], UserName=userName)

            sshPublicKeys = iamClient.list_ssh_public_keys(
                UserName=userName)['SSHPublicKeys']
            for keys in sshPublicKeys:
                iamClient.delete_ssh_public_key(
                    SSHPublicKeyId=keys['SSHPublicKeyId'], UserName=userName)

            mfaDevices = iamClient.list_mfa_devices(UserName=userName)['MFADevices']
            for mfa in mfaDevices:
                iamClient.deactivate_mfa_device(UserName=userName, SerialNumber=mfa['SerialNumber'])

            if not passwordDisabled:
                self.__disableConsoleAccess(iamClient, userName)

            response = iamClient.delete_user(UserName=userName)

            requestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]
            if requestStatus == 200:
                infoMessage = "User account is deleted."
                LoggerUtility.logInfo(infoMessage)
                return True, infoMessage
            else:
                errorMessage = ActionMessages.RESOURCE_ACTION_ERROR_MESSAGE.format('deleting', 'user', userName, requestStatus)
                LoggerUtility.logError(errorMessage)
                return False, errorMessage

        except Exception as expMsg:
            exceptionMessage = 'Exception occured {} while deleting the user {}'.format(expMsg, userName)
            LoggerUtility.logError(exceptionMessage)
            return False, exceptionMessage

    def performAction(self, eventItem):
        evaluationResult = EvaluationResult()
        exceptionMessage = ''
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            iamClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_IAM,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName
            )
            userName = eventItem.configItems[IamConstants.IAM_USER_NAME]

            if eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == IamConstants.IAM_USER_DELETE:
                userDeleted, responseMessage = self.__deleteUser(passwordDisabled=eventItem.configItems[IamConstants.IAM_USER_HAS_PASSWORD_DISABLED], iamClient=iamClient, userName=userName)
                if userDeleted:
                    self._AbstractAction__actionMessage = _(responseMessage)
                    evaluationResult.annotation = _("IAM User account is deleted successfully for {}.".format(userName))
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                else:
                    self._AbstractAction__actionMessage = _(responseMessage)
                    evaluationResult.annotation = _("Failed to delete IAM User account for user {}.".format(userName))
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == IamConstants.IAM_USER_DELETE_WARNINGS:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                if eventItem.configItems[IamConstants.IAM_USER_HAS_PASSWORD_DISABLED]:
                    evaluationResult.annotation = _("User {} does not have login profile enabled.".format(userName))
                    self._AbstractAction__actionMessage = "None"
                    LoggerUtility.logInfo(evaluationResult.annotation)
                else:
                    disabledConsoleAccess, responseMessage = self.__disableConsoleAccess(iamClient, userName)
                    if disabledConsoleAccess:
                        evaluationResult.annotation = _("Console access is disabled successfully for user {}.".format(userName))
                        self._AbstractAction__actionMessage = _(responseMessage)
                    else:
                        evaluationResult.annotation = _("Failed to disable Console access for user {}.".format(userName))
                        self._AbstractAction__actionMessage = _(responseMessage)

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == IamConstants.IAM_USER_DISABLE_WARNINGS:
                self._AbstractAction__actionMessage = "None"
                LoggerUtility.logInfo("IAM User account for {} will be disabled soon.".format(userName))
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("IAM User account for {} will be disabled soon.".format(userName))

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
            exceptionMessage = "Error occured while deleting User profile. {}".format(e)

        if exceptionMessage != '':
            LoggerUtility.logError(exceptionMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(exceptionMessage)
            self._AbstractAction__actionMessage = _(exceptionMessage)

        return evaluationResult
