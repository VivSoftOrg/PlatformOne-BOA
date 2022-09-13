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
import pytest
import sys

sys.path.append('../../')

import common.logger_utility as lu
from mock import MagicMock

class TestLoggerUtility(object):

    def test_log_info(self):
        assert(lu.LoggerUtility.logInfo("Hello"))

    def test_log_error(self):
        assert(lu.LoggerUtility.logError("Error"))
        