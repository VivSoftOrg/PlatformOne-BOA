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
""" This module will fetch ebs snapshots from all the available regions. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import BotoConstants, ManagedCloudConstants, ResourceConstants, TagsConstants
from unencrypted_snapshot.unencrypted_snapshot_constants import SnapshotConstants


class UnencryptedSnapshotResourceFetcher(AbstractResourceFetcher):
    """ This class is responsible for fetching the resources """
    def __parseAndFetchSnapshotDetails(self, snapObject):
        """ This method will be used to fetch and parse snapshot details. """
        resourceId = snapObject[SnapshotConstants.SNAPSHOT_ID]
        configItems = snapObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, configItems=configItems)

    def resourceFetcher(self):
        unencryptedSnapshot = []
        awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
        regions = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)
        try:
            errorMessage = ""
            for region in regions:
                ec2Client = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_EC2,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )

                LoggerUtility.logInfo('Fetching Snapshots in region: {}'.format(region))
                paginator = ec2Client.get_paginator(SnapshotConstants.DESCRIBE_SNAPSHOTS_METHOD_REFERENCE)
                operation_parameters = {SnapshotConstants.OWNER_IDS_REFERENCE: [SnapshotConstants.SELF_KEYWORD]}
                page_iterator = paginator.paginate(**operation_parameters)
                for page in page_iterator:
                    response = CommonUtility.changeDictionaryKeysToLowerCase(page)
                    snapshots = response[SnapshotConstants.SNAPSHOTS]
                    for snap in snapshots:
                        tags = CommonUtility.changeDictionaryKeysToLowerCase(ec2Client.describe_tags(
                            Filters=[
                                {
                                    SnapshotConstants.NAME_TAG: ResourceConstants.RESOURCE_ID_REFERNCE,
                                    SnapshotConstants.VALUES_TAG: [snap[SnapshotConstants.SNAPSHOT_ID]]
                                }
                            ]
                        ))
                        snap.update({TagsConstants.EC2_INSTANCE_TAGS: tags[TagsConstants.EC2_INSTANCE_TAGS]})
                        snap.update({ManagedCloudConstants.REGION_REFERENCE: region})
                        eventItems = self.__parseAndFetchSnapshotDetails(snap)
                        unencryptedSnapshot.append(eventItems)

        except KeyError as e:
            errorMessage = "KeyError occurred while fetching snapshots : {}".format(e)

        except ValueError as e:
            errorMessage = "ValueError occurred while fetching snapshots : {}".format(e)

        except AttributeError as e:
            errorMessage = "AttributeError occurred while fetching snapshots : {}".format(e)

        except ClientError as e:
            errorMessage = "Boto ClientError occurred while fetching snapshots : {}".format(e)

        except Exception as e:
            errorMessage = "Error occurred while fetching snapshots : {}".format(e)

        if not unencryptedSnapshot:
            LoggerUtility.logError(errorMessage)
            return False

        return unencryptedSnapshot
