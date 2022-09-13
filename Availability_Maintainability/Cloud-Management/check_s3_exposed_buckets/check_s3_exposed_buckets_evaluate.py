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
""" This module will check whether the S3 bucket is publicly accessible or not. """
import json
from common.boto_utility import BotoUtility
from common.abstract_evaluate import AbstractEvaluator
from common.framework_objects import EvaluationResult
from common.i18n import Translation as _
from common.common_constants import BotoConstants
from common.common_constants import ComplianceConstants
from common.logger_utility import LoggerUtility
from common.common_constants import CommonKeywords, ManagedCloudConstants
from check_s3_exposed_buckets.check_s3_exposed_buckets_constants import Constants


class S3ExposedBucketsEvaluate(AbstractEvaluator):
    """ This class will be responsible for evaluating the resources. """
    def evaluate(self, eventItem):
        evaluationResult = EvaluationResult()
        awsPartitionName = self._AbstractEvaluator__eventParam.awsPartitionName
        s3Client = BotoUtility.getClient(
            BotoConstants.BOTO_CLIENT_AWS_S3,
            self._AbstractEvaluator__eventParam.accNo,
            BotoConstants.BOTO_CLIENT_READ_TYPE_ROLE,
            awsPartitionName,
            eventItem.configItems[ManagedCloudConstants.REGION_REFERENCE]
        )
        bucketName = eventItem.configItems[CommonKeywords.NAME_KEYWORD]
        grants = s3Client.get_bucket_acl(Bucket=bucketName)[Constants.GRANTS_KEYWORD]

        complianceType = ComplianceConstants.COMPLIANT_RESOURCE

        for acl in grants:
            if Constants.URI_KEYWORD in acl[Constants.GRANTEE_KEYWORD]:
                if acl[Constants.GRANTEE_KEYWORD][Constants.URI_KEYWORD].endswith(Constants.ALL_USERS_KEYWORD):
                    eventItem.configItems.update({CommonKeywords.REMOVE_ACL: True})
                    complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE

        wrongPolicy = True
        policy = ""
        try:
            policy = s3Client.get_bucket_policy(Bucket=bucketName)
        except Exception as e:
            LoggerUtility.logWarning("The bucket %s does not have policy attached" % (bucketName))

        if policy:
            policy = json.loads(policy[Constants.POLICY_KEYWORD])
            for statement in policy[Constants.STATEMENT_KEYWORD]:
                if 'Condition' in statement:
                    if 'StringEquals' in statement['Condition']:
                        if 'aws:sourceVpc' in statement['Condition']['StringEquals']:
                            if "*" not in statement['Condition']['StringEquals']['aws:sourceVpc']:
                                wrongPolicy = False

                if statement[Constants.EFFECT_KEYWORD] == Constants.ALLOW_KEYWORD and statement[Constants.PRINCIPAL_KEYWORD] == "*" and wrongPolicy:
                    LoggerUtility.logInfo("The bucket %s has policy attached" % (bucketName))
                    eventItem.configItems.update({CommonKeywords.REMOVE_POLICY: True})
                    complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE

        if complianceType == ComplianceConstants.COMPLIANT_RESOURCE:
            LoggerUtility.logInfo("The bucket %s is not publicly accessible" % (bucketName))
            evaluationResult.complianceType = ComplianceConstants.COMPLIANT_RESOURCE
            evaluationResult.annotation = _("The bucket %s is not publicly accessible" % (bucketName))
        else:
            LoggerUtility.logInfo("The bucket %s is publicly accessible" % (bucketName))
            evaluationResult.complianceType = ComplianceConstants.NON_COMPLIANT_RESOURCE
            evaluationResult.annotation = _("The bucket is publicly accessible")

        self._AbstractEvaluator__evaluatorMessage = evaluationResult.annotation
        return evaluationResult
