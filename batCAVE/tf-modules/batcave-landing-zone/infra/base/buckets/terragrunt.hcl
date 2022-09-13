locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals

  # Default to latest release unless overridden in <env>/common.hcl
  tf_buckets_ref = lookup(local.common, "tf_buckets_ref", "0.2.2")
}

terraform {
  source = "git::${local.common.tf_module_source}/batcave-tf-buckets.git//.?ref=${local.tf_buckets_ref}"
}

inputs = {
  tags = {
    cluster_name = local.common.cluster_name
  }
  force_destroy = false
}
