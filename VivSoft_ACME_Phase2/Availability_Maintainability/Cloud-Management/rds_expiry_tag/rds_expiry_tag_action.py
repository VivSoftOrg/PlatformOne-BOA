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
""" This module performs action on RDS instances """
from datetime import datetime
from botocore.exceptions import ClientError
from common.boto_utility import BotoUtility
from common.abstract_action import AbstractAction
from common.logger_utility import LoggerUtility
from common.common_constants import BotoConstants, ManagedCloudConstants, ComplianceConstants, ResourceConstants
from common.framework_objects import EvaluationResult
from common.date_validation_util import DateValidationUtil
from rds_expiry_tag.rds_expiry_tag_constants import Constants


class RdsExpiryTagAction(AbstractAction):
    """ This class performs an action if resource is non-compliant """

    def performAction(self, eventItem):
        """ This class performs an action if resource is non-compliant """
        try:

            evaluationResult = EvaluationResult()
            region = eventItem.configItems.get(ManagedCloudConstants.REGION_REFERENCE)
            awsPartitionName = self._AbstractAction__eventParam.awsPartitionName
            rdsClient = BotoUtility.getClient(
                BotoConstants.BOTO_CLIENT_AWS_RDS,
                self._AbstractAction__eventParam.accNo,
                BotoConstants.BOTO_CLIENT_WRITE_TYPE_ROLE,
                awsPartitionName,
                region
            )

            limit_expiration_date = int(self._AbstractAction__eventParam.configParam[Constants.LIMIT_EXPIRTION_DATE_REFERENCE])

            rdsName = eventItem.configItems.get('dbinstanceidentifier')
            current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            snapshotName = '%s-%s' % (rdsName, current_time)

            if eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_VALIDITY_EXPIRED:
                deleteRDSInstance = rdsClient.delete_db_instance(DBInstanceIdentifier=rdsName, SkipFinalSnapshot=False, FinalDBSnapshotIdentifier=snapshotName)
                if deleteRDSInstance[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                    LoggerUtility.logInfo("RDS Instance is deleted")
                    self._AbstractAction__actionMessage = "Your RDS instance has been deleted and the latest snapshot has been created for it."
                    evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
                    evaluationResult.annotation = "Deleted the RDS instance"
                    eventItem.configItems.update({'snapshotname': snapshotName})
                else:
                    LoggerUtility.logInfo("Unable to delete RDS Instance")
                    self._AbstractAction__actionMessage = "Unable to delete the RDS instance"
                    evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                    evaluationResult.annotation = "Unable to delete the RDS instance"

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] == ResourceConstants.RESOURCE_ABOUT_TO_EXPIRE:
                LoggerUtility.logInfo("Resource are about to expire")
                self._AbstractAction__actionMessage = "The RDS instances are about to expire"
                evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                evaluationResult.annotation = "The RDS instances are about to expire"

            elif eventItem.configItems[ComplianceConstants.NON_COMPLAINT_RESOURCE_ACTION] != ComplianceConstants.UNABLE_TO_CHECK_RESOURCE_COMPLIANCE:
                # Adding tags to resource
                rdsARN = eventItem.configItems.get('dbinstancearn')
                newExpirationDate = DateValidationUtil.addDaysToToday(limit_expiration_date)

                try:
                    tagsRespponse = rdsClient.add_tags_to_resource(
                        ResourceName=rdsARN,
                        Tags=[
                            {
                                'Key': 'ExpirationDate',
                                'Value': newExpirationDate,
                            },
                        ]
                    )
                    if tagsRespponse[BotoConstants.BOTO_RESPONSE_METADATA][BotoConstants.BOTO_RESPONSE_HTTP_STATUS_CODE] == 200:
                        LoggerUtility.logInfo("Tags Added to the RDS instance")
                        self._AbstractAction__actionMessage = "An ExpirationDate tag is added to the resource"
                        evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                        evaluationResult.annotation = "An ExpirationDate tag is added to the resource"
                    else:
                        LoggerUtility.logInfo("Unable to add the RDS instance")
                        self._AbstractAction__actionMessage = "An ExpirationDate tag is not added to the resource"
                        evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
                        evaluationResult.annotation = "An ExpirationDate tag is not added to the resource"

                except Exception as e:
                    LoggerUtility.logError(e)

        except ValueError as e:
            LoggerUtility.logError("The content of the object you tried to assign the value is invalid. {}".format(e))
            self._AbstractAction__actionMessage = "The content of the object you tried to assign the value is invalid. {}".format(e)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = "The content of the object you tried to assign the value is invalid. {}".format(e)
        except AttributeError as e:
            LoggerUtility.logError("Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e))
            self._AbstractAction__actionMessage = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = "Trying to access or call an attribute of a particular object type which it doesn’t possess. {}".format(e)
        except TypeError as e:
            LoggerUtility.logError("Attempt to call a function or use an operator on something of incorrect type. {}".format(e))
            self._AbstractAction__actionMessage = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = "Attempt to call a function or use an operator on something of incorrect type. {}".format(e)
        except NameError as e:
            LoggerUtility.logError("Trying to access a variable that you have not defined properly. {}".format(e))
            self._AbstractAction__actionMessage = "Trying to access a variable that you have not defined properly. {}".format(e)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = "Trying to access a variable that you have not defined properly. {}".format(e)
        except ClientError as e:
            LoggerUtility.logError("Boto client error occured. {}".format(e))
            self._AbstractAction__actionMessage = "Boto client error occured. {}".format(e)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = "Boto client error occured. {}".format(e)
        except Exception as e:
            LoggerUtility.logError("Error occured. {}".format(e))
            self._AbstractAction__actionMessage = "Error occured. {}".format(e)
            evaluationResult.complianceType = ComplianceConstants.MNC_ACTION_EXCEPTION
            evaluationResult.annotation = "Error occured. {}".format(e)

        return evaluationResult
