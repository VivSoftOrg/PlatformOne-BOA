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
"""This module consist of all the constants used in the rule: active iam users"""


class IamConstants:
    """Constants used in rule."""
    IAM_USERS = "users"
    IAM_USER_NAME = "username"
    IAM_USER_ID = "userid"
    IAM_USER_ACCESS_KEY_ID = "accesskeyid"
    IAM_ACCESS_KEY_LAST_USED = "accesskeylastused"
    IAM_USER_HAS_PASSWORD_DISABLED = "passworddisabled"
    IAM_USER_NEVER_ACCESSED = "Never"
    IAM_USER_CREATE_DATE = "createdate"
    IAM_ACCESS_KEY_LAST_USED_DATE = "lastuseddate"
    IAM_USER_PASSWORD_LAST_USED = "passwordlastused"
    IAM_USER_LAST_ACTIVITY_VALIDITY = "lastActivityValidity"
    ACCESS_KEY_METADATA = "accesskeymetadata"
    IAM_USER_DELETE_WARNINGS = "deleteWarnings"
    IAM_USER_DISABLE_WARNINGS = "disableWarnings"
    IAM_USER_DELETE = "deleteuser"

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value