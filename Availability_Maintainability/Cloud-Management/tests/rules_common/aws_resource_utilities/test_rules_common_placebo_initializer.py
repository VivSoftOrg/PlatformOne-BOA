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
import os
import placebo
import boto3

class PlaceboMockResponseInitializer():

    @staticmethod
    def getSession():
        boto3.setup_default_session()
        session = boto3.DEFAULT_SESSION
        return session

    @staticmethod
    def replaying_pill(mockResponsePath):
        session = PlaceboMockResponseInitializer.getSession()
        pill = placebo.attach(session, data_path= os.path.abspath(mockResponsePath))
        pill.playback()
