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
"""This Module consist of perform action method which will take action."""
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.framework_objects import EvaluationResult
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants, ComplianceConstants, ManagedCloudConstants
from check_ec2_unused_eip_values.check_ec2_unused_eip_values_constants import Constants


class CheckEc2UnusedEIPValuesAction(AbstractAction):
    """Class for performing action on rule."""
    def performAction(self, eventItem):
        domainName = eventItem.configItems['domain']
        errorMessage = ""
        evaluationResult = EvaluationResult()
        try:
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
            )
            if domainName == Constants.VPC_DOMAIN_KEYWORD:
                response = ec2Client.release_address(AllocationId=eventItem.configItems['allocationid'])
            else:
                response = ec2Client.release_address(PublicIp=eventItem.configItems['publicip'])
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                logMessage = "Deleted unused Elastic IP."
                self._AbstractAction__actionMessage = logMessage
                LoggerUtility.logInfo(logMessage)
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = logMessage
            else:
                logMessage = "Could not delete unused Elastic IP."
                self._AbstractAction__actionMessage = logMessage
                LoggerUtility.logError(logMessage)
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = logMessage

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
            errorMessage = "Error occured while stopping instance. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            self._AbstractAction__actionMessage = errorMessage
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = errorMessage

        return evaluationResult
