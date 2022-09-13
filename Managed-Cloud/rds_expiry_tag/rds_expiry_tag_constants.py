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
""" Module for constants """


class Constants:
    """ Class for rds_expiry_tag rule constants """
    RDS_EXPIRY_TAG_KEYWORD = "ExpirationDate"
    RDS_REQUIRED_EXPIRY_TAG_KEYWORD = "value"
    RDS_REQUIRED_TAG_KEY = "key"
    RDS_REQUIRED_TAG_VALUE = "value"
    RDS_STATUS_CODE_RESPONCE_METADATA = "ResponseMetadata"
    RDS_HTTP_STATUS_CODE = "HTTPStatusCode"
    LIMIT_EXPIRTION_DATE_REFERENCE = "limit_expiration_date"

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
