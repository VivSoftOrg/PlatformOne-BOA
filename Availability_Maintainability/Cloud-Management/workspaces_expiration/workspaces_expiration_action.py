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
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.date_validation_util import DateValidationUtil
from common.framework_objects import EvaluationResult
from common.common_constants import BotoConstants, ResourceConstants, TagsConstants, ComplianceConstants, ManagedCloudConstants
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.common_constants import ActionMessages
from workspaces_expiration.workspaces_expiration_constants import Constants


class WorkSpacesAction(AbstractAction):
    """This class perform action if resource is non_compliant """
    def __deleteWorkSpace(self, WSClient, eventItem):
        """This method used to delete workspace"""
        try:
            response = WSClient.terminate_workspaces(TerminateWorkspaceRequests=[{'WorkspaceId': eventItem.resourceId}])
            deleteRequestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]

            if deleteRequestStatus == 200:
                self._AbstractAction__actionMessage = _("Elasticsearch Service deleted")
                LoggerUtility.logInfo("Elasticsearch Service: {} deleted".format(eventItem.resourceId))
                return True

            else:
                errorMessage = ActionMessages.RESOURCE_ACTION_ERROR_MESSAGE.format(
                    'deleting',
                    eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME],
                    eventItem.resourceId,
                    deleteRequestStatus
                )
                self._AbstractAction__actionMessage = _(errorMessage)
                LoggerUtility.logError(errorMessage)
                return False

        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            return False
        except Exception as e:
            LoggerUtility.logError("Error occured while deleting workspace in function call. {}".format(e))
            return False

    def __addExpirationDateTag(self, WSClient, eventItem):
        """this method is used to add Expiration date on the resource"""
        defaultValidity = int(self._AbstractAction__eventParam.configParam[ResourceConstants.RESOURCE_VALIDITY_RULE_PARAM])
        expirationDate = DateValidationUtil.addDaysToToday(defaultValidity)

        expirationTag = [
            {
                'Key': TagsConstants.EXPIRATION_DATE_TAG_KEY,
                'Value': expirationDate
            }
        ]

        try:
            response = WSClient.create_tags(ResourceId=eventItem.resourceId, Tags=expirationTag)
            requestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]

            if requestStatus == 200:
                self._AbstractAction__actionMessage = _(ActionMessages.RESOURCE_EXPIRATION_TAG_ADDED)
                LoggerUtility.logInfo(ActionMessages.RESOURCE_EXPIRATION_TAG_ADDED)
                return True

            else:
                errorMessage = ActionMessages.RESOURCE_ACTION_ERROR_MESSAGE.format(
                    'adding Expiration Tag to',
                    eventItem.configItems[ResourceConstants.RESOURCE_TYPE_NAME],
                    eventItem.resourceId,
                    requestStatus
                )
                self._AbstractAction__actionMessage = _(errorMessage)
                LoggerUtility.logError(errorMessage)
                return False

        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            return False
        except Exception as e:
            LoggerUtility.logError("Error occured while adding ExpirationDate to workspaces. {}".format(e))
            return False

    def performAction(self, eventItem):
        errorMessage = ""
        evaluationResult = EvaluationResult()
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            WSClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_WORKSPACE,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            response = False

            if eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_VALIDITY_EXPIRED:
                if eventItem.configItems['State'] == Constants.WORKSPACE_SUSPENDED:
                    self._AbstractAction__actionMessage = _("Cannot terminate workSpace during SUSPENDED state.")
                    LoggerUtility.logError("Cannot terminate workSpace during SUSPENDED state.")
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = 'Cannot terminate workSpace during SUSPENDED state.'
                else:
                    response = self.__deleteWorkSpace(WSClient, eventItem)
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = ('Workspace deleted successfully.')

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND or \
                    eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_DATE_LIMIT_EXCEEDED or \
                    eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_DATE_INVALID:
                response = self.__addExpirationDateTag(WSClient, eventItem)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = ('Expiration date added to workspace successfully.')

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_ABOUT_TO_EXPIRE:
                response = self._AbstractAction__actionMessage = _(ActionMessages.RESOURCE_ABOUT_TO_EXPIRE)
                LoggerUtility.logInfo(ActionMessages.RESOURCE_ABOUT_TO_EXPIRE)
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = ('Workspace is about to expire.')

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while deleting workspaces. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            self._AbstractAction__actionMessage = _(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)
        else:
            LoggerUtility.logInfo(evaluationResult.annotation)

        return evaluationResult
