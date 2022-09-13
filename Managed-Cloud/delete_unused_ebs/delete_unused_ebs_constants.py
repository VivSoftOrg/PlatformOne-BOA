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


class EBSVolumeConstants:
    """Constants used in rule."""
    EBS_VOLUMES = 'volumes'
    VOLUME_ID = 'volumeid'
    AWS_REGION = 'region'
    TAGS = 'tags'
    TAG_KEY = 'key'
    TAG_VALUE = 'value'
    NAME_TAG = 'Name'
    EBS_CREATION_DATE = 'createtime'
    EBS_Volume_AGE = 'volumeage'
    EBS_AGE = 'age'
    EBS_RESPONSE_METADATA = 'ResponseMetadata'
    EBS_HTTP_STATUS_CODE = "HTTPStatusCode"
    FILTER_VOLUMES = [{'Name': 'status', 'Values': ['available']}]

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
