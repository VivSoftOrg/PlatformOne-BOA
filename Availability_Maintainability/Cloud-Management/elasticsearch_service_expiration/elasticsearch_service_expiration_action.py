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
""" This method will perform an action depending on a resource is compliant or not complaint. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.date_validation_util import DateValidationUtil
from common.common_constants import ComplianceConstants, BotoConstants, TagsConstants, ResourceConstants, ActionMessages, ManagedCloudConstants
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.framework_objects import EvaluationResult


class ElasticSearchServiceAction(AbstractAction):
    """ This method will perform an action depending on a resource is compliant or not complaint. """

    def __deleteElasticService(self, ESClient, eventItem):
        """ This method will delete elastic service. """
        try:
            response = ESClient.delete_elasticsearch_domain(DomainName=eventItem.configItems['resourceName'])
            deleteRequestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]

            if deleteRequestStatus == 200:
                self._AbstractAction__actionMessage = _("ElasticSerach Service Deleted")
                LoggerUtility.logInfo("ElasticSearch Service: {} Deleted".format(eventItem.resourceId))
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

        except Exception as e:
            LoggerUtility.logError(e)
            return False

    def __addExpirationDateTag(self, ESClient, eventItem):
        """ This method will add ExpirationDate tag. """
        defaultValidity = int(self._AbstractAction__eventParam.configParam[ResourceConstants.RESOURCE_VALIDITY_RULE_PARAM])
        expirationDate = DateValidationUtil.addDaysToToday(defaultValidity)

        expirationTag = [
            {
                'Key': TagsConstants.EXPIRATION_DATE_TAG_KEY,
                'Value': expirationDate
            }
        ]

        try:
            response = ESClient.add_tags(ARN=eventItem.configItems['ARN'], TagList=expirationTag)

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

        except Exception as e:
            LoggerUtility.logError(e)

    def performAction(self, eventItem):
        errorMessage = ""
        evaluationResult = EvaluationResult()
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            ESClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_ELASTICSEARCH,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )

            response = False

            if eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_VALIDITY_EXPIRED:
                response = self.__deleteElasticService(ESClient, eventItem)
                if response:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Resource is deleted")
                else:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Unable to delete resource")

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND or eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_DATE_LIMIT_EXCEEDED or eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_DATE_INVALID:  # noqa
                response = self.__addExpirationDateTag(ESClient, eventItem)
                if response:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("ExpirationDate tag added to resource with default value.")
                else:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("Unable to add ExpirationTag.")

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_ABOUT_TO_EXPIRE:
                response = _(ActionMessages.RESOURCE_ABOUT_TO_EXPIRE)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _(ActionMessages.RESOURCE_ABOUT_TO_EXPIRE)

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
            errorMessage = "Error occured while performing action on Elasticsearch Service. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)
        else:
            LoggerUtility.logInfo(evaluationResult.annotation)

        self._AbstractAction__actionMessage = evaluationResult.annotation
        return evaluationResult
