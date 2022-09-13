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
from common.boto_utility import BotoUtility
from common.abstract_evaluate import AbstractEvaluator
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from common.common_constants import AWSResourceClassConstants, BotoConstants, ComplianceConstants, ManagedCloudConstants, TagsConstants
from common.rds_constants import RdsConstants
from common.common_utility import CommonUtility
from check_rds_owner_tag_values.check_rds_owner_tag_values_constants import IAMConstants


class CheckRDSOwnerTagValuesEvaluate(AbstractEvaluator):
    """ This class has evaluate method which will evaluate the resources. """
    def __getIamUsers(self):
        """This method will fetch all user names from IAM."""
        try:
            errorMessage = ""
            userNames = []
            minUsers = 100
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            iam = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_IAM,
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName
            )
            lsusers = iam.list_users()
            for user in lsusers[IAMConstants.IAM_USERS]:
                userNames.append(user[IAMConstants.IAM_USER_NAME])

            if (len(userNames)) >= minUsers:
                iamUserListMarker = lsusers[IAMConstants.IAM_MARKER]
                while iamUserListMarker:
                    userlist = iam.list_users(Marker=iamUserListMarker)
                    for user in userlist[IAMConstants.IAM_USERS]:
                        userNames.append(user[IAMConstants.IAM_USER_NAME])
                    if userlist[IAMConstants.IAM_ISTRUNCATED]:
                        iamUserListMarker = userlist[IAMConstants.IAM_MARKER]
                    else:
                        iamUserListMarker = None

        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while fetching user list. {}".format(e)
        if not userNames:
            LoggerUtility.logError(errorMessage)
        return userNames

    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        errorMessage = ""
        try:
            if eventItem.resourceType not in [AWSResourceClassConstants.RDS_INSTANCE]:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The rule doesn't apply to resources of type {type} .").format(
                    type=eventItem.resourceType
                )
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult
            clusterIdentifier = None
            if eventItem.configItems.__contains__(RdsConstants.RDS_CLUSTER_IDENTIFIER):
                clusterIdentifier = eventItem.configItems[RdsConstants.RDS_CLUSTER_IDENTIFIER]
            if clusterIdentifier:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The RDS instance is part of DBCluster {}, therefor can't be validated.").format(clusterIdentifier)
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            if eventItem.configItems[RdsConstants.RDS_STATE_REFERENCE] == RdsConstants.RDS_TERMINATED_STATE_REFERENCE:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The configurationItem was deleted and therefore cannot be validated.")
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            userNames = self.__getIamUsers()
            dbArn = eventItem.configItems[RdsConstants.RDS_ARN_KEY]
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            rdsClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_RDS,
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE])
            tagValues = rdsClient.list_tags_for_resource(ResourceName=dbArn)
            tagResponse = CommonUtility.changeDictionaryKeysToLowerCase(tagValues)
            eventItem.configItems.update({RdsConstants.RDS_TAG_NAME: tagResponse['taglist']})
            tags = eventItem.configItems[RdsConstants.RDS_TAG_NAME]
            # Get tags to dictionary as keys, values
            for tag in tags:
                tagValues.update({tag[TagsConstants.EC2_REQUIRED_TAG_KEY]: tag[TagsConstants.EC2_REQUIRED_TAG_VALUE]})
            if RdsConstants.OWNER_TAG_NAME in tagValues:
                if tagValues[RdsConstants.OWNER_TAG_NAME] in userNames:
                    LoggerUtility.logInfo("The RDS instance has Owner tag with the valid IAM user: %s" % tagValues[RdsConstants.OWNER_TAG_NAME])
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("The RDS instance has Owner tag with the valid IAM user: %s" % tagValues[RdsConstants.OWNER_TAG_NAME])
                    response = rdsClient.remove_tags_from_resource(ResourceName=dbArn, TagKeys=[TagsConstants.NO_OWNER_EXPIRATION_DATE_TAG_KEY])
                else:
                    LoggerUtility.logInfo("The instance has Owner tag with the invalid IAM user: %s" % tagValues[RdsConstants.OWNER_TAG_NAME])
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("The instance has Owner tag with the invalid IAM user.")
                    recommendationMessage = "It is recommended to adhere the tagging standards set for your organization. Kindly refer internal policy documents."  # noqa
                    self._AbstractEvaluator__recommendationMessage = _(recommendationMessage)
            else:
                LoggerUtility.logInfo("RDS Resource does not have Owner tag")
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("RDS instance does not have Owner tag.")
                recommendationMessage = "It is recommended to adhere the tagging standards set for your organization. Kindly refer internal policy documents."
                self._AbstractEvaluator__recommendationMessage = _(recommendationMessage)

            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
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
            errorMessage = "Error occured while evaluating Owner tag in RDS instances. {}".format(e)
        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)
        return evaluationResult
