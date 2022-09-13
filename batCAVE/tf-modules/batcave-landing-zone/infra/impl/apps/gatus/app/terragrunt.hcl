locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

include "parent" {
  path = find_in_parent_folders()
}

dependency "gatus-storage" {
  config_path = "../storage"
  mock_outputs = {s3_buckets = {dummy = {}}}
}

include "vpc-dependency" {
  path = find_in_parent_folders("base/vpc/dependency.hcl")
}

include "gatus" {
  path = find_in_parent_folders("base/apps/gatus/terragrunt.hcl")
}

inputs = {
  #Environment specific config
}
