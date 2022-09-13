provider "aws" {
  version = "~> 2.25.0"
}

# We need to be able to create an IAM policy in the core account.
provider "aws" {
  alias   = "core"
  profile = "${local.core_aws_profile}"
}

data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}
data "aws_region" "current" {}
data "aws_availability_zones" "zones" {}

locals {
  platform_bucket  = "${coalesce(var.platform_bucket, "${lower(var.client_code)}-${lower(var.environment)}-${lower(var.project)}")}"
  core_aws_profile = "${coalesce(var.core_aws_profile, var.core_account_code)}"
  current_user_arn = "${length(split(":user/",data.aws_caller_identity.current.arn)) > 1 ? data.aws_caller_identity.current.arn : ""}"

  current_role_arn = "${length(split(":assumed-role/",data.aws_caller_identity.current.arn)) > 1 ?
        "arn:${data.aws_partition.current.partition}:iam::${data.aws_caller_identity.current.account_id}:role/${element(split("/", data.aws_caller_identity.current.arn), 1)}" :
        ""
    }"
}

data "terraform_remote_state" "core-iam" {
  backend = "s3"

  config {
    profile                = "${local.core_aws_profile}"
    bucket                 = "${local.platform_bucket}"
    key                    = "tfstate/${var.core_account_code}${lookup(var.tfstate_prefixes, "core-iam", var.default_tfstate_prefix)}/core-iam"
    encryption             = true
    skip_region_validation = true
  }
}

data "terraform_remote_state" "core-bucket" {
  backend = "s3"

  config {
    profile                = "${local.core_aws_profile}"
    bucket                 = "${local.platform_bucket}"
    key                    = "tfstate/${var.core_account_code}${lookup(var.tfstate_prefixes, "core-bucket", var.default_tfstate_prefix)}/core-bucket"
    encryption             = true
    skip_region_validation = true
  }
}

data "aws_iam_policy_document" "ec2-assumerole" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    principals = {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "dockerhost-assumerole" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    principals = {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }

  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    principals = {
      type        = "AWS"
      identifiers = ["${data.terraform_remote_state.core-iam.dockerhost_role_arn}"]
    }
  }
}

data "aws_iam_policy_document" "viv_softjenkins-assumerole" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    principals = {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }

  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    principals = {
      type = "AWS"

      identifiers = [
        "${data.terraform_remote_state.core-iam.viv_softjenkins_role_arn}",
        "${formatlist("arn:${data.aws_partition.current.partition}:iam::${var.core_account_id}:role/%s", compact(split(",",var.extra_jenkins_roles)))}",
      ]
    }
  }
}

resource "aws_iam_role" "auditinfra" {
  name                 = "${var.prefix}-auditinfra"
  assume_role_policy   = "${data.aws_iam_policy_document.viv_softjenkins-assumerole.json}"
  max_session_duration = "${60 * 60 * 12}"
}

resource "aws_iam_instance_profile" "auditinfra" {
  name = "${var.prefix}-auditinfra"
  role = "${aws_iam_role.auditinfra.name}"
}

resource "aws_iam_policy" "auditinfra" {
  name   = "${var.prefix}-auditinfra"
  policy = "${data.aws_iam_policy_document.auditinfra.json}"
}

resource "aws_iam_role_policy_attachment" "auditinfra" {
  role       = "${aws_iam_role.auditinfra.name}"
  policy_arn = "${aws_iam_policy.auditinfra.arn}"
}

