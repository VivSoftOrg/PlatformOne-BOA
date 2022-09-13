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
""" This module has constants required for this rule. """


class Constants:
    """ This class has constants required for this rule. """
    EC2_BLOCK_DEVICE_MAPPINGS = 'blockdevicemappings'
    EBS_DELETE_ON_TERMINATION = 'deleteontermination'
    EBS_VOLUME = 'ebs'
    EC2_DEVICE_NAME = 'devicename'
    FILTER_EC2 = [{'Name': 'instance-state-name', 'Values': ['running', 'stopping', 'stopped', 'pending', 'shutting-down']}]
