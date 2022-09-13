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
import sys

sys.path.append('../../')

import common.compliance_object_factory as complianceobjectfactory
from common.abstract_evaluate import *
from common.common_constants import AWSResourceClassConstants
from unencrypted_rds.unencrypted_rds_evaluate import *

DB_ENCRYPTED_CONFIG_ITEM_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"configurationItemDiff\": {\"changedProperties\": {\"SupplementaryConfiguration.Tags.0\": {\"previousValue\": null,\"updatedValue\": {\"key\": \"RequiredTagsExpirationDate\",\"value\": \"2018-03-01\"},\"changeType\": \"CREATE\"}},\"changeType\": \"UPDATE\"},\"configurationItem\": {\"relatedEvents\": [],\"relationships\": [{\"resourceId\": \"default\",\"resourceName\": null,\"resourceType\": \"AWS::RDS::DBSubnetGroup\",\"name\": \"Is associated with DBSubnetGroup\"},{\"resourceId\": \"sg-339b7b45\",\"resourceName\": null,\"resourceType\": \"AWS::EC2::SecurityGroup\",\"name\": \"Is associated with SecurityGroup\"}],\"configuration\": {\"dBInstanceIdentifier\": \"demo\",\"dBInstanceClass\": \"db.t2.micro\",\"engine\": \"mysql\",\"dBInstanceStatus\": \"stopped\",\"masterUsername\": \"demo\",\"dBName\": \"demo\",\"endpoint\": {\"address\": \"demo.cmgtfpl1e4td.us-east-1.rds.amazonaws.com\",\"port\": 3306,\"hostedZoneId\": \"Z2R2ITUGPM61AM\"},\"allocatedStorage\": 20,\"instanceCreateTime\": \"2018-02-27T09:56:07.101Z\",\"preferredBackupWindow\": \"04:00-04:30\",\"backupRetentionPeriod\": 7,\"dBSecurityGroups\": [],\"vpcSecurityGroups\": [{\"vpcSecurityGroupId\": \"sg-339b7b45\",\"status\": \"active\"}],\"dBParameterGroups\": [{\"dBParameterGroupName\": \"default.mysql5.6\",\"parameterApplyStatus\": \"in-sync\"}],\"availabilityZone\": \"us-east-1d\",\"dBSubnetGroup\": {\"dBSubnetGroupName\": \"default\",\"dBSubnetGroupDescription\": \"default\",\"vpcId\": \"vpc-a25216da\",\"subnetGroupStatus\": \"Complete\",\"subnets\": [{\"subnetIdentifier\": \"subnet-87bc15da\",\"subnetAvailabilityZone\": {    \"name\": \"us-east-1c\"},\"subnetStatus\": \"Active\"},{\"subnetIdentifier\": \"subnet-c4bc08eb\",\"subnetAvailabilityZone\": {    \"name\": \"us-east-1a\"},\"subnetStatus\": \"Active\"},{\"subnetIdentifier\": \"subnet-3005900f\",\"subnetAvailabilityZone\": {    \"name\": \"us-east-1e\"},\"subnetStatus\": \"Active\"},{\"subnetIdentifier\": \"subnet-96a1be9a\",\"subnetAvailabilityZone\": {    \"name\": \"us-east-1f\"},\"subnetStatus\": \"Active\"},{\"subnetIdentifier\": \"subnet-0f611d6b\",\"subnetAvailabilityZone\": {    \"name\": \"us-east-1d\"},\"subnetStatus\": \"Active\"},{\"subnetIdentifier\": \"subnet-36c7b77d\",\"subnetAvailabilityZone\": {    \"name\": \"us-east-1b\"},\"subnetStatus\": \"Active\"}],\"dBSubnetGroupArn\": null},\"preferredMaintenanceWindow\": \"mon:08:43-mon:09:13\",\"pendingModifiedValues\": {\"dBInstanceClass\": null,\"allocatedStorage\": null,\"masterUserPassword\": null,\"port\": null,\"backupRetentionPeriod\": null,\"multiAZ\": null,\"engineVersion\": null,\"licenseModel\": null,\"iops\": null,\"dBInstanceIdentifier\": null,\"storageType\": null,\"cACertificateIdentifier\": null,\"dBSubnetGroupName\": null},\"latestRestorableTime\": \"2018-02-27T10:40:00.000Z\",\"multiAZ\": false,\"engineVersion\": \"5.6.37\",\"autoMinorVersionUpgrade\": true,\"readReplicaSourceDBInstanceIdentifier\": null,\"readReplicaDBInstanceIdentifiers\": [],\"readReplicaDBClusterIdentifiers\": [],\"licenseModel\": \"general-public-license\",\"iops\": null,\"optionGroupMemberships\": [{\"optionGroupName\": \"default:mysql-5-6\",\"status\": \"in-sync\"}],\"characterSetName\": null,\"secondaryAvailabilityZone\": null,\"publiclyAccessible\": true,\"statusInfos\": [],\"storageType\": \"gp2\",\"tdeCredentialArn\": null,\"dbInstancePort\": 0,\"dBClusterIdentifier\": null,\"storageEncrypted\": true,\"kmsKeyId\": null,\"dbiResourceId\": \"db-OKRZFFJJZYH5X2VPHY6NBXPLBY\",\"cACertificateIdentifier\": \"rds-ca-2015\",\"domainMemberships\": [],\"copyTagsToSnapshot\": false,\"monitoringInterval\": 0,\"enhancedMonitoringResourceArn\": null,\"monitoringRoleArn\": null,\"promotionTier\": null,\"dBInstanceArn\": \"arn:aws:rds:us-east-1:693265998683:db:demo\",\"timezone\": null,\"iAMDatabaseAuthenticationEnabled\": false,\"performanceInsightsEnabled\": false,\"performanceInsightsKMSKeyId\": null},\"supplementaryConfiguration\": {\"Tags\": [{\"key\": \"workload-type\",\"value\": \"other\"},{\"key\": \"RequiredTagsExpirationDate\",\"value\": \"2018-03-01\"}]},\"tags\": {\"workload-type\": \"other\",\"RequiredTagsExpirationDate\": \"2018-03-01\"},\"configurationItemVersion\": \"1.3\",\"configurationItemCaptureTime\": \"2018-02-27T18:18:48.143Z\",\"configurationStateId\": 1519755528143,\"awsAccountId\": \"693265998683\",\"configurationItemStatus\": \"OK\",\"resourceType\": \"AWS::RDS::DBInstance\",\"resourceId\": \"db-OKRZFFJJZYH5X2VPHY6NBXPLBY\",\"resourceName\": \"demo\",\"ARN\": \"arn:aws:rds:us-east-1:693265998683:db:demo\",\"awsRegion\": \"us-east-1\",\"availabilityZone\": \"us-east-1d\",\"configurationStateMd5Hash\": \"\",\"resourceCreationTime\": \"2018-02-27T09:56:07.101Z\"},\"notificationCreationTime\": \"2018-02-27T18:18:48.617Z\",\"messageType\": \"ConfigurationItemChangeNotification\",\"recordVersion\": \"1.3\"}",
    "ruleParameters": "{\"customerName\":\"MNC-Client\",\"performAction\": \"False\", \"actionName\": \"UnencryptedRdsAction\", \"evaluateName\": \"UnencryptedRdsEvaluate\",   \"resourceFetcherName\" : \"UnencryptedRdsResourceFetcher\",  \"moduleName\": \"unencrypted_rds\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\"}",
    "resultToken": "",
    "configRuleName": "unencrypted_rds",
    "configRuleId": "config-rule-nvphxd",
    "accountId": "693265998683",
    "executionRoleArn": "arn:aws:iam::411815166437:role/awsconfig-role",
    "configRuleArn": "arn:aws:config:us-east-1:411815166437:config-rule/config-rule-1v52mx"
}

