locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
  frontend_cidrs = [
    "10.0.0.0/8",  #Internal for 10.x
    "100.0.0.0/8", #Internal for 100.x
  ]
  tf_serverless_ref = lookup(local.common, "tf_serverless_ref", "0.3.0")
}

terraform {
  source = "git::https://code.batcave.internal.cms.gov/batcave-iac/batcave-tf-serverless.git//.?ref=${local.tf_serverless_ref}"
  # Copy the lambda source code to the terragrunt scratch directory before running terraform plan or terraform apply
  before_hook "plan" {
    commands     = ["apply", "plan"]
    execute      = ["cp", "-a", "${get_repo_root()}/infra/base/apps/emm-healthcheck/lambda", "."]
  }
}

inputs = {
  environment                   = local.common.environment
  vpc_id                        = dependency.vpc.outputs.vpc_id
  private_subnets               = dependency.vpc.outputs.subnets.private.ids
  # Default the frontend subnets to the same as the private
  frontend_subnets              = dependency.vpc.outputs.subnets.private.ids
  ingress_prefix_lists          = []
  ingress_cidrs                 = local.frontend_cidrs
  base_domain                   = local.common.base_domain
  create_custom_domain          = true
  custom_subdomain              = "status"
  service_name                  = "emm-healthcheck"
  iam_role_permissions_boundary = local.common.permissions_boundary
  iam_role_path                 = local.common.iam_path
  lambda_path                   = "lambda"
  lambda_handler                = "index.lambdaHandler"
  lambda_timeout                = 10
  lambda_environment            = { BASE_DOMAIN = local.common.base_domain }
  ingress_sgs                   = [ dependency.eks-cluster.outputs.private_alb_security_group_id ]
}

