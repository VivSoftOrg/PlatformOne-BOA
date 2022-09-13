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
import sys
import pytest
import mock

from mock import MagicMock
from moto import mock_iam
sys.path.append('../../')
from common.get_account_alias import *
import common.get_account_alias as ga

accNo = "411815166437"

alias = {'ResponseMetadata': {'HTTPHeaders': {'content-length': '389', 'x-amzn-requestid': '3eb40950-ec7e-11e7-ab2c-af0c632aa4a6', 'date': 'Fri, 29 Dec 2017 09:54:21 GMT', 'content-type': 'text/xml'}, 'HTTPStatusCode': 200, 'RequestId': '3eb40950-ec7e-11e7-ab2c-af0c632aa4a6', 'RetryAttempts': 0}, 'AccountAliases': ['mnc-master'], 'IsTruncated': False}


class TestGetAccountAlias(object):

    @mock_iam
    def test_get_account_alias(self):
        __getAccountAlias = GetAccountAlias()
        iamClient = boto3.client('iam')
        iamClient.list_account_aliases = MagicMock(return_value = alias)
        ga.BotoUtility.getClient = MagicMock(return_value = iamClient)
        list_account_aliases = __getAccountAlias.getAccountAlias(accNo)
        assert list_account_aliases == alias
