locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals

  # Default to latest release unless overridden in <env>/common.hcl
  tf_configmap_ref = lookup(local.common, "tf_configmap_ref", "1.0.0")

  # Store configmap_data in local to allow it to be merged (not just overwritten) on a per-env basis
  configmap_data = {
    aws_account_id       = get_aws_account_id()
    batcave_cluster_name = local.common.cluster_name
    batcave_base_domain  = local.common.base_domain
  }
}

terraform {
  source = "git::${local.common.tf_module_source}/batcave-tf-configmap.git//.?ref=${local.tf_configmap_ref}"
}

inputs = {
  cluster_name        = local.common.cluster_name
  configmap_name      = "terragrunt-vars"
  configmap_namespace = "batcave"
  configmap_data      = local.configmap_data
}
