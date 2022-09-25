locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

include "parent" {
  path = find_in_parent_folders()
}

generate "batcave_ecs_cluster" {
  path = "batcave-ecs-cluster.tf"
  if_exists = "overwrite_terragrunt"
  contents = <<EOF
resource "aws_ecs_cluster" "cluster" {
  name = "batcave"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}
EOF
}
