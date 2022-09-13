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
"""This module will contain port specific utilities."""


class PortUtility:
    ''' Class for all Port Specific Utiliy functions'''

    @staticmethod
    def expandPortRange(ports):
        """ This method will expand ip range. """
        if "-" in ports:
            return range(int(ports.split("-")[0]), int(ports.split("-")[1]) + 1)
        elif "," in ports:
            return [int(port.strip()) for port in ports.split(',')]
        else:
            return [int(ports)]
