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
""" Module for constants """


class SecurityGroupConstants:
    """ Class for security group constants """
    SECURITY_GROUP_KEYWORD = 'securitygroups'
    SECURITY_GROUP_ID_KEYWORD = "groupid"
    SECURITY_GROUP_NAME_KEYWORD = "groupname"
    VPC_SECURITY_GROUP_ID = 'vpcsecuritygroupid'
    IP_PERMISSIONS_KEYWORD = 'ippermissions'
    USER_ID_GROUP_PAIR_KEYWORD = 'useridgrouppairs'
    RESERVATIONS_KEYWORD = 'reservations'
    INSTANCES_KEYWORD = 'instances'
    DBINSTANCES_KEYWORD = 'DBInstances'
    VPC_SECURITY_GROUPS = 'vpcsecuritygroups'
    LOAD_BALANCER_DESCRIPTIONS = 'LoadBalancerDescriptions'
    RESPONSE_METADATA = "ResponseMetadata"
    RESPONSE_HTTP_STATUS_CODE = "HTTPStatusCode"
    DEFAULT_KEYWORD = "default"
    INSTANCE_STATE_NAME = "instance-state-name"
    NAME_KEYWORD = "Name"
    RUNNING_KEYWORD = "running"
    STOPPED_KEYWORD = "stopped"
    VALUES_KEYWORD = "Values"
    REGION_KEYWORD = "region"
    EC2_KEYWORD = "ec2"
    GROUP_ID_KEYWORD = "GroupId"
    GROUP_ID_REFERENCE = "group-id"
    SECURITY_GROUP_LIST = "securityGroupList"
    NETWORK_INTERFACES = "NetworkInterfaces"

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value.")

        self.__dict__[attr] = value
