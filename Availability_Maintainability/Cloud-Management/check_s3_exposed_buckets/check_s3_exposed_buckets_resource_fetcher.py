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
""" This module will fetch all the S3 buckets from all the available regions """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import BotoConstants, CommonKeywords, AWSResourceClassConstants, TagsConstants, ManagedCloudConstants
from check_s3_exposed_buckets.check_s3_exposed_buckets_constants import Constants


class S3ExposedBucketsFetcher(AbstractResourceFetcher):
    """ This class is responsible for fetching the resources """
    def __parseAndFetchACLDetails(self, aclObject):
        """ This method will be used to fetch and parse ACL details. """
        configItems = aclObject
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=configItems[CommonKeywords.NAME_KEYWORD], resourceType=AWSResourceClassConstants.S3_BUCKET, configItems=configItems)

    def resourceFetcher(self):
        bucketList = []
        try:
            awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
            s3Client = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_S3,
                self._AbstractResourceFetcher__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName
            )
            buckets = s3Client.list_buckets()[Constants.BUCKETS_KEYWORD]

            for bucket in buckets:
                bucketAcl = {}
                region = s3Client.get_bucket_location(Bucket=bucket[BotoConstants.BOTO_CLIENT_AWS_EC2_NAME])
                # As per the location constraint column of bucket region table, we are using the below condition. Table reference : https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
                bucketRegion = Constants.US_EAST_1_REGION if region[Constants.LOCATION_CONSTRAINT_KEYWORD] is None else region[Constants.LOCATION_CONSTRAINT_KEYWORD]  # noqa
                s3RegionalClient = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_S3,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    bucketRegion)
                bucketAcl = s3RegionalClient.get_bucket_acl(Bucket=bucket[BotoConstants.BOTO_CLIENT_AWS_EC2_NAME])
                bucketAcl.update({CommonKeywords.NAME_KEYWORD: bucket[BotoConstants.BOTO_CLIENT_AWS_EC2_NAME]})
                bucketAcl.update({Constants.CREATION_DATE_KEYWORD: bucket[Constants.CREATION_DATE_REFERENCE]})
                try:
                    tags = CommonUtility.changeDictionaryKeysToLowerCase(s3Client.get_bucket_tagging(
                        Bucket=bucket[BotoConstants.BOTO_CLIENT_AWS_EC2_NAME])[Constants.TAG_SET_KEYWORD])
                    bucketAcl.update({TagsConstants.EC2_INSTANCE_TAGS: tags})
                except ClientError as e:
                    LoggerUtility.logWarning("Bucket does not have tags!")
                bucketAcl.update({ManagedCloudConstants.REGION_REFERENCE: bucketRegion})
                eventItems = self.__parseAndFetchACLDetails(bucketAcl)
                bucketList.append(eventItems)

        except KeyError as e:
            LoggerUtility.logError("KeyError occurred while fetching the S3 buckets {} ".format(e))
        except ValueError as e:
            LoggerUtility.logError("ValueError occurred while fetching the S3 buckets {} ".format(e))
        except AttributeError as e:
            LoggerUtility.logError("AttributeError occurred while fetching the S3 buckets {} ".format(e))
        except ClientError as e:
            LoggerUtility.logError("Boto ClientError occurred while fetching the S3 buckets {} ".format(e))
        except Exception as e:
            LoggerUtility.logError("Error occurred while fetching the S3 buckets {} ".format(e))
        return bucketList
