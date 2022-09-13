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
""" This module fetches the iam user list """
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.framework_objects_cloudwatch_events import CloudWatchEventsEventItems


class ProcessCloudwatchEventsResourceFetcher(AbstractResourceFetcher):
    """ This class is responsible for fetching the resources """

    def resourceFetcher(self):
        """ perform resource feteching for the Cloudwatch events """
        detail = {"SampleKey": "Sample Value"}
        resourceType = "ec2"
        eventItem = CloudWatchEventsEventItems(
            resourceType=resourceType,
            detail=detail
        )
        return [eventItem]
