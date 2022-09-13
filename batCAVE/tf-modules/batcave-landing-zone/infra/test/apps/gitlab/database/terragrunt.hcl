locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

include "parent" {
  path = find_in_parent_folders()
}

include "vpc-dependency" {
  path = "../../../../base/vpc/dependency.hcl"
}

include "eks-cluster-dependency" {
  path = "../../../../base/eks-cluster/dependency.hcl"
}

include "postgresql" {
  path = "../../../../base/postgresql/terragrunt.hcl"
}

inputs = {
  name                = local.common.cluster_name
  engine_version      = 13.4
  route53_zone_id     = "Z0780710QA4FMGA7MX3Y"
  route53_record_name = "db.batcave-test.internal.cms.gov"
  database_name       = "gitlab"
  master_username     = "gitlab"
  apply_immediately   = "false"
  skip_final_snapshot = "false"
}
