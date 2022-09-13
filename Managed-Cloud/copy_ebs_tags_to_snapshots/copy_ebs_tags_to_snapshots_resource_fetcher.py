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
""" This module will fetch the EC2 Instance resource details and send it to Evaluator.  """
from botocore.exceptions import ClientError

from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.boto_utility import BotoUtility
from common.common_constants import (AWSResourceClassConstants, BotoConstants,
                                     ManagedCloudConstants)
from common.common_utility import CommonUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.logger_utility import LoggerUtility
from copy_ebs_tags_to_snapshots.copy_ebs_tags_to_snapshots_constants import \
    Constants


class CopyEbsTagsToSnapshotsResourceFetcher(AbstractResourceFetcher):
    """ This class is created for Fetching the resource details using Boto Client and provide the reource details to EventItem. """

    def __parseAndFetchEBSDetails(self, instanceObject):
        """Method will fetch instance details and assign it to configItems."""
        resourceId = instanceObject['volumeid']
        configItems = instanceObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.EBS_VOLUME, configItems=configItems)

    def resourceFetcher(self):
        """ This method fetches all the EBS Volumes """
        ebsVolumesList = []
        errorMessage = "No Resources are available."
        awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
        regions = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)
        try:
            for region in regions:
                ec2Client = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_EC2,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )
                LoggerUtility.logInfo('Fetching Volumes in region: {}'.format(region))
                paginator = ec2Client.get_paginator('describe_volumes')
                for paginatorResponse in paginator.paginate():
                    response = CommonUtility.changeDictionaryKeysToLowerCase(paginatorResponse)
                    ebsVolumes = response[Constants.EBS_VOLUMES]
                    for volume in ebsVolumes:
                        volume.update({ManagedCloudConstants.REGION_REFERENCE: region})
                        eventItems = self.__parseAndFetchEBSDetails(volume)
                        ebsVolumesList.append(eventItems)

        except ValueError as e:
            errorMessage = "The content of the object you tried to assign the value is Invalid. {}".format(e)
        except AttributeError as e:
            errorMessage = "Trying to access or call an attribute of a particular object type doesn't possess. {}".format(e)
        except TypeError as e:
            errorMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            errorMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            errorMessage = "Boto client error occured. {}".format(e)
        except Exception as e:
            errorMessage = "Error occured while {}".format(e)
        if not ebsVolumesList:
            LoggerUtility.logError(errorMessage)

        return ebsVolumesList
