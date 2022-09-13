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
""" This module will fetch the ALB resource details and send it to Evaluator.  """
from rules_common.aws_resource_utility.elbv2_utility import Elbv2Utility
from common.abstract_resource_fetcher import AbstractResourceFetcher


class CheckTargetGroupAssociationWithAlbNlbResourceFetcher(AbstractResourceFetcher):
    """ This class is created for Fetching the target group resource details. """

    def resourceFetcher(self):
        """ This method fetches all the target group details """

        return Elbv2Utility.fetchTargetGroups(eventParam=self._AbstractResourceFetcher__eventParam)
