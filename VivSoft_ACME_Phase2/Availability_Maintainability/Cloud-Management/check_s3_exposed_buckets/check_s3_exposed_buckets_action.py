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
""" This module will remove public access of S3 bucket if it is publicly accessible. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants
from common.common_constants import ComplianceConstants
from common.common_constants import CommonKeywords, ManagedCloudConstants
from common.framework_objects import EvaluationResult
from check_s3_exposed_buckets.check_s3_exposed_buckets_constants import Constants


class S3ExposedBucketsAction(AbstractAction):
    """ This class will be responsible for performing action if the resource is non-compliant. """
    def performAction(self, eventItem):
        try:
            evaluationResult = EvaluationResult()
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            s3Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_S3,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )
            try:
                if eventItem.configItems[CommonKeywords.REMOVE_ACL] is True:
                    response = s3Client.put_bucket_acl(
                        ACL=Constants.PRIVATE_KEYWORD,
                        Bucket=eventItem.configItems[CommonKeywords.NAME_KEYWORD]
                    )
            except ClientError as e:
                LoggerUtility.logWarning(e)
            except Exception as e:
                LoggerUtility.logWarning(e)

            try:
                if eventItem.configItems[CommonKeywords.REMOVE_POLICY] is True:
                    response = s3Client.delete_bucket_policy(
                        Bucket=eventItem.configItems[CommonKeywords.NAME_KEYWORD]
                    )
            except ClientError as e:
                LoggerUtility.logWarning(e)
            except Exception as e:
                LoggerUtility.logWarning(e)

            if response[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200 or response['ResponseMetadata']['HTTPStatusCode'] == 204:  # noqa
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = ('The bucket is not publicly accessible.')
                self._AbstractAction__actionMessage = _("Removed public access")
                LoggerUtility.logInfo("Removed public access")
                return evaluationResult
            else:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = ('The bucket is publicly accessible.')
                self._AbstractAction__actionMessage = _("Could not remove public access")
                LoggerUtility.logWarning("Could not remove public access")
                return evaluationResult
        except ValueError as e:
            LoggerUtility.logError("ValueError occurred while performing action on the resource : {}".format(e))
            self._AbstractAction__actionMessage = _("Error while removing public access '{exception}'").format(exception=e)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except KeyError as e:
            LoggerUtility.logError("KeyError occurred while performing action on the resource : {}".format(e))
            self._AbstractAction__actionMessage = _("Error while removing public access '{exception}'").format(exception=e)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except AttributeError as e:
            LoggerUtility.logError("AttributeError occurred while performing action on the resource : {}".format(e))
            self._AbstractAction__actionMessage = _("Error while removing public access '{exception}'").format(exception=e)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except ClientError as e:
            LoggerUtility.logError("Boto ClientError occurred while performing action on the resource : {}".format(e))
            self._AbstractAction__actionMessage = _("Error while removing public access '{exception}'").format(exception=e)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        except Exception as e:
            LoggerUtility.logError("Error occurred while performing action on the resource : {}".format(e))
            self._AbstractAction__actionMessage = _("Error while removing public access '{exception}'").format(exception=e)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = e

        return evaluationResult
