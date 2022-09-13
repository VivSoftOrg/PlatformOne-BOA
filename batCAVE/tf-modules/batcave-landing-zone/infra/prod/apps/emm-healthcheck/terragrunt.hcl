locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

include "parent" {
  path = find_in_parent_folders()
}

include "vpc-dependency" {
  path = "../../../base/vpc/dependency.hcl"
}

include "eks-dependency" {
  path = "../../../base/eks-cluster/dependency.hcl"
}

include "healthcheck" {
  path ="../../../base/apps/emm-healthcheck/terragrunt.hcl"
}

inputs = {
  frontend_subnets   = dependency.vpc.outputs.subnets.shared.ids
  lambda_environment = {
    BASE_DOMAIN = local.common.base_domain
    SIGNAL_URL  = "https://app.signal.internal.cms.gov/"
  }
}

