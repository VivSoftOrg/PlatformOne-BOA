locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

include "parent" {
  path = find_in_parent_folders()
}

include "buckets" {
  path = find_in_parent_folders("base/buckets/terragrunt.hcl")
}

inputs = {
  s3_bucket_names = [
    "batcave-${local.common.cluster_name}-gatus"
  ]
  force_destroy = true
}

generate "config_object" {
  path = "config_object.tf"
  if_exists = "overwrite_terragrunt"
  contents = <<EOF
resource "aws_s3_object" "config" {
  bucket = aws_s3_bucket.landing_zone_buckets[var.s3_bucket_names[0]].id
  key    = "config.yaml"
  source = "config.yaml"
  etag = filemd5("config.yaml")
}
EOF
}
