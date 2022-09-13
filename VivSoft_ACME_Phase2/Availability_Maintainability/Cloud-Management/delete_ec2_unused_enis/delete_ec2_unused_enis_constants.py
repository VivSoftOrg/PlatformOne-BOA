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
"""This module consist of all the constants used in EC2 Environment tag value rule"""


class Constants:
    """Constants for Unused ENI rule."""
    ENI_AVAILABLE_STATE_REFERENCE = 'available'
    ENI_IN_USE_STATE_REFERENCE = 'in-use'
    ENI_STATUS_CODE_RESPONSE_METADATA = "ResponseMetadata"
    ENI_HTTP_STATUS_CODE = "HTTPStatusCode"

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
