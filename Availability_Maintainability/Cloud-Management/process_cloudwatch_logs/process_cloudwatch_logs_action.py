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
""" Pefrom Action on Cloudwatch Event"""
from common.abstract_action import AbstractAction


class ProcessCloudwatchLogsAction(AbstractAction):
    """ Pefrom Action on Cloudwatch Event"""

    # The purpose of this function is to do action for Cloudwatch events.
    # Currently we don't have any action for Cloudwatch events, so
    # this performAction function is not doing anything
    def performAction(self, eventItem):
        return True
