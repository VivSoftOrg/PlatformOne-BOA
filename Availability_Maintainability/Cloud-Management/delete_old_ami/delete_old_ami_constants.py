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


class AMIConstants:
    """Constants used in rule."""
    AWS_REGION = 'region'
    Image_Id = 'ImageId'
    Image_Id_Lower = 'imageid'
    AMI_CREATION_DATE = 'creationdate'
    RESPONSE_METADATA = 'ResponseMetadata'
    HTTP_STATUS_CODE = "HTTPStatusCode"
    AMI_FILTER = [{'Name': 'image-type', 'Values': ['machine']}, {'Name': 'state', 'Values': ['available']}]
    DO_NOT_DELETE_TAG = {'Key': 'doNotDelete', 'Value': 'True'}

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
