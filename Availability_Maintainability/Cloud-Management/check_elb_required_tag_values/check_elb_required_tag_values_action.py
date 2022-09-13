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
""" This module will add expiration tag if required tags are not found on Load Balancer or else will be removed """
from botocore.exceptions import ClientError

from common.abstract_action import AbstractAction
from common.boto_utility import BotoUtility
from common.common_constants import (ActionMessages, AWSResourceClassConstants,
                                     BotoConstants, ComplianceConstants,
                                     ResourceConstants, TagsConstants, ManagedCloudConstants)
from common.date_validation_util import DateValidationUtil
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility


class CheckELBRequiredTagValuesAction(AbstractAction):
    """ This class will be responsible for performing action if the resource is non-compliant"""

    def __deleteLoadBalancer(self, elbClient, eventItem):
        """ This method is used to delete all types of Load Balancer. """
        exceptionMessage = ''
        try:
            evaluationResult = EvaluationResult()
            if eventItem.resourceType == AWSResourceClassConstants.ELB_RESOURCE:
                response = elbClient.delete_load_balancer(LoadBalancerName=eventItem.resourceId)
            else:
                response = elbClient.delete_load_balancer(LoadBalancerArn=eventItem.configItems[ResourceConstants.LOAD_BALANCER_ARN])

            deleteRequestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]

            if deleteRequestStatus == 200:
                self._AbstractAction__actionMessage = _("The {} has been deleted".format(ResourceConstants.ELB_KEYWORD))
                LoggerUtility.logInfo("{} {} deleted".format(ResourceConstants.ELB_KEYWORD, eventItem.resourceId))
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = "The {} has been deleted.".format(ResourceConstants.ELB_KEYWORD)

            else:
                errorMessage = ActionMessages.RESOURCE_ACTION_ERROR_MESSAGE.format(
                    'deleting',
                    ResourceConstants.RESOURCE_TYPE_NAME,
                    eventItem.resourceId,
                    deleteRequestStatus
                )
                self._AbstractAction__actionMessage = _(errorMessage)
                LoggerUtility.logError(errorMessage)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "An error occurred while deleting the {}.".format(ResourceConstants.ELB_KEYWORD)

        except KeyError as e:
            exceptionMessage = "KeyError occurred while deleting the {} : {}".format(e, ResourceConstants.ELB_KEYWORD)

        except ValueError as e:
            exceptionMessage = "ValueError occurred while deleting the {} : {}".format(e, ResourceConstants.ELB_KEYWORD)

        except AttributeError as e:
            exceptionMessage = "AttributeError occurred while deleting the {} : {}".format(e, ResourceConstants.ELB_KEYWORD)

        except ClientError as e:
            exceptionMessage = "Boto ClientError occurred while deleting the {} : {}".format(e, ResourceConstants.ELB_KEYWORD)

        except Exception as e:
            exceptionMessage = "Error occurred while deleting the {} : {}".format(e, ResourceConstants.ELB_KEYWORD)

        if exceptionMessage != '':
            LoggerUtility.logError(exceptionMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(exceptionMessage)
            self._AbstractAction__actionMessage = _(exceptionMessage)

        return evaluationResult

    def __addRequiredExpirationDateTag(self, elbClient, eventItem):
        """ This method will be used to add an expiration tag to elastic Load Balancer. """
        defaultValidity = int(self._AbstractAction__eventParam.configParam[ResourceConstants.RESOURCE_VALIDITY_RULE_PARAM])
        expirationDate = DateValidationUtil.addDaysToToday(defaultValidity)

        expirationTag = [
            {
                TagsConstants.TAG_KEY_REFERENCE: TagsConstants.EXPIRATION_DATE_TAG_KEY,
                TagsConstants.TAG_VALUE_REFERENCE: expirationDate
            }
        ]
        exceptionMessage = ''
        try:
            evaluationResult = EvaluationResult()
            if eventItem.resourceType == AWSResourceClassConstants.ELB_RESOURCE:
                response = elbClient.add_tags(LoadBalancerNames=[eventItem.resourceId], Tags=expirationTag)
            else:
                response = elbClient.add_tags(ResourceArns=[eventItem.configItems[ResourceConstants.LOAD_BALANCER_ARN]], Tags=expirationTag)

            requestStatus = response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE]

            if requestStatus == 200:
                self._AbstractAction__actionMessage = _(ActionMessages.RESOURCE_EXPIRATION_TAG_ADDED)
                LoggerUtility.logInfo(ActionMessages.RESOURCE_EXPIRATION_TAG_ADDED)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "An ExpirationDate tag is added to the {}.".format(ResourceConstants.ELB_KEYWORD)
            else:
                errorMessage = ActionMessages.RESOURCE_ACTION_ERROR_MESSAGE.format(
                    'adding ExpirationDate tag to',
                    ResourceConstants.RESOURCE_TYPE_NAME,
                    eventItem.resourceId,
                    requestStatus
                )
                self._AbstractAction__actionMessage = _(errorMessage)
                LoggerUtility.logError(errorMessage)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "Failed to add ExpirationDate tag to the {}.".format(ResourceConstants.ELB_KEYWORD)

        except KeyError as e:
            exceptionMessage = "KeyError occurred while adding tag to the {} : {}".format(e, ResourceConstants.ELB_KEYWORD)

        except ValueError as e:
            exceptionMessage = "ValueError occurred while adding tag to the {} : {}".format(e, ResourceConstants.ELB_KEYWORD)

        except AttributeError as e:
            exceptionMessage = "AttributeError occurred while adding tag to the {} : {}".format(e, ResourceConstants.ELB_KEYWORD)

        except ClientError as e:
            exceptionMessage = "Boto ClientError occurred while adding tag to the {} : {}".format(e, ResourceConstants.ELB_KEYWORD)

        except Exception as e:
            exceptionMessage = "Error occurred while adding tag to the {} : {}".format(e, ResourceConstants.ELB_KEYWORD)

        if exceptionMessage != '':
            LoggerUtility.logError(exceptionMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(exceptionMessage)
            self._AbstractAction__actionMessage = _(exceptionMessage)

        return evaluationResult

    def performAction(self, eventItem):
        evaluationResult = EvaluationResult()
        exceptionMessage = ''
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            if eventItem.resourceType == AWSResourceClassConstants.ELB_RESOURCE:
                elbClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_ELB,
                    self._AbstractAction__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                    awsPartitionName,
                    eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
                )
            else:
                elbClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_ELB_V2,
                    self._AbstractAction__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                    awsPartitionName,
                    eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
                )

            response = False

            if eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_VALIDITY_EXPIRED:
                evaluationResult = self.__deleteLoadBalancer(elbClient, eventItem)
            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_TAG_NOT_FOUND or \
                eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_DATE_LIMIT_EXCEEDED or \
                    eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_EXPIRATION_DATE_INVALID:
                evaluationResult = self.__addRequiredExpirationDateTag(elbClient, eventItem)
            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_ABOUT_TO_EXPIRE or \
                    eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_HAS_VALIDITY:
                response = self._AbstractAction__recommendationMessage = _(ActionMessages.RESOURCE_ADD_TAGS)
                self._AbstractAction__actionMessage = _("None")
                LoggerUtility.logInfo(ActionMessages.RESOURCE_ADD_TAGS)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "The {} is about to expire.".format(ResourceConstants.ELB_KEYWORD)

        except KeyError as e:
            exceptionMessage = "KeyError occurred while performing action on the resource : {}".format(e)

        except ValueError as e:
            exceptionMessage = "ValueError occurred while performing action on the resource : {}".format(e)

        except AttributeError as e:
            exceptionMessage = "AttributeError occurred while performing action on the resource : {}".format(e)

        except ClientError as e:
            exceptionMessage = "Boto ClientError occurred while performing action on the resource : {}".format(e)

        except Exception as e:
            exceptionMessage = "Error occurred while performing action on the resource : {}".format(e)

        if exceptionMessage != '':
            LoggerUtility.logError(exceptionMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(exceptionMessage)
            self._AbstractAction__actionMessage = _(exceptionMessage)

        return evaluationResult
