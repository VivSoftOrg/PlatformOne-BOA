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
""" This module will take action noncompliant instances and try to stop them. """
from botocore.exceptions import ClientError

from common.abstract_action import AbstractAction
from common.boto_utility import BotoUtility
from common.common_constants import BotoConstants, ComplianceConstants
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.logger_utility import LoggerUtility
from ec2_exposed_instances.ec2_exposed_instances_constants import Constants
from utility.port_utility import PortUtility


class EC2ExposedInstancesAction(AbstractAction):
    """ This class will take action noncompliant instances and try to stop them. """

    def __revokePublicRule(self, eventItem, ec2Client):
        """ This method will revoke the public rule from a security group attached to an instance. """
        try:
            securityGroups = eventItem.configItems.get("securitygroups")
            ports = PortUtility.expandPortRange(
                self._AbstractAction__eventParam.configParam[Constants.EC2_FORBIDDEN_PORTS_REFERENCE])

            for securityGroup in securityGroups:
                groups = ec2Client.describe_security_groups(GroupIds=[securityGroup["groupid"]])
                for group in groups['SecurityGroups']:
                    ipPermission = group['IpPermissions']
                    for permission in ipPermission:
                        if 'FromPort' in permission:
                            from_port = permission['FromPort']
                        if 'ToPort' in permission:
                            to_port = permission['ToPort']
                        if 'IpProtocol' in permission:
                            ipProtocol = permission['IpProtocol']
                        for cidrRange in permission["IpRanges"]:
                            ip = cidrRange["CidrIp"]
                            for port in ports:
                                if int(str(ip.split('.')[0])) == 0 and port == from_port:
                                    response = ec2Client.revoke_security_group_ingress(
                                        GroupId=securityGroup["groupid"],
                                        CidrIp=ip,
                                        FromPort=from_port,
                                        ToPort=to_port,
                                        IpProtocol=ipProtocol
                                    )
            return True
        except Exception as e:
            LoggerUtility.logError(e)
            return False

    def performAction(self, eventItem):
        errorMessage = ""
        try:
            evaluationResult = EvaluationResult()
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            ec2Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_EC2,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName
            )

            if self.__revokePublicRule(eventItem, ec2Client):
                evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                evaluationResult.annotation = ('The public rule has been revoked from the security group.')
            else:
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = ('The public rule could not be revoked from the security group.')

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
            errorMessage = "Error occurred while performing an action for EC2 exposed instances. {}".format(e)

        if errorMessage != "":
            LoggerUtility.logError(errorMessage)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = _(errorMessage)
        else:
            LoggerUtility.logInfo(evaluationResult.annotation)

        self._AbstractAction__actionMessage = evaluationResult.annotation
        return evaluationResult
