locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

include "parent" {
  path = find_in_parent_folders()
}

include "buckets" {
  path = "../../../../base/buckets/terragrunt.hcl"
}

inputs = {
  s3_bucket_names = ["${local.common.cluster_name}-batcave-velero-storage"]
  force_destroy = true
}
