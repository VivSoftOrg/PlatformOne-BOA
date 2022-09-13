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


class Constants:
    """Constants for copy tag rule."""
    # The below key value constants are input to the aws api call not the recieved event from aws so they are case sensitive
    ID = "Id"
    COPY_TAGS = "CopyTags"
    EC2_TAG_KEY = "Key"
    EC2_TAG_VALUE = "Value"
    EBS_VOLUMES = 'volumes'
    TAGS_TO_COPY = "tagsToCopy"
    EC2_TAGS_NAME = "tags"
    EC2_STATE_REFERENCE = "state"
    EC2_STATE_NAME = "name"
    EC2_INSTANCE_ID = "instanceid"
    EC2_VOLUME_ID = "volumeid"
    RESPONSE_RESERVATIONS_REFERENCE = "reservations"
    EC2_INSTANCES_REFERENCE = "instances"
    EC2_STATUS_CODE_RESPONSE_METADATA = "ResponseMetadata"
    EC2_HTTP_STATUS_CODE = "HTTPStatusCode"

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
