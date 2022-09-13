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
""" Module for Constants """


class NoShutDownTagConstants:
    """ Class for NoShutdown tag constants """
    EC2_NOSHUTDOWN_TAG_REFERENCE = "noshutdown"
    EC2_REQUIRED_TAG_KEY = "key"
    EC2_REQUIRED_TAG_VALUE = "value"
    EC2_STATUS_CODE_RESPONSE_METADATA = "ResponseMetadata"
    EC2_HTTP_STATUS_CODE = "HTTPStatusCode"
    EC2_TAGS_NAME = "tags"
    EC2_INSTANCE_ID = "instanceid"
    INSTANCE_IDS_TO_SKIP_KEYWORD = "instanceIdsToSkip"
    EC2_RESERVATION_KEYWORD = "reservations"
    EC2_INSTANCES_KEYWORD = "instances"
    REGION_KEYWORD = "region"
    NAME_KEYWORD = "Name"
    INSTANCE_STATE_NAME = "instance-state-name"
    VALUES_KEYWORD = "Values"
    RUNNING_KEYWORD = "running"
    STOPPED_KEYWORD = "stopped"
    EC2_KEYWORD = "ec2"
    NOSHUTDOWN_KEY = "noShutDownKey"

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value.")

        self.__dict__[attr] = value
