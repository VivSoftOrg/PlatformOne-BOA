provider "aws" {
  version = "~> 2.25.0"
}

data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}
data "aws_region" "current" {}
data "aws_elb_service_account" "current" {}

locals {
  platform_bucket  = "${coalesce(var.platform_bucket, "${lower(var.client_code)}-${lower(var.environment)}-${lower(var.project)}")}"
  elb_logs_bucket  = "${coalesce(var.elb_logs_bucket, "${lower(var.client_code)}-${lower(var.prefix)}")}-elb-logs"
  current_user_arn = "${length(split(":user/",data.aws_caller_identity.current.arn)) > 1 ? data.aws_caller_identity.current.arn : ""}"

  current_role_arn = "${length(split(":assumed-role/",data.aws_caller_identity.current.arn)) > 1 ?
        "arn:${data.aws_partition.current.partition}:iam::${data.aws_caller_identity.current.account_id}:role/${element(split("/", data.aws_caller_identity.current.arn), 1)}" :
        ""
    }"
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

data "terraform_remote_state" "core-bucket" {
  backend = "s3"

  config {
    bucket                 = "${local.platform_bucket}"
    key                    = "tfstate/${var.account_code}${lookup(var.tfstate_prefixes, "core-bucket", var.default_tfstate_prefix)}/core-bucket"
    encryption             = true
    skip_region_validation = true
  }
}

resource "aws_iam_role" "dockerhost" {
  name               = "${var.prefix}-dockerhost"
  assume_role_policy = "${data.aws_iam_policy_document.ec2-assumerole.json}"
}

resource "aws_iam_instance_profile" "dockerhost" {
  name = "${var.prefix}-dockerhost"
  role = "${aws_iam_role.dockerhost.name}"
}


data "aws_iam_policy_document" "dockerhost-attachebs" {
  statement {
    effect = "Allow"

    actions = [
      "ec2:DescribeVolumes",
    ]

    resources = ["*"]
  }

  statement {
    effect = "Allow"

    actions = [
      "ec2:AttachVolume",
      "ec2:DetachVolume",
    ]

    resources = [
      "arn:${data.aws_partition.current.partition}:ec2:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:volume/*",
      "arn:${data.aws_partition.current.partition}:ec2:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:instance/*",
    ]

    condition {
      test     = "StringLike"
      variable = "ec2:ResourceTag/Name"

      values = [
        "viv_softhome",
        "viv_softhome*",
        "viv_softPlatform-HOME",
        "viv_softPlatform-HOME*",
        "${var.environment}*-${var.project}-dockerhost",
        "${var.environment}*-${var.project}-dockerhost*",
        "${var.environment}*-${var.project}-HOME",
        "${var.environment}*-${var.project}-HOME*",
      ]
    }
  }
}

resource "aws_iam_policy" "dockerhost-attachebs" {
  name   = "${var.prefix}-dockerhost-attachebs"
  policy = "${data.aws_iam_policy_document.dockerhost-attachebs.json}"
}

resource "aws_iam_role_policy_attachment" "dockerhost-attachebs" {
  role       = "${aws_iam_role.dockerhost.name}"
  policy_arn = "${aws_iam_policy.dockerhost-attachebs.arn}"
}

resource "aws_iam_role_policy_attachment" "dockerhost-cloudwatch_logs_write_access" {
  role       = "${aws_iam_role.dockerhost.name}"
  policy_arn = "${aws_iam_policy.cloudwatch_logs_write_access-policy.arn}"
}

resource "aws_iam_policy" "dockerhost-s3-access" {
  name   = "${var.prefix}-dockerhost-s3-access"
  policy = "${data.aws_iam_policy_document.dockerhost-s3-access.json}"
}

resource "aws_iam_role_policy_attachment" "dockerhost-s3-access" {
  role       = "${aws_iam_role.dockerhost.name}"
  policy_arn = "${aws_iam_policy.dockerhost-s3-access.arn}"
}

data "aws_iam_policy_document" "dockerhost-s3-access" {
  statement {
    effect = "Allow"

    actions = [
      "s3:Get*",
      "s3:List*",
    ]

    resources = [
      "arn:${data.aws_partition.current.partition}:s3:::${local.platform_bucket}/shared",
      "arn:${data.aws_partition.current.partition}:s3:::${local.platform_bucket}/shared/*",
      "arn:${data.aws_partition.current.partition}:s3:::${local.platform_bucket}/config",
      "arn:${data.aws_partition.current.partition}:s3:::${local.platform_bucket}/config/*",
    ]
  }

}

resource "aws_iam_role_policy_attachment" "dockerhost-ssm" {
  count      = "${var.enable_ssm ? 1 : 0}"
  role       = "${aws_iam_role.dockerhost.name}"
  policy_arn = "${aws_iam_policy.ssm_core_policy.arn}"
}

