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

dependency "gitlab_storage" {
  config_path = "../apps/gitlab/storage"
  mock_outputs = {
    s3_buckets = {}
  }
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

  # Create a second ALB in the shared subnet to open access to services across CMSCloud (AWS)
  alb_proxy_is_internal = true
  alb_proxy_subnets     = dependency.vpc.outputs.subnets.shared.ids
  alb_proxy_ingress_prefix_lists = [
    dependency.vpc.outputs.cmscloud_shared_services_pl,
    dependency.vpc.outputs.cmscloud_vpn_pl,
    dependency.vpc.outputs.cmscloud_security_tools_pl,
  ]
  alb_proxy_ingress_cidrs = [
    "10.0.0.0/8",
    "100.0.0.0/8",
  ]

  # EKS Cluster General Node information
  general_node_pool = {
    instance_type = "c5.2xlarge"
    min_size      = "4"
    desired_size  = "5"
    max_size      = "10"
  }

  custom_node_pools = {
    gen-small = {
      instance_type = "c6a.xlarge"
      desired_size  = 0
      max_size      = 4
      min_size      = 0
      labels        = { general = "true" }
    }
    runners = {
      instance_type = "c5.xlarge"
      # Size for GitLab runners nodepool group
      desired_size = 1
      max_size     = 10
      min_size     = 1
      tags = {
        project-number = "072ccs"
        business-owner = "iusg"
        project-name   = "batcave"
        application    = "gitlab"
        lifecycle      = "prod"
        billing-type   = "ado"
      }
      taints = { runners = "true:NoSchedule" }
    }
  }

  s3_bucket_access_grants = concat(
    keys(dependency.gitlab_storage.outputs.s3_buckets),
    keys(dependency.loki_storage.outputs.s3_buckets),
    keys(dependency.velero_storage.outputs.s3_buckets),
    # fluent bit log destination
    ["cms-cloud-${get_aws_account_id()}-us-east-1"]
  )

  create_cosign_iam_role = true
}