data "aws_iam_policy_document" "auditinfra" {
  statement {
    effect = "Allow"

    actions = [
      "acm:DescribeCertificate",
      "acm:GetCertificate",
      "acm:ListCertificates",
      "appstream:Get*",
      "autoscaling:Describe*",
      "cloudformation:Describe*",
      "cloudformation:Get*",
      "cloudformation:List*",
      "cloudfront:Get*",
      "cloudfront:List*",
      "cloudsearch:Describe*",
      "cloudsearch:List*",
      "cloudtrail:DescribeTrails",
      "cloudtrail:GetTrailStatus",
      "cloudwatch:Describe*",
      "cloudwatch:Get*",
      "cloudwatch:List*",
      "codecommit:BatchGetRepositories",
      "codecommit:Get*",
      "codecommit:GitPull",
      "codecommit:List*",
      "codedeploy:Batch*",
      "codedeploy:Get*",
      "codedeploy:List*",
      "config:Deliver*",
      "config:Describe*",
      "config:Get*",
      "datapipeline:DescribeObjects",
      "datapipeline:DescribePipelines",
      "datapipeline:EvaluateExpression",
      "datapipeline:GetPipelineDefinition",
      "datapipeline:ListPipelines",
      "datapipeline:QueryObjects",
      "datapipeline:ValidatePipelineDefinition",
      "directconnect:Describe*",
      "dynamodb:BatchGetItem",
      "dynamodb:DescribeTable",
      "dynamodb:GetItem",
      "dynamodb:ListTables",
      "dynamodb:Query",
      "dynamodb:Scan",
      "ec2:Describe*",
      "ec2:GetConsoleOutput",
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:GetManifest",
      "ecr:DescribeRepositories",
      "ecr:ListImages",
      "ecr:BatchGetImage",
      "ecs:Describe*",
      "ecs:List*",
      "elasticache:Describe*",
      "elasticache:List*",
      "elasticbeanstalk:Check*",
      "elasticbeanstalk:Describe*",
      "elasticbeanstalk:List*",
      "elasticbeanstalk:RequestEnvironmentInfo",
      "elasticbeanstalk:RetrieveEnvironmentInfo",
      "elasticloadbalancing:Describe*",
      "elasticmapreduce:Describe*",
      "elasticmapreduce:List*",
      "elastictranscoder:List*",
      "elastictranscoder:Read*",
      "es:DescribeElasticsearchDomain",
      "es:DescribeElasticsearchDomains",
      "es:DescribeElasticsearchDomainConfig",
      "es:ListDomainNames",
      "es:ListTags",
      "es:ESHttpGet",
      "es:ESHttpHead",
      "events:DescribeRule",
      "events:ListRuleNamesByTarget",
      "events:ListRules",
      "events:ListTargetsByRule",
      "events:TestEventPattern",
      "firehose:Describe*",
      "firehose:List*",
      "glacier:ListVaults",
      "glacier:DescribeVault",
      "glacier:GetDataRetrievalPolicy",
      "glacier:GetVaultAccessPolicy",
      "glacier:GetVaultLock",
      "glacier:GetVaultNotifications",
      "glacier:ListJobs",
      "glacier:ListMultipartUploads",
      "glacier:ListParts",
      "glacier:ListTagsForVault",
      "glacier:DescribeJob",
      "glacier:GetJobOutput",
      "iam:GenerateCredentialReport",
      "iam:Get*",
      "iam:List*",
      "inspector:Describe*",
      "inspector:Get*",
      "inspector:List*",
      "inspector:LocalizeText",
      "inspector:PreviewAgentsForResourceGroup",
      "iot:Describe*",
      "iot:Get*",
      "iot:List*",
      "kinesis:Describe*",
      "kinesis:Get*",
      "kinesis:List*",
      "kms:Describe*",
      "kms:Get*",
      "kms:List*",
      "lambda:List*",
      "lambda:Get*",
      "logs:Describe*",
      "logs:Get*",
      "logs:TestMetricFilter",
      "mobilehub:GetProject",
      "mobilehub:ListAvailableFeatures",
      "mobilehub:ListAvailableRegions",
      "mobilehub:ListProjects",
      "mobilehub:ValidateProject",
      "mobilehub:VerifyServiceRole",
      "opsworks:Describe*",
      "opsworks:Get*",
      "rds:Describe*",
      "rds:ListTagsForResource",
      "redshift:Describe*",
      "redshift:ViewQueriesInConsole",
      "route53:Get*",
      "route53:List*",
      "route53domains:CheckDomainAvailability",
      "route53domains:GetDomainDetail",
      "route53domains:GetOperationDetail",
      "route53domains:ListDomains",
      "route53domains:ListOperations",
      "route53domains:ListTagsForDomain",
      "s3:Get*",
      "s3:List*",
      "sdb:GetAttributes",
      "sdb:List*",
      "sdb:Select*",
      "ses:Get*",
      "ses:List*",
      "sns:Get*",
      "sns:List*",
      "sqs:GetQueueAttributes",
      "sqs:ListQueues",
      "sqs:ReceiveMessage",
      "storagegateway:Describe*",
      "storagegateway:List*",
      "swf:Count*",
      "swf:Describe*",
      "swf:Get*",
      "swf:List*",
      "tag:Get*",
      "trustedadvisor:Describe*",
      "waf:Get*",
      "waf:List*",
      "workspaces:Describe*",
    ]

    resources = [
      "*",
    ]
  }
}

