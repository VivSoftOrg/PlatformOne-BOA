locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

include "parent" {
  path = find_in_parent_folders()
}

include "terragrunt-vars" {
  path   = "../../base/terragrunt-vars/terragrunt.hcl"
  expose = true
}

include "eks-cluster" {
  path = "../../base/eks-cluster/dependency.hcl"
}

dependency "loki_storage" {
  config_path = "../apps/loki/storage"
  mock_outputs = {
    s3_buckets = { }
  }
}

inputs = {
  # Wire eks-cluster connection information
  # Must be here because terragrunt-vars base is exposed
  cluster_endpoint                   = dependency.eks-cluster.outputs.cluster_endpoint
  cluster_certificate_authority_data = dependency.eks-cluster.outputs.cluster_certificate_authority_data

  ## Environment-specific configuration
  ## Note the values MUST be simple strings and not complex vars for use
  ## in the flux substitution process on the k8s side
  configmap_data = merge(include.terragrunt-vars.locals.configmap_data,
    {
      batcave_bucket_loki = one(keys(dependency.loki_storage.outputs.s3_buckets))
      batcave_bucket_gitlab = local.common.gitlab_storage_bucket
      batcave_bucket_gitlab_runner_cache = local.common.gitlab_runner_cache_bucket
      cosign_iam_role_arn = dependency.eks-cluster.outputs.cosign_iam_role_arn
    }
  )
}