DB_NOT_ENCRYPTED_CONFIG_ITEM_JSON = {
    "version": "1.0",
    "invokingEvent": "{\"configurationItemDiff\": {\"changedProperties\": {\"SupplementaryConfiguration.Tags.0\": {\"previousValue\": null,\"updatedValue\": {\"key\": \"RequiredTagsExpirationDate\",\"value\": \"2018-03-01\"},\"changeType\": \"CREATE\"}},\"changeType\": \"UPDATE\"},\"configurationItem\": {\"relatedEvents\": [],\"relationships\": [{\"resourceId\": \"default\",\"resourceName\": null,\"resourceType\": \"AWS::RDS::DBSubnetGroup\",\"name\": \"Is associated with DBSubnetGroup\"},{\"resourceId\": \"sg-339b7b45\",\"resourceName\": null,\"resourceType\": \"AWS::EC2::SecurityGroup\",\"name\": \"Is associated with SecurityGroup\"}],\"configuration\": {\"dBInstanceIdentifier\": \"demo\",\"dBInstanceClass\": \"db.t2.micro\",\"engine\": \"mysql\",\"dBInstanceStatus\": \"stopped\",\"masterUsername\": \"demo\",\"dBName\": \"demo\",\"endpoint\": {\"address\": \"demo.cmgtfpl1e4td.us-east-1.rds.amazonaws.com\",\"port\": 3306,\"hostedZoneId\": \"Z2R2ITUGPM61AM\"},\"allocatedStorage\": 20,\"instanceCreateTime\": \"2018-02-27T09:56:07.101Z\",\"preferredBackupWindow\": \"04:00-04:30\",\"backupRetentionPeriod\": 7,\"dBSecurityGroups\": [],\"vpcSecurityGroups\": [{\"vpcSecurityGroupId\": \"sg-339b7b45\",\"status\": \"active\"}],\"dBParameterGroups\": [{\"dBParameterGroupName\": \"default.mysql5.6\",\"parameterApplyStatus\": \"in-sync\"}],\"availabilityZone\": \"us-east-1d\",\"dBSubnetGroup\": {\"dBSubnetGroupName\": \"default\",\"dBSubnetGroupDescription\": \"default\",\"vpcId\": \"vpc-a25216da\",\"subnetGroupStatus\": \"Complete\",\"subnets\": [{\"subnetIdentifier\": \"subnet-87bc15da\",\"subnetAvailabilityZone\": {    \"name\": \"us-east-1c\"},\"subnetStatus\": \"Active\"},{\"subnetIdentifier\": \"subnet-c4bc08eb\",\"subnetAvailabilityZone\": {    \"name\": \"us-east-1a\"},\"subnetStatus\": \"Active\"},{\"subnetIdentifier\": \"subnet-3005900f\",\"subnetAvailabilityZone\": {    \"name\": \"us-east-1e\"},\"subnetStatus\": \"Active\"},{\"subnetIdentifier\": \"subnet-96a1be9a\",\"subnetAvailabilityZone\": {    \"name\": \"us-east-1f\"},\"subnetStatus\": \"Active\"},{\"subnetIdentifier\": \"subnet-0f611d6b\",\"subnetAvailabilityZone\": {    \"name\": \"us-east-1d\"},\"subnetStatus\": \"Active\"},{\"subnetIdentifier\": \"subnet-36c7b77d\",\"subnetAvailabilityZone\": {    \"name\": \"us-east-1b\"},\"subnetStatus\": \"Active\"}],\"dBSubnetGroupArn\": null},\"preferredMaintenanceWindow\": \"mon:08:43-mon:09:13\",\"pendingModifiedValues\": {\"dBInstanceClass\": null,\"allocatedStorage\": null,\"masterUserPassword\": null,\"port\": null,\"backupRetentionPeriod\": null,\"multiAZ\": null,\"engineVersion\": null,\"licenseModel\": null,\"iops\": null,\"dBInstanceIdentifier\": null,\"storageType\": null,\"cACertificateIdentifier\": null,\"dBSubnetGroupName\": null},\"latestRestorableTime\": \"2018-02-27T10:40:00.000Z\",\"multiAZ\": false,\"engineVersion\": \"5.6.37\",\"autoMinorVersionUpgrade\": true,\"readReplicaSourceDBInstanceIdentifier\": null,\"readReplicaDBInstanceIdentifiers\": [],\"readReplicaDBClusterIdentifiers\": [],\"licenseModel\": \"general-public-license\",\"iops\": null,\"optionGroupMemberships\": [{\"optionGroupName\": \"default:mysql-5-6\",\"status\": \"in-sync\"}],\"characterSetName\": null,\"secondaryAvailabilityZone\": null,\"publiclyAccessible\": true,\"statusInfos\": [],\"storageType\": \"gp2\",\"tdeCredentialArn\": null,\"dbInstancePort\": 0,\"dBClusterIdentifier\": null,\"storageEncrypted\": false,\"kmsKeyId\": null,\"dbiResourceId\": \"db-OKRZFFJJZYH5X2VPHY6NBXPLBY\",\"cACertificateIdentifier\": \"rds-ca-2015\",\"domainMemberships\": [],\"copyTagsToSnapshot\": false,\"monitoringInterval\": 0,\"enhancedMonitoringResourceArn\": null,\"monitoringRoleArn\": null,\"promotionTier\": null,\"dBInstanceArn\": \"arn:aws:rds:us-east-1:693265998683:db:demo\",\"timezone\": null,\"iAMDatabaseAuthenticationEnabled\": false,\"performanceInsightsEnabled\": false,\"performanceInsightsKMSKeyId\": null},\"supplementaryConfiguration\": {\"Tags\": [{\"key\": \"workload-type\",\"value\": \"other\"},{\"key\": \"RequiredTagsExpirationDate\",\"value\": \"2018-03-01\"}]},\"tags\": {\"workload-type\": \"other\",\"RequiredTagsExpirationDate\": \"2018-03-01\"},\"configurationItemVersion\": \"1.3\",\"configurationItemCaptureTime\": \"2018-02-27T18:18:48.143Z\",\"configurationStateId\": 1519755528143,\"awsAccountId\": \"693265998683\",\"configurationItemStatus\": \"OK\",\"resourceType\": \"AWS::RDS::DBInstance\",\"resourceId\": \"db-OKRZFFJJZYH5X2VPHY6NBXPLBY\",\"resourceName\": \"demo\",\"ARN\": \"arn:aws:rds:us-east-1:693265998683:db:demo\",\"awsRegion\": \"us-east-1\",\"availabilityZone\": \"us-east-1d\",\"configurationStateMd5Hash\": \"\",\"resourceCreationTime\": \"2018-02-27T09:56:07.101Z\"},\"notificationCreationTime\": \"2018-02-27T18:18:48.617Z\",\"messageType\": \"ConfigurationItemChangeNotification\",\"recordVersion\": \"1.3\"}",
    "ruleParameters": "{\"customerName\":\"MNC-Client\",\"performAction\": \"False\", \"actionName\": \"UnencryptedRdsAction\", \"evaluateName\": \"UnencryptedRdsEvaluate\",   \"resourceFetcherName\" : \"UnencryptedRdsResourceFetcher\",  \"moduleName\": \"unencrypted_rds\", \n \"notifier\":\"ses\",\n \"toEmail\": \"devendra.suthar@reancloud.com\",\n \"ccEmail\": \"devendra.suthar@reancloud.com\"}",
    "resultToken": "",
    "configRuleName": "unencrypted_rds",
    "configRuleId": "config-rule-nvphxd",
    "accountId": "693265998683",
    "executionRoleArn": "arn:aws:iam::411815166437:role/awsconfig-role",
    "configRuleArn": "arn:aws:config:us-east-1:411815166437:config-rule/config-rule-1v52mx"
}

