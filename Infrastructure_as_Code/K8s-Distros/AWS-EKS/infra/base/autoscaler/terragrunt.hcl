locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals

  tf_autoscaler_ref = lookup(local.common, "tf_autoscaler_ref", "1.5.0")
}

terraform {
  source = "git::${local.common.tf_module_source}/batcave-tf-autoscaler.git//.?ref=${local.tf_autoscaler_ref}"
}

inputs = {
  env                  = local.common.environment
  cluster_name         = local.common.cluster_name
  iam_path             = local.common.iam_path
  permissions_boundary = local.common.permissions_boundary

  # Wire vpc outputs
  vpc_eni_subnets = dependency.vpc.outputs.subnets.container.azs_to_id

  # Wire eks-cluster outputs
  self_managed_node_groups           = dependency.eks-cluster.outputs.self_managed_node_groups
  worker_security_group_id           = dependency.eks-cluster.outputs.worker_security_group_id
  cluster_endpoint                   = dependency.eks-cluster.outputs.cluster_endpoint
  cluster_certificate_authority_data = dependency.eks-cluster.outputs.cluster_certificate_authority_data
  cluster_oidc_issuer_url            = dependency.eks-cluster.outputs.cluster_oidc_issuer_url
}
