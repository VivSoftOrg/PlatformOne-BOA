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
""" This module has constants required for this rule. """


class Constants:
    """ This class has constants required for this rule. """
    RESOURCE_NAME = "CloudFront Distribution"

    DISTRIBUTION_EXPIRED = "The CloudFront Distribution is expired and in `{}` State"
    DISTRIBUTION_NOT_DEPLOYED_EVALUATE = "The CloudFront Distribution is expired but not in Deployed State."
    DISTRIBUTION_NOT_DEPLOYED_ACTION = "Cannot delete the Distribution until its status changes to Deployed."

    DISTRIBUTION_DEPLOYED_STATUS_REFERENCE = "Deployed"
    DISTRIBUTION_ENABLED_STATE_REFERENCE = 'Enabled'
    DISTRIBUTION_DISABLED_STATE_REFERENCE = 'Disabled'

    STREAMING_DISTRIBUTION_LIST_FUNCTION = "list_streaming_distributions"
    WEB_DISTRIBUTION_LIST_FUNCTION = "list_distributions"

    STREAMING_DISTRIBUTION_GET_CONFIG_FUNCTION = "get_streaming_distribution_config"
    WEB_DISTRIBUTION_GET_CONFIG_FUNCTION = "get_distribution_config"

    STREAMING_DISTRIBUTION_UPDATE_FUNCTION = "update_streaming_distribution"
    WEB_DISTRIBUTION_UPDATE_FUNCTION = "update_distribution"

    STREAMING_DISTRIBUTION_DELETE_FUNCTION = "delete_streaming_distribution"
    WEB_DISTRIBUTION_DELETE_FUNCTION = "delete_distribution"

    STREAMING_DISTRIBUTION_CONFIG_REFERENCE = "StreamingDistributionConfig"
    WEB_DISTRIBUTION_CONFIG_REFERENCE = "DistributionConfig"

    STREAMING_DISTRIBUTION_TYPE_REFERENCE = "StreamingDistributionList"
    WEB_DISTRIBUTION_TYPE_REFERENCE = "DistributionList"

    STREAMING_DISTRIBUTION_WAITER_TYPE = "streaming_distribution_deployed"
    WEB_DISTRIBUTION_WAITER_TYPE = "distribution_deployed"

    DISTRIBUTION_DISABLED_ACTION_REFERENCE = "The CloudFront Distribution is Disabled."
    DISTRIBUTION_ABOUT_TO_EXPIRE_ACTION_MESSAGE = "Please update the expiration date if you want to retain the distribution"
    DISTRIBUTION_ACTION_ERROR_MESSAGE = "Error {} the CloudFront Distribution : {}, HTTPStatus Code : {}."
    DISTRIBUTION_EXPIRATION_TAG_ADDED_MESSAGE = "An Expiration Tag is added to the distribution."

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