CONTEXT = ""
RESOURCE_TYPE = AWSResourceClassConstants.RDS_INSTANCE
RESOURCE_ID = 'InstanceId'

class TestUnencryptedRdsEvaluate(object):

    def testEvaluateForRdsStorageNotEncrypted(self):
        self._AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            DB_NOT_ENCRYPTED_CONFIG_ITEM_JSON,
            CONTEXT
        )
        eventItem = complianceobjectfactory.ComplianceObjectFactory.createEventItemFrom(DB_NOT_ENCRYPTED_CONFIG_ITEM_JSON, CONTEXT, self._AbstractEvaluator__eventParam)
        evaluationResult = UnencryptedRdsEvaluate(self._AbstractEvaluator__eventParam).evaluate(eventItem[0])
        assert evaluationResult.complianceType == ComplianceConstants.NON_COMPLIANT_RESOURCE

    def testEvaluateForRdsStorageEncrypted(self):
        self._AbstractEvaluator__eventParam = complianceobjectfactory.ComplianceObjectFactory.createEventParamFrom(
            DB_ENCRYPTED_CONFIG_ITEM_JSON,
            CONTEXT
        )
        eventItem = complianceobjectfactory.ComplianceObjectFactory.createEventItemFrom(DB_ENCRYPTED_CONFIG_ITEM_JSON, CONTEXT, self._AbstractEvaluator__eventParam)
        evaluationResult = UnencryptedRdsEvaluate(self._AbstractEvaluator__eventParam).evaluate(eventItem[0])
        assert evaluationResult.complianceType == ComplianceConstants.COMPLIANT_RESOURCE
