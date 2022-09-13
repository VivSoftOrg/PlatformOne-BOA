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
""" This module will fetch security groups present in all the available regions. """
from botocore.exceptions import ClientError

from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.boto_utility import BotoUtility
from common.common_constants import (AWSResourceClassConstants, BotoConstants,
                                     ResourceConstants, TagsConstants)
from common.common_utility import CommonUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.logger_utility import LoggerUtility
from delete_unused_security_group.delete_unused_security_group_constants import \
    SecurityGroupConstants


class DeleteUnusedSGResourceFetcher(AbstractResourceFetcher):
    """ This class is responsible for fetching the resources """

    def __parseAndFetchSGDetails(self, sgObject):
        """ This method is used for fetching and parsing resource details."""
        resourceId = sgObject[SecurityGroupConstants.SECURITY_GROUP_ID_KEYWORD]
        configItem = sgObject

        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.SG_RESOURCE, configItems=configItem)

    def resourceFetcher(self):
        allsgsList = []
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
                LoggerUtility.logInfo("Fetching Resources....")
                securityGroups = []
                secgrps = CommonUtility.changeDictionaryKeysToLowerCase(ec2Client.describe_security_groups())
                if secgrps.__contains__(SecurityGroupConstants.SECURITY_GROUP_KEYWORD):
                    securityGroups = secgrps[SecurityGroupConstants.SECURITY_GROUP_KEYWORD]
                for sgs in securityGroups:
                    sgObject = sgs
                    tags = CommonUtility.changeDictionaryKeysToLowerCase(ec2Client.describe_tags(
                        Filters=[
                            {
                                BotoConstants.BOTO_CLIENT_AWS_EC2_NAME: ResourceConstants.RESOURCE_ID_REFERNCE,
                                BotoConstants.BOTO_CLIENT_AWS_EC2_VALUES: [sgObject[SecurityGroupConstants.SECURITY_GROUP_ID_KEYWORD]]
                            }]))
                    sgObject.update({TagsConstants.EC2_INSTANCE_TAGS: tags[TagsConstants.EC2_INSTANCE_TAGS]})
                    sgObject.update({SecurityGroupConstants.REGION_KEYWORD: region})
                    eventItem = self.__parseAndFetchSGDetails(sgObject)
                    allsgsList.append(eventItem)

        except AttributeError as e:
            LoggerUtility.logError("AttributeError occurred while fetching the security groups: {}".format(e))
        except KeyError as e:
            LoggerUtility.logError("KeyError occurred while fetching the security groups: {}".format(e))
        except ValueError as e:
            LoggerUtility.logError("ValueError occurred while fetching the security groups: {}".format(e))
        except ClientError as e:
            LoggerUtility.logError("Boto ClientError occurred while fetching the security groups: {}".format(e))
        except Exception as e:
            LoggerUtility.logError("Error occurred while fetching the security groups: {}".format(e))
        return allsgsList