resource "aws_s3_bucket" "elb_access_logs_bucket" {
  bucket = "${local.elb_logs_bucket}"
  acl    = "private"

  tags {
    "Name"        = "${local.elb_logs_bucket}"
    "Environment" = "${var.environment}"
    "Owner"       = "${var.owner}"
    "Project"     = "${var.project}"
    "Product"     = "viv_soft Platform"
    "ExpirationDate" = "${var.expiration_date}"
  }
}

data "aws_iam_policy_document" "elb_logs" {
  statement {
    sid       = "elb-logs-write"
    effect    = "Allow"
    actions   = ["s3:PutObject"]
    resources = ["arn:${data.aws_partition.current.partition}:s3:::${local.elb_logs_bucket}/*"]

    principals = {
      type        = "AWS"
      identifiers = ["${data.aws_elb_service_account.current.arn}"]
    }
  }
}

resource "aws_s3_bucket_policy" "elb_logs" {
  bucket = "${aws_s3_bucket.elb_access_logs_bucket.id}"
  policy = "${data.aws_iam_policy_document.elb_logs.json}"
}

locals {
  kms_platform_admins = "${distinct(compact(concat(
            list(data.terraform_remote_state.core-bucket.platformadmin_role_arn,
                 "arn:${data.aws_partition.current.partition}:iam::${data.aws_caller_identity.current.account_id}:root",
                 local.current_user_arn,
                 local.current_role_arn),
            formatlist("arn:${data.aws_partition.current.partition}:iam::${data.aws_caller_identity.current.account_id}:user/%s", compact(split(",",var.platform_admin_users))),
            formatlist("arn:${data.aws_partition.current.partition}:iam::${data.aws_caller_identity.current.account_id}:role/%s", compact(split(",", length(var.platform_admin_roles)>0 ? var.platform_admin_roles : "")))
        )))}"
}

data "aws_iam_policy_document" "ssh-keys" {
  statement {
    sid       = "platform-admin"
    effect    = "Allow"
    actions   = ["kms:*"]
    resources = ["*"]

    principals = {
      type        = "AWS"
      identifiers = ["${local.kms_platform_admins}"]
    }
  }
}

resource "aws_kms_key" "ssh-keys" {
  description             = "SSH Keys for ${var.project}"
  deletion_window_in_days = 7
  policy                  = "${data.aws_iam_policy_document.ssh-keys.json}"
  enable_key_rotation     = "true"

  tags {
    Name           = "${var.prefix}-core-sshkeys"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Project        = "${var.project}"
    Product        = "viv_soft Platform"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }

  # See https://github.com/terraform-providers/terraform-provider-aws/issues/245
  provisioner "local-exec" {
    command = "sleep 15" # FIXME: Terraform needs to close issue #245
  }
}

resource "aws_kms_alias" "ssh-keys" {
  name          = "alias/${var.prefix}-core-sshkeys"
  target_key_id = "${aws_kms_key.ssh-keys.key_id}"

  provisioner "local-exec" {
    command = "sleep 15" # FIXME: Terraform needs to close issue #245
  }
}

data "aws_iam_policy_document" "kms-platform-service" {
  statement {
    sid    = "platform-admin"
    effect = "Allow"

    actions = [
      "kms:Create*",
      "kms:Describe*",
      "kms:Enable*",
      "kms:List*",
      "kms:Put*",
      "kms:Update*",
      "kms:Revoke*",
      "kms:Disable*",
      "kms:Get*",
      "kms:Delete*",
      "kms:ScheduleKeyDeletion",
      "kms:CancelKeyDeletion",
      "kms:TagResource",
      "kms:UnTagResource",
    ]

    resources = ["*"]

    principals = {
      type        = "AWS"
      identifiers = ["${local.kms_platform_admins}"]
    }
  }

  statement {
    sid    = "platform-use"
    effect = "Allow"

    actions = [
      "kms:Encrypt",
      "kms:Decrypt",
      "kms:ReEncrypt*",
      "kms:GenerateDataKey*",
      "kms:DescribeKey",
    ]

    resources = ["*"]

    principals = {
      type        = "AWS"
      identifiers = ["${local.kms_platform_admins}"]
    }
  }

  statement {
    sid    = "aws-grant"
    effect = "Allow"

    actions = [
      "kms:CreateGrant",
      "kms:ListGrants",
      "kms:RevokeGrant",
    ]

    resources = ["*"]

    principals = {
      type        = "AWS"
      identifiers = ["${local.kms_platform_admins}", "${aws_iam_role.dockerhost.arn}"]
    }

    condition = {
      test     = "Bool"
      variable = "kms:GrantIsForAWSResource"
      values   = ["true"]
    }
  }
}

