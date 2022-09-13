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
"""This module consist of Exception constants that can be used across all the MNC rules"""


class ExceptionMessages:
    '''
        This class contains general exception messages which are being used in all the MNC rules.
        The error messge recieved in the Excpetion shoud be passed to these strings to formulate the complete message
    '''
    VALUE_ERROR = "The content of the object you tried to assign the value is Invalid: {}"
    ATTRIBUTE_ERROR = "Trying to access or call an attribute of a particular object type doesn’t possess: {}"
    TYPE_ERROR = "Attempt to call a function or use an operator on something of the incorrect type: {}"
    NAME_ERROR = "Trying to access a variable that you have not defined properly: {}"
    CLIENT_ERROR = "Boto client error occured: {}"
