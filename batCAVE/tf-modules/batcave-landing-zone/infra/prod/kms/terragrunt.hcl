locals {
  common   = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

include "parent" {
  path = find_in_parent_folders()
}

include "kms" {
  path   = "../../base/kms/terragrunt.hcl"
}

inputs = {
  # Environment Specific Config
}
