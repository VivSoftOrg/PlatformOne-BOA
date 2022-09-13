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
""" This module will add ExpirationDate tag with default validity if not present,
 Starts sending reminder before 3 days of expiration, deletes the distrubution after crossing the date. """
from datetime import date, timedelta
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants, ResourceConstants, TagsConstants, ComplianceConstants
from common.framework_objects import EvaluationResult
from cloudfront_distribution_expiration.cloudfront_distribution_expiration_constants import Constants


class CloudFrontDistributionAction(AbstractAction):
    """ This method will take action on cloudfront depends on expirationdate tag. """

    def __disableDistribution(self, CFClient, eventItem):
        """ This method will disable distribution. """
        try:
            response = getattr(CFClient, eventItem.configItems['UpdateFunction'])(
                **eventItem.configItems['configArgument'],
                Id=eventItem.resourceId,
                IfMatch=eventItem.configItems['ETag']
            )
            disableRequestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]

            if disableRequestStatus == 200:
                self._AbstractAction__actionMessage = _("The distributions was disabled and will be deleted on next run.")
                LoggerUtility.logInfo("The distributions was disabled and will be deleted on next run.")
                return Constants.DISTRIBUTION_DISABLED_ACTION_REFERENCE

            else:
                errorMessage = Constants.DISTRIBUTION_ACTION_ERROR_MESSAGE.format(
                    'disabling',
                    eventItem.resourceId,
                    disableRequestStatus
                )
                self._AbstractAction__actionMessage = _(errorMessage)
                LoggerUtility.logError(errorMessage)
                return False

        except Exception as e:
            LoggerUtility.logError(e)

    def __deleteDistribution(self, CFClient, eventItem):
        """ This method will delete distribution. """
        try:
            ETagHeader = eventItem.configItems['ETag']
            response = getattr(CFClient, eventItem.configItems['DeleteFunction'])(Id=eventItem.resourceId, IfMatch=ETagHeader)
            deleteRequestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]

            if deleteRequestStatus == 204:
                self._AbstractAction__actionMessage = _("Distribution deleted")
                LoggerUtility.logInfo("Distribution deleted")
                return True

            else:
                errorMessage = Constants.DISTRIBUTION_ACTION_ERROR_MESSAGE.format(
                    'deleting',
                    eventItem.resourceId,
                    deleteRequestStatus
                )
                self._AbstractAction__actionMessage = _(errorMessage)
                LoggerUtility.logError(errorMessage)
                return False

        except Exception as e:
            LoggerUtility.logError("Error occured while deleting distribution. {}".format(e))

    def __addExpirationDateTag(self, CFClient, eventItem):
        """ This method will add expiration date tag. """
        defaultValidity = int(self._AbstractAction__eventParam.configParam[ResourceConstants.RESOURCE_VALIDITY_RULE_PARAM])
        expirationDate = (date.today() + timedelta(days=defaultValidity)).isoformat()

        expirationTag = {
            'Items': [
                {
                    'Key': TagsConstants.EXPIRATION_DATE_TAG_KEY,
                    'Value': expirationDate
                }
            ]
        }

        try:
            response = CFClient.tag_resource(Resource=eventItem.configItems['ARN'], Tags=expirationTag)

            requestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]
            if requestStatus == 204:
                self._AbstractAction__actionMessage = _(Constants.DISTRIBUTION_EXPIRATION_TAG_ADDED_MESSAGE)
                LoggerUtility.logInfo(Constants.DISTRIBUTION_EXPIRATION_TAG_ADDED_MESSAGE)
                return True

            else:
                errorMessage = Constants.DISTRIBUTION_ACTION_ERROR_MESSAGE.format(
                    'adding ExpirationDate tag to',
                    eventItem.resourceId,
                    requestStatus
                )
                self._AbstractAction__actionMessage = _(errorMessage)
                LoggerUtility.logError(errorMessage)
                return False

        except Exception as e:
            LoggerUtility.logError("Error occured while adding ExpirationDate tag. {}".format(e))

    def performAction(self, eventItem):
        evaluationResult = EvaluationResult()
        errorMessage = ""
        awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
        try:
            CFClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_CLOUDFRONT,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName
            )

            response = False

            if eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] ==  \
                    Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_ENABLED_STATE_REFERENCE):
                response = self.__disableDistribution(CFClient, eventItem)
                if response:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Distribution disabled")
                else:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Unable to disable distribution")

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] ==  \
                    Constants.DISTRIBUTION_EXPIRED.format(Constants.DISTRIBUTION_DISABLED_STATE_REFERENCE):
                response = self.__deleteDistribution(CFClient, eventItem)
                if response:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Distribution deleted")
                else:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Unable to delete distribution")

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == Constants.DISTRIBUTION_NOT_DEPLOYED_EVALUATE:
                response = _(Constants.DISTRIBUTION_NOT_DEPLOYED_ACTION)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _(Constants.DISTRIBUTION_NOT_DEPLOYED_ACTION)

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND or eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_DATE_LIMIT_EXCEEDED or eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_DATE_INVALID:  # noqa
                response = self.__addExpirationDateTag(CFClient, eventItem)
                if response:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("ExpirationDate tag added with default value")
                else:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Unable to add ExpirationDate tag")

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_ABOUT_TO_EXPIRE:
                response = _(Constants.DISTRIBUTION_ABOUT_TO_EXPIRE_ACTION_MESSAGE)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _(Constants.DISTRIBUTION_ABOUT_TO_EXPIRE_ACTION_MESSAGE)

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type doesn't possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occurred while performing an action on CloudFront service. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)
        else:
            LoggerUtility.logInfo(evaluationResult.annotation)

        self._AbstractAction__actionMessage = evaluationResult.annotation
        return evaluationResult
