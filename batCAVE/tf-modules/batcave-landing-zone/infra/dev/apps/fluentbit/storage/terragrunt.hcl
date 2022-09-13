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
    # Bucket for storing log files
    "batcave-${local.common.cluster_name}-logs"
  ]
  force_destroy = true
}
