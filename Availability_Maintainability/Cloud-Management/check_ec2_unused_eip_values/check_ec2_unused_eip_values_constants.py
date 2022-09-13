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
    """ Class for Elastic Ip constants """
    RESPONSE_ADDRESSES_KEYWORD = "addresses"
    EC2_INSTANCE_ID_KEYWORD = "instanceid"
    NETWORK_INTERFACE_ID_KEYWORD = "networkinterfaceownerid"
    VPC_DOMAIN_KEYWORD = "vpc"
    ASSOCIATION_ID_REFERENCE = "associationid"
    ALLOCATION_ID_REFERENCE = "allocationid"

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
