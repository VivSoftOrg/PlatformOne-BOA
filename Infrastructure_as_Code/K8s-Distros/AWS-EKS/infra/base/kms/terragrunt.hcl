locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals

  tf_kms_ref = lookup(local.common, "tf_kms_ref", "0.1.0")
}

terraform {
  source = "git::${local.common.tf_module_source}/batcave-tf-kms.git//.?ref=${local.tf_kms_ref}"
}

inputs = {
  name                    = "${local.common.cluster_name}-sops"
  description             = "kms for sops encryption"
  deletion_window_in_days = "30" #7-30
}
