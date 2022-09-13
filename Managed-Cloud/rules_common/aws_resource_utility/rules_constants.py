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
"""This module consist of all the constants that can be used in AWS MNC rules"""
from common.common_constants import AWSResourceClassConstants


class RulesConstants:
    """Constants for AWS MNC Rules rule."""

    # EC2 Specific Constants
    EC2_TERMINATED_STATE_REFERENCE = "terminated"
    EC2_RUNNING_STATE_REFERENCE = "running"
    EC2_PENDING_STATE_REFERENCE = "pending"
    EC2_STATE_NAME = "name"
    EC2_STATE_REFERENCE = "state"
    EC2_INSTANCE_ID = "instanceid"
    EC2_INSTANCES_REFERENCE = "instances"
    RESPONSE_RESERVATIONS_REFERENCE = "reservations"

    # Common Constants
    STATUS_CODE_RESPONSE_METADATA = "ResponseMetadata"
    HTTP_STATUS_CODE = "HTTPStatusCode"

    # IAM Constants
    IAM_USERS = "Users"
    IAM_USER_NAME = "UserName"

    # ELBv2 Constants
    TARGET_GROUPS = "targetgroups"
    LOAD_BALANCER_ARNS = "loadbalancerarns"


class TagsConstants:
    ''' This class contains constants for general tag related processing '''
    TAG_LIST = "tagList"
    TAGS_REFERENCE = "tags"
    TAG_KEY_REFERENCE = "key"
    TAG_VALUE_REFERENCE = "value"


class MonitoredResourceConstants:
    ''' This class contains constants for processing the input parameters for MNC Monitored Resource Types '''
    RESOURCE_TYPE = "aws_resource_type"
    RESOURCE_UTILITY_REFERENCE = "utility"
    MONITERED_RESOURCES_DICT_REF = {
        AWSResourceClassConstants.EC2_INSTANCE: 'ec2',
        AWSResourceClassConstants.EBS_VOLUME: 'ebs'
    }
