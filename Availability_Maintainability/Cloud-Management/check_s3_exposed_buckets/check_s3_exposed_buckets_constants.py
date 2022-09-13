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
    """ Class for S3 exposed bucket constants """
    ALL_USERS_KEYWORD = 'AllUsers'
    URI_KEYWORD = 'URI'
    PRIVATE_KEYWORD = "private"
    GRANTS_KEYWORD = "Grants"
    GRANTEE_KEYWORD = "Grantee"
    POLICY_KEYWORD = "Policy"
    STATEMENT_KEYWORD = "Statement"
    EFFECT_KEYWORD = "Effect"
    ALLOW_KEYWORD = "Allow"
    PRINCIPAL_KEYWORD = "Principal"
    BUCKETS_KEYWORD = "Buckets"
    CREATION_DATE_KEYWORD = "creationdate"
    CREATION_DATE_REFERENCE = "CreationDate"
    TAG_SET_KEYWORD = "TagSet"
    LOCATION_CONSTRAINT_KEYWORD = "LocationConstraint"
    US_EAST_1_REGION = "us-east-1"
    AWS_KEYWORD = "AWS"

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
