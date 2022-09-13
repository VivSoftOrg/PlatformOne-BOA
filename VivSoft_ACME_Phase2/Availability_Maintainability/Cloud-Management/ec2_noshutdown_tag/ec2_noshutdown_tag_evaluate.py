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
""" This module will check whether NoShutdown tag is present to EC2 instance or not. If not then mark it as a Non-Compliant. """
from common.common_constants import ComplianceConstants
from common.abstract_evaluate import AbstractEvaluator
from common.framework_objects import EvaluationResult
from common.logger_utility import LoggerUtility
from ec2_noshutdown_tag.ec2_noshutdown_tag_constants import NoShutDownTagConstants


class Ec2NoshutdownTagEvaluate(AbstractEvaluator):
    """ This class will be responsible for evaluating the resources. """

    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        instanceIdsToSkipList = []
        errorMessage = ""
        try:
            instanceIdsToSkipList = self._AbstractEvaluator__eventParam.configParam[NoShutDownTagConstants.INSTANCE_IDS_TO_SKIP_KEYWORD].split(",")
            isNoShutdownTagPresent = False

            if eventItem.resourceId not in instanceIdsToSkipList:
                if NoShutDownTagConstants.EC2_TAGS_NAME in eventItem.configItems:
                    for tag in eventItem.configItems[NoShutDownTagConstants.EC2_TAGS_NAME]:
                        if tag[NoShutDownTagConstants.EC2_REQUIRED_TAG_KEY].lower() == NoShutDownTagConstants.EC2_NOSHUTDOWN_TAG_REFERENCE:
                            eventItem.configItems.update({NoShutDownTagConstants.NOSHUTDOWN_KEY: tag[NoShutDownTagConstants.EC2_REQUIRED_TAG_KEY]})
                            isNoShutdownTagPresent = True
                            break
                else:
                    eventItem.configItems.update({NoShutDownTagConstants.EC2_TAGS_NAME: []})

            if isNoShutdownTagPresent is True:
                LoggerUtility.logInfo("Resource has NoShutdown tag")
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "Resource has NoShutdown tag"
            else:
                LoggerUtility.logInfo("Resource does not have NoShutdown tag")
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = "Resource does not have NoShutdown tag"

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type doesn't possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while performing evaluating for EC2 project tag. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = errorMessage
        else:
            LoggerUtility.logInfo(evaluationResult.annotation)

        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
