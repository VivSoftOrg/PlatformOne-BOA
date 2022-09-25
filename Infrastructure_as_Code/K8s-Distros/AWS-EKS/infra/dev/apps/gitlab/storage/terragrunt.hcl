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
  s3_bucket_names = [
    # Bucket for storing gitlab backups artifacts
    "batcave-${local.common.cluster_name}-gitlab-storage"
  ]
  force_destroy = true
}
