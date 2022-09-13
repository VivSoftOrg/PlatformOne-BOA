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
    """ Class for ec2_expiry_tag rule constants """
    EC2_EXPIRY_TAG_KEYWORD = "ExpirationDate"
    EC2_REQUIRED_EXPIRY_TAG_KEYWORD = "value"
    EC2_REQUIRED_TAG_KEY = "key"
    EC2_REQUIRED_TAG_VALUE = "value"
    EC2_STATUS_CODE_RESPONCE_METADATA = "ResponseMetadata"
    EC2_HTTP_STATUS_CODE = "HTTPStatusCode"
    LIMIT_EXPIRTION_DATE_REFERENCE = "limit_expiration_date"
    TERMINATION_DAYS = "termination_days"
    EXPIRATION_DAYS = "expirationDays"
    EC2_SUCCESSFULLY_TERMINATED = "Instance terminated and AMI created."
