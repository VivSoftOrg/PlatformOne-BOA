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
"""This module will perform action based on the Evaluation Result."""
from datetime import datetime

from botocore.exceptions import ClientError
from dateutil.relativedelta import relativedelta

from common.abstract_action import AbstractAction
from common.boto_utility import BotoUtility
from common.common_constants import BotoConstants, ComplianceConstants
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common_constants.exception_constants import ExceptionMessages


class CheckIamMfaAction(AbstractAction):
    """This class perform action if resource is non_compliant """

    def __disableLoginProfile(self, iamClient):
        """method for disabling Login profile if it exist."""
        try:
            responseLoginProfile = iamClient.delete_login_profile(
                UserName=self.__userName
            )
            if responseLoginProfile['ResponseMetadata']['HTTPStatusCode'] == 200:
                LoggerUtility.logInfo("Deleted Login profile of user %s" % self.__eventItem.configItems['username'])
                return True
            else:
                LoggerUtility.logInfo("Could not delete login profile of user %s ." % self.__eventItem.configItems['username'])
                return False

        except ClientError as e:
            LoggerUtility.logError(ExceptionMessages.CLIENT_ERROR.format(e))
            return False

        except Exception as e:
            LoggerUtility.logError("Error occured while disabling login profile. {}".format(e))
            return False

    def __disableAccessKeys(self, iamClient):
        """Method for dissabling Access keys."""
        for accessKey in iamClient.list_access_keys(UserName=self.__eventItem.configItems['username'])['AccessKeyMetadata']:
            try:
                responseDeleteAccessKey = iamClient.update_access_key(
                    UserName=self.__userName,
                    AccessKeyId=accessKey['AccessKeyId'],
                    Status='Inactive'
                )
                if responseDeleteAccessKey['ResponseMetadata']['HTTPStatusCode'] == 200:
                    LoggerUtility.logInfo("Access Keys disabled for {}.".format(self.__eventItem.configItems['username']))
                    return True
                else:
                    LoggerUtility.logInfo("Unable to disable Access keys for {}.".format(self.__eventItem.configItems['username']))
                    return False

            except ClientError as e:
                LoggerUtility.logError(ExceptionMessages.CLIENT_ERROR.format(e))
                return False
            except Exception as e:
                LoggerUtility.logError("Error occured while disabling access keys for {}: {}".format(self.__eventItem.configItems['username'], e))
                return False

    def __processAllActions(self, evaluationResult):
        ''' Function to process all the actions '''
        awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
        iamClient = BotoUtility.getClient(
            BotoConstants.BOTO_CLIENT_AWS_IAM,
            self._AbstractAction__eventParam.accNo,
            BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
            awsPartitionName
        )
        disabledLogInProfile = self.__disableLoginProfile(iamClient)
        disabledAccessKeys = self.__disableAccessKeys(iamClient)

        if disabledAccessKeys and disabledLogInProfile:
            self._AbstractAction__actionMessage = _("To ensure the AWS environment is compliant to the defined standards, AWS Console Access and Access Keys are disabled for the IAM user.")
            evaluationResult.annotation = _("AWS Console Access and Access Keys are disabled for the IAM user.")
            evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE

        else:
            self._AbstractAction__actionMessage = _("Unable to disable AWS Console Access and Access Keys for the IAM user.")
            evaluationResult.annotation = self._AbstractAction__actionMessage
            evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE

        return evaluationResult

    def performAction(self, eventItem):
        evaluationResult = EvaluationResult()
        errorMessage = ""
        self._AbstractAction__actionMessage = _("")
        self.__eventItem = eventItem
        self.__userName = self._CheckIamMfaAction__eventItem.configItems['username']

        try:
            createDate = eventItem.configItems['CreateDate'].strftime("%Y-%m-%d")
            requiredDate = (datetime.now() - relativedelta(days=3)).strftime("%Y-%m-%d")
            deactivationDate = eventItem.configItems.get('DeactivationDate', None)
            userNew = 'No' if requiredDate >= createDate else 'Yes'

            if deactivationDate is None or userNew == 'Yes':
                if requiredDate >= createDate:
                    evaluationResult = self.__processAllActions(evaluationResult)
                else:
                    self._AbstractAction__actionMessage = _("None")
                    LoggerUtility.logInfo("User: {} is new and have MFA disbaled".format(self.__userName))
                    evaluationResult.annotation = _("User is new and have MFA disabled")
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
            else:
                if requiredDate >= deactivationDate:
                    evaluationResult = self.__processAllActions(evaluationResult)
                else:
                    self._AbstractAction__actionMessage = _("None")
                    LoggerUtility.logInfo("User {} does not have MFA enabled".format(self.__userName))
                    evaluationResult.annotation = _("User does not have MFA enabled")
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE

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
            errorMessage = "Error occured while deleting User Profile and deactivating Access Keys: {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            self._AbstractAction__actionMessage = errorMessage
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)

        return evaluationResult
