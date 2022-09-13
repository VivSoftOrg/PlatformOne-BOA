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
"""This module will Evaluate the Rule and mark resource as compliant or non_Compliant based on behaviour."""
from botocore.exceptions import ClientError

from common.abstract_evaluate import AbstractEvaluator
from common.boto_utility import BotoUtility
from common.common_constants import (BotoConstants, ComplianceConstants,
                                     TagsConstants)
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common_constants.exception_constants import ExceptionMessages


class CheckIamMfaEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """

    def __hasPassword(self, iamClient, userName):
        """Method checks whether the  user has password or not"""
        hasPassword = False
        try:
            loginProfile = iamClient.get_login_profile(UserName=userName)
            if loginProfile:
                hasPassword = True
                LoggerUtility.logInfo("The user %s has a password." % userName)

        except ClientError as e:
            LoggerUtility.logWarning("The user %s do not have login profile." % userName)
            return False
        except Exception as e:
            LoggerUtility.logWarning("Exception occured while checking login profile of user. {}".format(e))
            return False
        return hasPassword

    def evaluate(self, eventItem):
        self.__userName = eventItem.configItems['username']
        errorMessage = ""
        evaluationResult = EvaluationResult()
        try:
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            iamClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_IAM,
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName
            )

            cloudTrailClient = BotoUtility.getClient(
                'cloudtrail',
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName
            )
            paginator = cloudTrailClient.get_paginator('lookup_events')

            response_iterator = paginator.paginate(
                LookupAttributes=[
                    {
                        'AttributeKey': 'EventName',
                        'AttributeValue': 'DeactivateMFADevice'
                    },
                ],
                PaginationConfig={
                    'PageSize': 123
                }
            )

            eventItem.configItems.update({TagsConstants.TAG_LIST: [{TagsConstants.EC2_REQUIRED_TAG_KEY: 'Owner', TagsConstants.EC2_REQUIRED_TAG_VALUE: eventItem.configItems['username']}]})
            if self.__hasPassword(iamClient, self.__userName):
                listMfaDevices = iamClient.list_mfa_devices(UserName=self.__userName)
                if not listMfaDevices['MFADevices']:
                    for cloudTrailResponse in response_iterator:
                        for response in cloudTrailResponse['Events']:
                            try:
                                if self.__userName in response['Resources'][0]['ResourceName']:
                                    eventItem.configItems.update({'DeactivationDate': response['EventTime'].strftime("%Y-%m-%d")})
                                    break
                            except Exception:
                                pass

                    LoggerUtility.logInfo("The user '%s' does not have MFA enabled" % self.__userName)
                    evaluationResult.annotation = _("The user does not have Multi-Factor Authentication (MFA) enabled.")
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    eventItem.configItems['createdtime'] = eventItem.configItems['CreateDate'].strftime("%Y-%m-%d")
                    recommendationMessage = "As AWS best security practices,it is important that all IAM users with login profile associated should have MFA enabled."
                    self._AbstractEvaluator__recommendationMessage = _(recommendationMessage)
                else:
                    LoggerUtility.logInfo("The user '%s' have MFA enabled" % self.__userName)
                    evaluationResult.annotation = _("The user have MFA enabled")
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
            else:
                evaluationResult.annotation = _("The user does not have password")
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE

            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

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
            errorMessage = "Error occured while Evaluating user account. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)

        return evaluationResult
