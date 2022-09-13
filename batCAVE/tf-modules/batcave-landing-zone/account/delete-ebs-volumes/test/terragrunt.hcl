locals {
  common               = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
  lambda_name          = "delete_ebs_volumes"
  iam_path             = "/delegatedadmin/developer/"
  permissions_boundary = "arn:aws:iam::831579051573:policy/cms-cloud-admin/developer-boundary-policy"
  event_schedule_cron  = "cron(0 9 * * ? *)" #11 PM Hawaii time
  log_retention        = 30                  #CW logs retention in days
  lambda_timeout       = 300                 # Lambda timeout in seconds
  is_test              = get_aws_account_id() == "831579051573"
}

generate "providers" {
  path      = "providers.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.common.aws_region}"
}
EOF
}

remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket  = "${local.common.project}-${local.common.environment}-${local.common.aws_region}-tf-state"
    key     = format("${local.lambda_name}/%s/terraform.tfstate", path_relative_to_include())
    region  = "${local.common.aws_region}"
    encrypt = true
  }
}

dependency "vpc" {
  config_path = "../../vpc/"
}

terraform {
  source = (local.is_test ? "git::git@github.com:CMSgov/batcave-tf-misc-modules.git//delete_ebs_volumes" : null)
}

inputs = {
  aws_region           = local.common.aws_region
  lambda_name          = local.lambda_name
  environment          = local.common.environment
  project              = local.common.project
  iam_path             = local.iam_path
  permissions_boundary = local.permissions_boundary
  event_schedule_cron  = local.event_schedule_cron
  log_retention        = local.log_retention
  lambda_timeout       = local.lambda_timeout
  vpc_id               = dependency.vpc.outputs.vpc_id
  vpc_subnet_ids       = dependency.vpc.outputs.subnets.private.ids
}