locals {
  platform_admin_users = ["${distinct(concat(slice(split(",", data.aws_caller_identity.current.arn), 1, 1), compact(split(",",var.platform_admin_users))))}"]

  kms_platform_admins = "${distinct(compact(concat(
            list(data.terraform_remote_state.core-bucket.platformadmin_role_arn,
                 "arn:${data.aws_partition.current.partition}:iam::${var.core_account_id}:root",
                 "arn:${data.aws_partition.current.partition}:iam::${data.aws_caller_identity.current.account_id}:root",
                 local.current_user_arn,
                 local.current_role_arn),
            formatlist("arn:${data.aws_partition.current.partition}:iam::${data.aws_caller_identity.current.account_id}:user/%s", compact(split(",",var.platform_admin_users))),
            formatlist("arn:${data.aws_partition.current.partition}:iam::${data.aws_caller_identity.current.account_id}:role/%s", compact(split(",", length(var.platform_admin_roles)>0 ? var.platform_admin_roles : "")))
        )))}"
}

data "aws_iam_user" "platformadmin" {
  count = "${length(local.platform_admin_users)}"

  user_name = "${element(local.platform_admin_users, count.index)}"
}

data "aws_iam_policy_document" "ssh-keys" {
  statement {
    sid       = "WorkloadAdmin"
    effect    = "Allow"
    actions   = ["kms:*"]
    resources = ["*"]

    principals = {
      type = "AWS"

      identifiers = [
        "${distinct(compact(concat(data.aws_iam_user.platformadmin.*.arn, local.kms_platform_admins)))}",
      ]
    }
  }

  statement {
    sid       = "CoreUse"
    effect    = "Allow"
    actions   = ["kms:Decrypt", "kms:DescribeKey"]
    resources = ["*"]

    principals = {
      type        = "AWS"
      identifiers = ["arn:${data.aws_partition.current.partition}:iam::${var.core_account_id}:root"]
    }
  }
}

resource "aws_kms_key" "ssh-keys" {
  description             = "SSH Keys for ${var.project}"
  deletion_window_in_days = 7
  policy                  = "${data.aws_iam_policy_document.ssh-keys.json}"
  enable_key_rotation     = "true" 

  tags {
    Name           = "${var.prefix}-workload-sshkeys"
    BuildUrl       = "${var.build_url}"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Project        = "${var.project}"
    Product        = "viv_soft Platform"
    ExpirationDate = "${var.expiration_date}"
  }

  # See https://github.com/terraform-providers/terraform-provider-aws/issues/245
  provisioner "local-exec" {
    command = "sleep 15" # FIXME: Terraform needs to close issue #245
  }
}

resource "aws_kms_alias" "ssh-keys" {
  name          = "alias/${var.prefix}-workload-sshkeys"
  target_key_id = "${aws_kms_key.ssh-keys.key_id}"

  provisioner "local-exec" {
    command = "sleep 15" # FIXME: Terraform needs to close issue #245
  }
}

