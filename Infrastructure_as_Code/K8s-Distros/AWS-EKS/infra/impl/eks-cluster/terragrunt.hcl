locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

include "parent" {
  path = find_in_parent_folders()
}

include "vpc-dependency" {
  path = "../../base/vpc/dependency.hcl"
}

include "eks-cluster" {
  path = "../../base/eks-cluster/terragrunt.hcl"
}

dependency "loki_storage" {
  config_path = "../apps/loki/storage"
  mock_outputs = {
    s3_buckets = {}
  }
}

dependency "velero_storage" {
  config_path = "../apps/velero/storage"
  mock_outputs = {
    s3_buckets = {}
  }
}

inputs = {
  ## Environment specific values

  # General nodepool config
  general_node_pool = {
    instance_type = "c5.2xlarge"
    min_size      = "1"
    desired_size  = "1"
    max_size      = "10"
    taints        = { CriticalAddonsOnly = "true:NoSchedule" }
    tags = {
      cluster_name   = local.common.cluster_name
      project-number = "shared"
      project-name   = "shared"
      business-owner = "shared"
      application    = "shared"
      lifecycle      = "impl"
      billing-type   = "shared"
    }
  }

  s3_bucket_access_grants = concat(
    keys(dependency.loki_storage.outputs.s3_buckets),
    keys(dependency.velero_storage.outputs.s3_buckets),
    # fluent bit log destination
    ["cms-cloud-${get_aws_account_id()}-us-east-1"]
  )

  # Custom nodepool config
  custom_node_pools = {
    knightlight = {
      instance_type = "m5.xlarge"
      desired_size  = 1
      max_size      = 1
      min_size      = 1
      tags = {
        project-number = "072ccs"
        business-owner = "iusg"
        project-name   = "batcave"
        application    = "knightlight"
        lifecycle      = "impl"
        billing-type   = "ado"
      }
      taints = { knightlight = "true:NoSchedule" }
    }
    signal = {
      instance_type = "c5.large"
      desired_size  = 1
      max_size      = 1
      min_size      = 1
      tags = {
        project-number = "072ccs"
        business-owner = "iusg"
        project-name   = "batcave"
        application    = "signal"
        lifecycle      = "impl"
        billing-type   = "ado"
      }
      taints = { signal = "true:NoSchedule" }
    }
    oedaeppe = {
      instance_type = "c5.large"
      desired_size  = 1
      max_size      = 1
      min_size      = 1
      tags = {
        project-number = "210ccs"
        business-owner = "oeda"
        project-name   = "eppe"
        application    = "eppe"
        lifecycle      = "impl"
        billing-type   = "ado"
      }
      taints = { oedaeppe = "true:NoSchedule" }
    }
    easi = {
      instance_type = "c5.large"
      desired_size  = 1
      max_size      = 1
      min_size      = 1
      tags = {
        project-number = "072ccs"
        business-owner = "iusg"
        project-name   = "easi"
        application    = "easi"
        lifecycle      = "impl"
        billing-type   = "ado"
      }
      taints = { easi = "true:NoSchedule" }
    }
  }
}
