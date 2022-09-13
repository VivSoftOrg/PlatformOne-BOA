locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

inputs = {
  aws_region = local.common.aws_region
}

generate "providers" {
  path      = "providers.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.common.aws_region}"
}
EOF
}

remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket = "${local.common.project}-${local.common.environment}-${local.common.aws_region}-tf-state"
    key    = format("${local.common.cluster_name}/%s/terraform.tfstate", path_relative_to_include())
    region = local.common.aws_region
    encrypt = true
  }
}
