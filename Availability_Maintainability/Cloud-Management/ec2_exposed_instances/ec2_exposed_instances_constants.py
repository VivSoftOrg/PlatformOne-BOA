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
""" This module is defines constants required for this rule. """


class Constants:
    """ This class defines constants required for this rule. """

    EC2_EXPOSED_IP_ENV_VAR = "exposedIp"
    EC2_EXPOSED_IP_DEFAULT_VAL = "0.0.0.0/0"
    EC2_FORBIDDEN_PORTS_REFERENCE = "forbiddenPorts"
    EC2_TERMINATED_STATE_REFERENCE = "terminated"
