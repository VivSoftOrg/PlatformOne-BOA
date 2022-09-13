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
""" Placebo Mock Response Initializer """
import os
import placebo
import boto3


class PlaceboMockResponseInitializer():
    """ Placebo Mock Response Initializer class """

    @staticmethod
    def getSession():
        """ getSession  method """
        boto3.setup_default_session()
        session = boto3.DEFAULT_SESSION
        return session

    @staticmethod
    def replaying_pill(mockResponsePath):
        """ replaying pill method """
        session = PlaceboMockResponseInitializer.getSession()
        pill = placebo.attach(session, data_path=os.path.abspath(mockResponsePath))
        pill.playback()

    @staticmethod
    def getActionMock(mockType):
        """ getActionMock method """
        PLACEBO_DIR = 'placebo_recorded_responses'
        PLACEBO_ACTION_MOCKS = 'test_cloudfront_distribution_expiration_action'
        dir_path = os.path.dirname(os.path.realpath(__file__))
        mockPath = dir_path + '/' + PLACEBO_DIR + '/' + PLACEBO_ACTION_MOCKS + '/' + mockType
        return mockPath

    @staticmethod
    def getEvaluatorMock(mockType):
        """ getEvaluatorMock method """
        PLACEBO_DIR = 'placebo_recorded_responses'
        PLACEBO_EVALUATION_MOCKS = 'test_cloudfront_distribution_expiration_evaluate'
        dir_path = os.path.dirname(os.path.realpath(__file__))
        mockPath = dir_path + '/' + PLACEBO_DIR + '/' + PLACEBO_EVALUATION_MOCKS + '/' + mockType
        return mockPath

    @staticmethod
    def getResourceFetcherMock(mockType):
        """ getResourceFetcherMock method """
        PLACEBO_DIR = 'placebo_recorded_responses'
        PLACEBO_RESOURCE_FETCHER_MOCKS = 'test_cloudfront_distribution_expiration_resource_fetcher'
        dir_path = os.path.dirname(os.path.realpath(__file__))
        mockPath = dir_path + '/' + PLACEBO_DIR + '/' + PLACEBO_RESOURCE_FETCHER_MOCKS + '/' + mockType
        return mockPath
