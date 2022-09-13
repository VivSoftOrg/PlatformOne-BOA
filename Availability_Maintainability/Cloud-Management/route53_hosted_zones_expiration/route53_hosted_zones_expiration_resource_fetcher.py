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
""" This module will fetch the resource details. """
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.common_utility import CommonUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_constants import BotoConstants, CommonKeywords, TagsConstants, AWSResourceClassConstants, ResourceConstants
from route53_hosted_zones_expiration.route53_hosted_zones_expiration_constants import Route53Constants


class HostedZoneExpirationResourceFetcher(AbstractResourceFetcher):
    """ This class is created for Fetching the resource details using Boto Client and provide the reource details to EventItem. """
    def __listHostedZones(self, hzClient):
        """This method will return list of hosted zones"""
        try:
            zoneList = []

            response = CommonUtility.changeDictionaryKeysToLowerCase(hzClient.list_hosted_zones())

            for zone in response[Route53Constants.HOSTED_ZONES]:
                zoneList.append(self.__parseAndFetchResource(zone, hzClient))

            while response[BotoConstants.BOTO_RESPONSE_IS_TRUNCATED]:
                response = CommonUtility.changeDictionaryKeysToLowerCase(
                    hzClient.list_hosted_zones(
                        Marker=response[BotoConstants.BOTO_RESPONSE_NEXT_MARKER]
                    )
                )

                for zone in response[Route53Constants.HOSTED_ZONES]:
                    zoneList.append(self.__parseAndFetchResource(zone, hzClient))

            return zoneList

        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            return False
        except Exception as e:
            LoggerUtility.logError("Error occured while {}".format(e))
            return False

    def __parseAndFetchResource(self, zone, hzClient):
        """Method will fetch instance details and assign it to configItems."""
        resourceId = zone[CommonKeywords.ID_KEYWORD].split('/')[2]
        LoggerUtility.logInfo(resourceId)
        # Error in "tagList", Please check the complete code once again.
        tagResponse = hzClient.list_tags_for_resource(
            ResourceType=Route53Constants.HOSTED_ZONES[:-1],
            ResourceId=resourceId
        )[Route53Constants.TAG_SET]
        tagList = CommonUtility.changeDictionaryKeysToLowerCase(tagResponse)[TagsConstants.TAG_LIST]
        configItems = {
            'tags': tagList,
            ResourceConstants.RESOURCE_TYPE_NAME: Route53Constants.RESOURCE_NAME
        }
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, resourceType=AWSResourceClassConstants.ROUTE53_HOSTED_ZONE, configItems=configItems)

    def resourceFetcher(self):
        hostedZonesList = []
        try:
            awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
            HZClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_ROUTE53,
                self._AbstractResourceFetcher__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName
            )

            LoggerUtility.logInfo('Fetching Hosted Zones.')

            hostedZonesList = self.__listHostedZones(HZClient)

        except ValueError as e:
            LoggerUtility.logError("The content of the object you tried to assign the value is Invalid. {}".format(e))
        except AttributeError as e:
            LoggerUtility.logError("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
        except TypeError as e:
            LoggerUtility.logError("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
        except NameError as e:
            LoggerUtility.logError("Trying to access a variable that you have not defined properly. {}".format(e))
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
        except Exception as e:
            LoggerUtility.logError("Error occured while fetching route53 hosted zones. {}".format(e))

        return hostedZonesList
