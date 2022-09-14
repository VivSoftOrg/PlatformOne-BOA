locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

include "parent" {
  path = find_in_parent_folders()
}

terraform {
  source = "git::https://code.batcave.internal.cms.gov/batcave-iac/batcave-tf-sec-alerts.git"
}
