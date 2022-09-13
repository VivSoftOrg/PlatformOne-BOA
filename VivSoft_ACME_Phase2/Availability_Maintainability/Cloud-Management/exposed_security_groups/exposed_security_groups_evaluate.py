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
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_evaluate import AbstractEvaluator
from common.common_constants import (BotoConstants, AWSResourceClassConstants,
                                     ComplianceConstants, ManagedCloudConstants)
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from ec2_exposed_instances.ec2_exposed_instances_constants import Constants
from utility.port_utility import PortUtility


class ExposedSecurityGroupsEvaluate(AbstractEvaluator):
    """ This class will evaluate on the basis of exposed ports. """
    __applicableResources = [AWSResourceClassConstants.SG_RESOURCE]

    def __getEc2Client(self, eventItem):
        """ Method will create ec2 client """
        ec2Client = None
        try:
            awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self._AbstractEvaluator__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName,
                eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE])
        except Exception as identifier:
            LoggerUtility.logError("Error occoured while creating - {}".format(identifier))

        return ec2Client

    def __getENIDetailsAssociatedWithSecurityGroup(self, ec2Client, securityGroupId):
        """ Method will returns details of associted ENI """
        eniSummaryDetails = ""
        try:
            resp = ec2Client.describe_network_interfaces(Filters=[{'Name': 'group-id', 'Values': [securityGroupId]}])
            if resp['ResponseMetadata']['HTTPStatusCode'] != 200:
                eniSummaryDetails = "Error response while describing network interfaces."
            else:
                if resp['NetworkInterfaces']:
                    eniSummaryDetails = "Associted ENI Details:<br> "
                    counter = 1
                    for eni in resp['NetworkInterfaces']:
                        networkInterfaceId = eni['NetworkInterfaceId']
                        if eni['Description']:
                            description = eni['Description']
                        else:
                            description = "No description available"
                        eniSummaryDetails += "{}. ENI Id - {} ( Description - {}) <br>".format(counter, networkInterfaceId, description)
                        counter += 1
                else:
                    eniSummaryDetails = "No ENI associated with the security group."
        except Exception as expMsg:
            eniSummaryDetails = "Error occoured while fetching ENI details - {}".format(expMsg)
        return eniSummaryDetails

    def evaluate(self, eventItem):
        associatedENIDetails = ""
        evaluationResult = EvaluationResult()
        errorMessage = ""
        awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
        exposedIP = []
        exposedPort = []

        groupsToExclude = self._AbstractEvaluator__eventParam.configParam['excludedGroupsName'].split(',')
        groupsToExclude = [group.strip() for group in groupsToExclude]

        excludedPorts = self._AbstractEvaluator__eventParam.configParam['excludedPorts']
        excludedPorts = [int(item.strip()) for item in excludedPorts.split(',')]
        ip = ""
        try:
            ports = PortUtility.expandPortRange(
                self._AbstractEvaluator__eventParam.configParam[Constants.EC2_FORBIDDEN_PORTS_REFERENCE]
            )

            if eventItem.resourceType not in self.__applicableResources:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANCE_NOT_APPLICABLE
                evaluationResult.annotation = _("The rule doesn't apply to resources of type {type} .".format(type=eventItem.resourceType))
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                return evaluationResult

            if eventItem.configItems['groupname'] not in groupsToExclude:
                for permission in eventItem.configItems['ippermissions']:
                    portRange = range(0)
                    if "fromport" in permission:
                        from_port = permission['fromport']
                        if "toport" in permission:
                            to_port = permission['toport']
                        portRange = range(from_port, to_port)
                    if "ipv4ranges" in permission:
                        ipRanges = permission['ipv4ranges']
                    else:
                        ipRanges = permission['ipranges']

                    for cidrRange in ipRanges:
                        ip = cidrRange['cidrip']
                        for port in ports:
                            if port not in excludedPorts:
                                if int(str(ip.split('.')[0])) == 0 and (port == from_port or port in portRange):
                                    exposedIP.append(str(ip))
                                    exposedPort.append(str(port))

                if exposedIP and exposedPort:
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("A forbidden port is exposed to the internet")
                    self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
                    recommendationMessage = "Please ensure you have followed the correct procedure to open this rule. Kindly correct your security group rule to not be open to the world"
                    self._AbstractEvaluator__recommendationMessage = recommendationMessage
                    eventItem.configItems.update({"ExposedIP": exposedIP})
                    eventItem.configItems.update({"ExposedPort": exposedPort})
                else:
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = _("This resource is compliant with the rule.")
            else:
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = _("The group is excluded from evaluation.")
                self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation

            if evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE:
                ec2Client = self.__getEc2Client(eventItem)
                if ec2Client:
                    associatedENIDetails = self.__getENIDetailsAssociatedWithSecurityGroup(ec2Client=ec2Client, securityGroupId=eventItem.resourceId)
                else:
                    LoggerUtility.logError("Error occoured while creating ec2 client")

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is Invalid. {}".format(e)
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

        eventItem.configItems.update({"additionalDetails": associatedENIDetails})
        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
