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
"""This module consist of all the constants used in copy tag value rule"""


class ALBConstants:
    """Constants for copy tag rule."""
    # The below key value constants are input to the aws api call not the recieved event from aws so they are case sensitive
    TARGET_GROUPS = "TargetGroups"
    SUPPLEMENTARY_CONFIGURATION = "supplementaryconfiguration"
    TAGS_LOWER_CASE = "tags"
    TAGS_PASCAL_CASE = "Tags"
    TARGET_GROUP_ARN = "TargetGroupArn"
    MISSING_TAGS_TARGET_GROUPS = "missingTagsTargetGroups"
    EXCLUDE_TAGS = "excludeTags"
    RESOURCE_ARN = "ResourceArn"

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
