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
    DYNAMO_DB_EXPIRATION_TAG_REFERENCE = "ExpirationDate"
    DYNAMO_DB_TAG_KEY = "key"
    DYNAMO_DB_TAG_VALUE = "value"
    DYNAMO_DB_ACTIVE_STATUS_REF = "ACTIVE"
    DYNAMO_DB_VALIDITY_RULE_PARAM = 'validity'
    DYNAMO_DB_EXPIRATION_DATE_LIMIT_RULE_PARAM = 'expirationDateLimit'
    DYNAMO_DB_TABLE_HAS_VALIDITY = "For Referrence when expiration date has validity remaining"
    DYNAMO_DB_TABLE_EXPIRATION_DATE_LIMIT_EXCEEDED = "For Reference when expiration date is more than 20 days"
    DYNAMO_DB_TABLE_ABOUT_TO_EXPIRE = "For Reference when expiration date is near"
    DYNAMO_DB_TABLE_VALIDITY_EXPIRED = "For Reference when the expiration date's validity passed."
    DYNAMO_DB_TABLE_EXPIRATION_DATE_NOT_FOUND = "For Reference when either the ExpirationDate tag is not there or is it empty"
    DYNAMO_DB_TABLE_EXPIRATION_DATE_INVALID = "For Reference when the ExpirationDate tag is not valid "
    DYNAMO_DB_RESPONSE_METADATA = "ResponseMetadata"
    DYNAMO_DB_HTTP_STATUS_CODE = "HTTPStatusCode"

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
