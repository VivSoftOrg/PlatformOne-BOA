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
"""This module consist of all the constants used in the rule"""


class Constants:
    """Constants used in rule."""

    MISSING_TAGS = "missingTags"
    INVALID_TAGS = "invalidTags"
    EXPIRATION_DATE_TAG_KEY = "ExpirationDate"
    RETENTION_PERIOD_TAG_KEY = "RetentionPeriod"
    OWNER_AS_IAM_USERS = "IAM_USERS"
    OWNER_TAG_KEY = "Owner"
    MONITORING_RESOURCES_DYNAMO_DB_TABLE = "monitoringResourcesTable"

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
