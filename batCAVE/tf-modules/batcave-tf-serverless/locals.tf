# Local variables used around the module
locals {
  # Naming
  service_name                  = var.service_name
  stage                         = var.environment
  resource_prefix               = "${local.stage}-${local.service_name}"
  iam_role_path                 = var.iam_role_path
  iam_role_permissions_boundary = var.iam_role_permissions_boundary

  # VPC
  vpc_id  = var.vpc_id
  subnets = var.private_subnets
}

data "aws_caller_identity" "current" {}
