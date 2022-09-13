locals {
  common       = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

include {
  path = find_in_parent_folders()
}

terraform {
  source = "git::git@github.com:CMSgov/batcave-tf-buckets.git//.?ref=0.2.2"
}

inputs = {
  cluster_name = local.common.cluster_name
  s3_bucket_names = [
    "rapidfort-test-storage",
  ]
  tags = {
    cluster_name = local.common.cluster_name
  }
}
