locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

include "parent" {
  path = find_in_parent_folders()
}

include "vpc" {
  path   = "../../base/vpc/terragrunt.hcl"
}

inputs = {
  # This module will look for a VPC named "<project>-east-<env>", populate the below accordingly
  project = "batcave"

  transport_subnets_exist = true
  shared_subnets_exist    = false
}
