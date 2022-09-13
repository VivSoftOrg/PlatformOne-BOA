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
""" This module will mark security group as Non-Compliant if it is not in use. """
from common.abstract_evaluate import AbstractEvaluator
from common.boto_utility import BotoUtility
from common.common_constants import BotoConstants, ComplianceConstants
from common.common_utility import CommonUtility
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from delete_unused_security_group.delete_unused_security_group_constants import \
    SecurityGroupConstants


class DeleteUnusedSGEvaluate(AbstractEvaluator):
    """ This class will be responsible for evaluating the resources. """
    securityGroupDetails = {SecurityGroupConstants.REGION_KEYWORD: "", SecurityGroupConstants.SECURITY_GROUP_LIST: []}

    def __fetchSecurityGroupDetails(self, region):
        """ This method will be used to fetch security group details. """
        try:
            securityGroupsList = []
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName,
                region
            )
            lambdaClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_LAMBDA,
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName,
                region
            )

            response = CommonUtility.changeDictionaryKeysToLowerCase(ec2Client.describe_security_groups())
            securityGroups = response[SecurityGroupConstants.SECURITY_GROUP_KEYWORD]

            for securityGroup in securityGroups:
                if securityGroup[SecurityGroupConstants.SECURITY_GROUP_NAME_KEYWORD] == SecurityGroupConstants.DEFAULT_KEYWORD:
                    securityGroupsList.append(securityGroup[SecurityGroupConstants.SECURITY_GROUP_ID_KEYWORD])

                for ipPermission in securityGroup[SecurityGroupConstants.IP_PERMISSIONS_KEYWORD]:
                    for userIdGroupPair in ipPermission[SecurityGroupConstants.USER_ID_GROUP_PAIR_KEYWORD]:
                        if userIdGroupPair[SecurityGroupConstants.SECURITY_GROUP_ID_KEYWORD] not in securityGroupsList:
                            securityGroupsList.append(userIdGroupPair[SecurityGroupConstants.SECURITY_GROUP_ID_KEYWORD])

                response = ec2Client.describe_network_interfaces(
                    Filters=[{SecurityGroupConstants.NAME_KEYWORD: SecurityGroupConstants.GROUP_ID_REFERENCE,
                              SecurityGroupConstants.VALUES_KEYWORD: [securityGroup[SecurityGroupConstants.SECURITY_GROUP_ID_KEYWORD]]
                             }])  # noqa

                if response[SecurityGroupConstants.NETWORK_INTERFACES]:
                    securityGroupsList.append(securityGroup[SecurityGroupConstants.SECURITY_GROUP_ID_KEYWORD])

            # For Lambda
            response = lambdaClient.list_functions()
            lowerResponse = CommonUtility.changeDictionaryKeysToLowerCase(response)
            for response in lowerResponse['functions']:
                if 'vpcconfig' in response.keys():
                    for securityGroup in response['vpcconfig']['securitygroupids']:
                        securityGroupsList.append(securityGroup)

            DeleteUnusedSGEvaluate.securityGroupDetails = {SecurityGroupConstants.REGION_KEYWORD: region,
                                                           SecurityGroupConstants.SECURITY_GROUP_LIST: securityGroupsList}

        except Exception as e:
            LoggerUtility.logError(e)

    def __isCompliant(self, region, resourceId):
        """ This method will be used to check whether the security group is compliant or not. """
        isValid = False

        if DeleteUnusedSGEvaluate.securityGroupDetails[SecurityGroupConstants.REGION_KEYWORD] != region:
            self.__fetchSecurityGroupDetails(region)

        if resourceId in DeleteUnusedSGEvaluate.securityGroupDetails[SecurityGroupConstants.SECURITY_GROUP_LIST]:
            isValid = True

        return isValid

    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        resourceId = eventItem.resourceId
        region = eventItem.configItems[SecurityGroupConstants.REGION_KEYWORD]

        if self.__isCompliant(region, resourceId):
            evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
            evaluationResult.annotation = _("Security group '{}' is in use.".format(eventItem.resourceId))
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
            LoggerUtility.logInfo("Security group '{}' is in use.".format(resourceId))
        else:
            evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
            evaluationResult.annotation = _("Security group is not in use.")
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
            LoggerUtility.logInfo("Security group '{}' is not in use.".format(resourceId))

        return evaluationResult
