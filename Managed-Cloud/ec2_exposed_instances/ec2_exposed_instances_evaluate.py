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
""" This module will evaluate on the basis of exposed ports. """
import os

from botocore.exceptions import ClientError

from common.abstract_evaluate import AbstractEvaluator
from common.boto_utility import BotoUtility
from common.common_constants import (AWSResourceClassConstants, BotoConstants,
                                     ComplianceConstants, ManagedCloudConstants)
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from ec2_exposed_instances.ec2_exposed_instances_constants import Constants
from utility.port_utility import PortUtility


class EC2ExposedInstancesEvaluate(AbstractEvaluator):
    """ This class will evaluate on the basis of exposed ports. """
    __applicableResources = [AWSResourceClassConstants.EC2_INSTANCE]

    def __findExposedPorts(self, ipPermission, eventItem):
        """ This method will retrieve the open ports for a security group. """
        exposedPorts = []

        try:
            exposedIp = os.environ[Constants.EC2_EXPOSED_IP_ENV_VAR]
        except Exception as e:
            exposedIp = Constants.EC2_EXPOSED_IP_DEFAULT_VAL

        from_port = '-1'
        to_port = '-1'

        for permission in ipPermission:
            if 'FromPort' in permission:
                from_port = permission['FromPort']
            if 'ToPort' in permission:
                to_port = permission['ToPort']
            for cidrRange in permission["IpRanges"]:
                ip = cidrRange["CidrIp"]
                if int(str(ip.split('.')[0])) == 0:
                    exposedPorts.extend(
                        range(
                            int(from_port),
                            int(to_port) + 1
                        )
                    )

        return exposedPorts

    def __findExposedIP(self, ipPermission, eventItem, ports):
        """ This method will find exposed IP particular to port. """
        exposedIP = []

        for permission in ipPermission:
            if 'FromPort' in permission:
                from_port = permission['FromPort']
            if 'ToPort' in permission:
                to_port = permission['ToPort']
            for cidrRange in permission["IpRanges"]:
                ip = cidrRange["CidrIp"]
                for port in ports:
                    if int(str(ip.split('.')[0])) == 0 and port == from_port:
                        exposedIP.append(ip)

        return exposedIP

    def __updateExposedPort(self, eventItem, exposedPorts, ports):
        """ This method will find exposed IP particular to port. """
        exposedPort = []

        for port in ports:
            if port in exposedPorts:
                exposedPort.append(str(port))

        return exposedPort

    def __findViolation(self, ipPermissions, eventItem):
        """ This method checks unwanted ports are exposed or not. """
        exposedPorts = self.__findExposedPorts(ipPermissions, eventItem)
        ports = PortUtility.expandPortRange(
            self._AbstractEvaluator__eventParam.configParam[Constants.EC2_FORBIDDEN_PORTS_REFERENCE]
        )

        for port in ports:
            if port in exposedPorts:
                exposedIP = self.__findExposedIP(ipPermissions, eventItem, ports)
                exposedPort = self.__updateExposedPort(eventItem, exposedPorts, ports)
                eventItem.configItems.update({"ExposedPort": exposedPort})
                eventItem.configItems.update({"ExposedIP": exposedIP})
                return _("A forbidden port is exposed to the internet.")

        return None

    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        errorMessage = ""
        awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
        try:
            if isinstance(eventItem.configItems['tags'], dict):
                eventItem.configItems['tags'] = [{'key': tag, 'value': eventItem.configItems['tags'][tag]} for tag in eventItem.configItems['tags']]

            if eventItem.resourceType not in self.__applicableResources:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The rule doesn't apply to resources of type {type} .").format(
                    type=eventItem.resourceType
                )
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            if eventItem.configItems["state"]["name"] == Constants.EC2_TERMINATED_STATE_REFERENCE:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The configurationItem was deleted and therefore it cannot be validated")
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            securityGroups = eventItem.configItems.get("securitygroups")

            if securityGroups is None:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("The instance doesn't pertain to any security groups")
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            ec2 = BotoUtility.getResource(
                BotoConstants.BOTO_CLIENT_AWS_EC2, self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE])

            for securityGroup in securityGroups:
                ipPermissions = ec2.SecurityGroup(securityGroup["groupid"]).ip_permissions

                hasAViolation = self.__findViolation(ipPermissions, eventItem)

                if hasAViolation:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = hasAViolation
                    self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                    recommendationMessage = "Please ensure you have followed the correct procedure to open this rule."
                    self._AbstractEvaluator__recommendationMessage = recommendationMessage
                    return evaluationResult

            evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
            evaluationResult.annotation = _("This resource is compliant with the rule.")

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
            errorMessage = "Error occured while evaluating for EC2 exposed instances instances. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.UNABLE_TO_CHECK_EVALUATE_COMPLIANCE
            evaluationResult.annotation = _(errorMessage)

        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
