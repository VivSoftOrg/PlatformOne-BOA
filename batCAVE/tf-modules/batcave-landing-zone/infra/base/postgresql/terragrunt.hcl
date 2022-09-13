locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals

  # Default to latest release unless overridden in <env>/common.hcl
  tf_postgresql_ref = lookup(local.common, "tf_postgresql_ref", "0.1.0")
}

terraform {
  source = "git::${local.common.tf_module_source}/batcave-tf-postgresql.git//.?ref=${local.tf_postgresql_ref}"
}

inputs = {
  vpc_id                              = dependency.vpc.outputs.vpc_id
  create_security_group               = "true"
  subnets                             = dependency.vpc.outputs.subnets.private.ids
  create_db_subnet_group              = true
  iam_database_authentication_enabled = "true"
  apply_immediately                   = "false"
  skip_final_snapshot                 = "false"

  allowed_security_groups             = ["${dependency.eks-cluster.outputs.worker_security_group_id}"]
  worker_security_group_id            = dependency.eks-cluster.outputs.worker_security_group_id
  cluster_security_group_id           = dependency.eks-cluster.outputs.cluster_security_group_id
  cluster_primary_security_group_id   = dependency.eks-cluster.outputs.cluster_primary_security_group_id
}
