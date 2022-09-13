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
""" This module will mark launch configuration as a non-compliant if they are not in use. """
from datetime import datetime
from common.boto_utility import BotoUtility
from common.abstract_evaluate import AbstractEvaluator
from common.common_constants import BotoConstants
from common.common_constants import ResourceConstants, ManagedCloudConstants, ComplianceConstants
from common.framework_objects import EvaluationResult
from common.common_utility import CommonUtility
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility


class DeleteUnusedLaunchConfigurationsEvaluate(AbstractEvaluator):
    """ This class will be responsible for evaluating the resources. """
    __launchConfigurationDetails = {ManagedCloudConstants.REGION_REFERENCE: "", ResourceConstants.LAUNCH_CONFIGURATION_LIST: []}

    def __isLaunchConfigurationOlder(self, launchConfigurationCreationTime, spareTime):
        """ This method will be used to check whether launch configuration is older or not. """
        try:
            utc = datetime.utcnow()
            return bool(int((utc - launchConfigurationCreationTime).total_seconds() / 3600) > int(spareTime))
        except Exception as e:
            LoggerUtility.logError(e)

    def __getLaunchConfigurationDetails(self, eventItem):
        """ This method will be used to launch configuration details. """
        try:
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            launchConfigurationList = []
            asgClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_ASC,
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )
            asgResponse = CommonUtility.changeDictionaryKeysToLowerCase(asgClient.describe_auto_scaling_groups()[ResourceConstants.AUTO_SCALING_GROUPS])
            for autoScalingGroup in asgResponse:
                launchConfigurationList.append(autoScalingGroup[ResourceConstants.LAUNCH_CONFIGURATION_NAME])

            self.__launchConfigurationDetails = {
                ManagedCloudConstants.REGION_REFERENCE: eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE],
                ResourceConstants.LAUNCH_CONFIGURATION_LIST: launchConfigurationList
            }
        except Exception as e:
            LoggerUtility.logError(e)

    def __isCompliant(self, eventItem):
        """ This method will be used to check whether launch configuration is compliant or not. """
        isValid = False
        region = eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
        if self.__launchConfigurationDetails[ManagedCloudConstants.REGION_REFERENCE] != region:
            self.__getLaunchConfigurationDetails(eventItem)

        if eventItem.resourceId in self.__launchConfigurationDetails[ResourceConstants.LAUNCH_CONFIGURATION_LIST]:
            isValid = True

        return isValid

    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        spareTime = self._AbstractEvaluator__eventParam.configParam[ResourceConstants.SPARE_TIME_IN_HOURS]
        launchConfigurationCreationTime = eventItem.configItems[ResourceConstants.CREATED_TIME].replace(tzinfo=None)

        if self.__isLaunchConfigurationOlder(launchConfigurationCreationTime, spareTime):
            if not self.__isCompliant(eventItem):
                LoggerUtility.logInfo("Launch configuration '{}' is not in use.".format(eventItem.resourceId))
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = _("Launch configuration is not in use.")
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
            else:
                LoggerUtility.logInfo("Launch configuration '{}' is in use.".format(eventItem.resourceId))
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("Launch configuration is in use.")
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        else:
            LoggerUtility.logInfo("Launch configuration '{}' is not older than {} hours.".format(eventItem.resourceId, spareTime))
            evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
            evaluationResult.annotation = _("Launch configuration is not much older.")
            self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

        return evaluationResult
