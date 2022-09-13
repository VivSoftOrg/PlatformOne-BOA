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
""" This module has common constants required for this rule  """


class Constants:
    """ This class has common constants required for this rule  """
    FILTER_INSTANCES = [
        {
            'Name': 'instance-state-name',
            'Values': ['pending', 'stopped', 'running']
        }
    ]

    INPUT_MAPPINGS = 'mappings'
    VPC_ID = 'vpcid'
    SECURITY_GROUPS = 'securitygroups'
    GROUP_ID = 'groupid'
    ATTACH_GROUPS = 'attachgroups'
    ALL_SECURITY_GROUPS = 'allsecuritygroupsofvpc'
    GROUPS_NOT_FOUND = 'groupsnotfound'

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