# Allow access to workload sshkeys KMS in core, for decryption only.
data "aws_iam_policy_document" "workload-sshkeys-in-core" {
  provider = "aws.core"

  statement {
    sid       = "PlatformAdmin"
    effect    = "Allow"
    actions   = ["kms:Decrypt", "kms:DescribeKey"]
    resources = ["${aws_kms_key.ssh-keys.arn}"]
  }
}

# Allow access to workload sshkeys KMS in core, for decryption only.
resource "aws_iam_policy" "workload-sshkeys-in-core" {
  provider = "aws.core"

  name   = "${var.prefix}-${var.account_code}-workload-sshkeys"
  policy = "${data.aws_iam_policy_document.workload-sshkeys-in-core.json}"
}

# Allow access to workload sshkeys KMS in core, for decryption only.
resource "aws_iam_role_policy_attachment" "workload-sshkeys-in-core" {
  provider = "aws.core"

  role       = "${data.terraform_remote_state.core-bucket.platformadmin_role_name}"
  policy_arn = "${aws_iam_policy.workload-sshkeys-in-core.arn}"
}

# Allow access to workload sshkeys KMS in core, for decryption only.
resource "aws_iam_group_policy_attachment" "workload-sshkeys-in-core" {
  provider = "aws.core"

  group      = "${data.terraform_remote_state.core-bucket.platformadmin_group_name}"
  policy_arn = "${aws_iam_policy.workload-sshkeys-in-core.arn}"
}

resource "aws_iam_role" "s3-shared" {
  name               = "${var.prefix}-s3-shared"
  assume_role_policy = "${data.aws_iam_policy_document.ec2-assumerole.json}"
}

resource "aws_iam_instance_profile" "s3-shared" {
  name = "${var.prefix}-s3-shared"
  role = "${aws_iam_role.s3-shared.name}"
}

resource "aws_iam_policy" "s3-shared" {
  name   = "${var.prefix}-s3-shared"
  policy = "${data.aws_iam_policy_document.s3-shared.json}"
}

resource "aws_iam_role_policy_attachment" "s3-shared" {
  role       = "${aws_iam_role.s3-shared.name}"
  policy_arn = "${aws_iam_policy.s3-shared.arn}"
}

data "aws_iam_policy_document" "s3-shared" {
  statement {
    effect = "Allow"

    actions = [
      "s3:Get*",
      "s3:List*",
    ]

    resources = [
      "arn:${data.aws_partition.current.partition}:s3:::${local.platform_bucket}/shared",
      "arn:${data.aws_partition.current.partition}:s3:::${local.platform_bucket}/shared/*",
    ]
  }
}

resource "aws_kms_grant" "s3-shared-to-util-kms" {
  name              = "s3-shared-grant"
  key_id            = "${data.terraform_remote_state.core-bucket.util_kms_key_arn}"
  grantee_principal = "${aws_iam_role.s3-shared.arn}"
  operations        = ["DescribeKey", "Decrypt"]
}

resource "aws_iam_role" "tfdeploy" {
  name                 = "${var.prefix}-tfdeploy"
  assume_role_policy   = "${data.aws_iam_policy_document.viv_softjenkins-assumerole.json}"
  max_session_duration = "${60 * 60 * 12}"
}

resource "aws_iam_instance_profile" "tfdeploy" {
  name = "${var.prefix}-tfdeploy"
  role = "${aws_iam_role.tfdeploy.name}"
}

resource "aws_iam_policy" "tfdeploy" {
  name   = "${var.prefix}-tfdeploy"
  policy = "${data.aws_iam_policy_document.tfdeploy.json}"
}

resource "aws_iam_role_policy_attachment" "tfdeploy" {
  role       = "${aws_iam_role.tfdeploy.name}"
  policy_arn = "${aws_iam_policy.tfdeploy.arn}"
}

data "aws_iam_policy_document" "tfdeploy" {
  statement {
    effect = "Allow"

    not_actions = [
      "organizations:*",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "organizations:DescribeOrganization",
    ]

    resources = [
      "*",
    ]
  }
}

