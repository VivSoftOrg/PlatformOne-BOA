locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals

  # Default to latest release unless overridden in <env>/common.hcl
  tf_vpc_ref = lookup(local.common, "tf_vpc_ref", "0.9.0")
}

terraform {
  source = "git::${local.common.tf_module_source}/batcave-tf-vpc.git//.?ref=${local.tf_vpc_ref}"
}

inputs = {
  env = local.common.environment
}
