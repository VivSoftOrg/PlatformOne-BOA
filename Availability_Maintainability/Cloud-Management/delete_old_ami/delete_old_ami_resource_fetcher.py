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
from delete_old_ami.delete_old_ami_constants import AMIConstants
from common.boto_utility import BotoUtility
from common.abstract_resource_fetcher import AbstractResourceFetcher
from common.logger_utility import LoggerUtility
from common.compliance_object_factory import ComplianceObjectFactory
from common.common_utility import CommonUtility
from common.common_constants import BotoConstants


class DeleteOldAMIResourceFetcher(AbstractResourceFetcher):
    """ This class will fetch details of AMI which are not associated with LaunchConfiguration and  do not have doNotDelete tag. """

    def __parseAndFetchAmiDetails(self, amiObject):
        """Method will parse and fetch AMI details."""
        resourceId = amiObject[AMIConstants.Image_Id]
        configItems = CommonUtility.changeDictionaryKeysToLowerCase(amiObject)
        return ComplianceObjectFactory.createAWSConfigEventItemfrom(resourceId=resourceId, configItems=configItems)

    def __getLaunchConfigAMIList(self):
        """ Method to get AMI list associated with Launch configurations """
        lcImages = []
        awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
        regionsAS = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)
        for region in regionsAS:
            autoScalingClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_ASC,
                self._AbstractResourceFetcher__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                awsPartitionName,
                region
            )
            launchConfig = autoScalingClient.describe_launch_configurations()
            LoggerUtility.logInfo("Fetching Launch configuration AMI's in region: {}".format(region))
            if launchConfig[AMIConstants.RESPONSE_METADATA][AMIConstants.HTTP_STATUS_CODE] == 200:
                for lc in launchConfig['LaunchConfigurations']:
                    lcImages.append(lc[AMIConstants.Image_Id])
        lcImages = list(set(lcImages))
        return lcImages

    def resourceFetcher(self):
        amiList = []
        lcImages = []
        awsPartitionName = self._AbstractResourceFetcher__eventParam.awsPartitionName
        regionsEc2 = BotoUtility.getRegions(self._AbstractResourceFetcher__eventParam.accNo, awsPartitionName)

        try:

            lcImages = self.__getLaunchConfigAMIList()
            for region in regionsEc2:
                ec2Client = BotoUtility.getClient(
                    BotoConstants.BOTO_CLIENT_AWS_EC2,
                    self._AbstractResourceFetcher__eventParam.accNo,
                    BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
                    awsPartitionName,
                    region
                )

                response = ec2Client.describe_images(Owners=['self'], Filters=AMIConstants.AMI_FILTER)
                if response[AMIConstants.RESPONSE_METADATA][AMIConstants.HTTP_STATUS_CODE] == 200:
                    for image in response['Images']:
                        if image[AMIConstants.Image_Id] not in lcImages:
                            if "Tags" in image:
                                if AMIConstants.DO_NOT_DELETE_TAG in image['Tags']:
                                    continue
                            amiObject = image
                            amiObject.update({AMIConstants.AWS_REGION: region})
                            eventItems = self.__parseAndFetchAmiDetails(amiObject)
                            amiList.append(eventItems)

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
            LoggerUtility.logError("Error occured while fetching AMIs list for delete_old_ami rule. {}".format(e))

        return amiList