resource "aws_kms_key" "rds" {
  description             = "RDS for ${var.project}"
  deletion_window_in_days = 7
  policy                  = "${data.aws_iam_policy_document.kms-platform-service.json}"
  enable_key_rotation     = "true"

  tags {
    Name           = "${var.prefix}-RDS"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Project        = "${var.project}"
    Product        = "viv_soft Platform"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }

  # See https://github.com/terraform-providers/terraform-provider-aws/issues/245
  provisioner "local-exec" {
    command = "sleep 15" # FIXME: Terraform needs to close issue #245
  }
}

resource "aws_kms_alias" "rds" {
  name          = "alias/${var.prefix}-RDS"
  target_key_id = "${aws_kms_key.rds.key_id}"
}

resource "aws_kms_key" "ebs" {
  description             = "EBS for ${var.project}"
  deletion_window_in_days = 7
  policy                  = "${data.aws_iam_policy_document.kms-platform-service.json}"
  enable_key_rotation     = "true"

  tags {
    Name           = "${var.prefix}-EBS"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Project        = "${var.project}"
    Product        = "viv_soft Platform"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }

  # See https://github.com/terraform-providers/terraform-provider-aws/issues/245
  provisioner "local-exec" {
    command = "sleep 15" # FIXME: Terraform needs to close issue #245
  }
}

resource "aws_kms_alias" "ebs" {
  name          = "alias/${var.prefix}-EBS"
  target_key_id = "${aws_kms_key.ebs.key_id}"
}

resource "aws_iam_policy" "ssm_core_policy" {
  count      = "${var.enable_ssm ? 1 : 0}"
  name   = "${var.prefix}-ssm-instance"
  policy = "${data.aws_iam_policy_document.ssm_core_policy_data.json}"
}

locals {
  jenkins_assumable_roles = "${compact(list(
            "arn:${data.aws_partition.current.partition}:iam::*:role/${var.prefix}-auditinfra",
            "arn:${data.aws_partition.current.partition}:iam::*:role/${var.prefix}-viv_softbakery",
            var.jenkins_allow_tfdeploy ? "arn:${data.aws_partition.current.partition}:iam::*:role/${var.prefix}-tfdeploy" : ""
        ))}"
}

resource "aws_iam_role" "viv_softjenkins" {
  name               = "${var.prefix}-viv_softjenkins"
  assume_role_policy = "${data.aws_iam_policy_document.ec2-assumerole.json}"
}

resource "aws_iam_instance_profile" "viv_softjenkins" {
  name = "${var.prefix}-viv_softjenkins"
  role = "${aws_iam_role.viv_softjenkins.name}"
}

data "aws_iam_policy_document" "viv_softjenkins-assumerole-core" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    resources = ["${local.jenkins_assumable_roles}"]
  }
}

resource "aws_iam_policy" "viv_softjenkins-assumerole-core" {
  name   = "${var.prefix}-viv_softjenkins-assumerole-core"
  policy = "${data.aws_iam_policy_document.viv_softjenkins-assumerole-core.json}"
}

resource "aws_iam_role_policy_attachment" "viv_softjenkins-assumerole-core" {
  role       = "${aws_iam_role.viv_softjenkins.name}"
  policy_arn = "${aws_iam_policy.viv_softjenkins-assumerole-core.arn}"
}

data "aws_iam_policy_document" "viv_softjenkins-attachebs" {
  statement {
    effect = "Allow"

    actions = [
      "ec2:DescribeVolumes",
    ]

    resources = ["*"]
  }

  statement {
    effect = "Allow"

    actions = [
      "ec2:AttachVolume",
      "ec2:DetachVolume",
    ]

    resources = [
      "arn:${data.aws_partition.current.partition}:ec2:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:volume/*",
      "arn:${data.aws_partition.current.partition}:ec2:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:instance/*",
    ]

    condition {
      test     = "StringLike"
      variable = "ec2:ResourceTag/Name"

      values = [
        "dev",
        "qa",
        "prod",
        "viv_softjenkinshome",
        "viv_softjenkins*",
        "viv_softJenkins-HOME",
        "viv_softJenkins*",
        "${var.environment}*-${var.project}-viv_softJenkins",
        "${var.environment}*-${var.project}-viv_softJenkins*",
      ]
    }
  }
}

resource "aws_iam_policy" "viv_softjenkins-attachebs" {
  name   = "${var.prefix}-viv_softjenkins-attachebs"
  policy = "${data.aws_iam_policy_document.viv_softjenkins-attachebs.json}"
}

resource "aws_iam_role_policy_attachment" "viv_softjenkins-attachebs" {
  role       = "${aws_iam_role.viv_softjenkins.name}"
  policy_arn = "${aws_iam_policy.viv_softjenkins-attachebs.arn}"
}
