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
""" This module is used to mock the test session with saved responses when executing unit test cases """
import os

import boto3
import placebo


class PlaceboMockResponseInitializer():
    """ Class containing functions to mock the AWS API calls """
    PLACEBO_DIR = 'placebo_recorded_responses'

    def __init__(self, testDirectoryPath, moduleName):
        self.testDirectoryPath = testDirectoryPath
        self.moduleName = moduleName

    def getSession(self):
        """ Function to initialize default boto session across all boto calls """
        boto3.setup_default_session()
        session = boto3.DEFAULT_SESSION
        return session

    def replaying_pill(self, mockType):
        """ Function to start placebo mock session """
        session = self.getSession()
        mockResponsePath = self.testDirectoryPath + '/' + self.PLACEBO_DIR + '/test_' + self.moduleName + "_" + mockType
        pill = placebo.attach(session, data_path=os.path.abspath(mockResponsePath))
        pill.playback()
