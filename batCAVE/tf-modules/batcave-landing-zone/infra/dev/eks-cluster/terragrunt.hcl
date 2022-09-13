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

dependency "fluentbit_storage" {
  config_path = "../apps/fluentbit/storage"
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

  create_alb_proxy = false
  ## Uncomment lines below to provision the public ALB, not necessary for dev environments
  #create_alb_proxy        = true
  #alb_proxy_subnets       = dependency.vpc.outputs.subnets.public.ids
  #alb_proxy_ingress_cidrs = dependency.vpc.outputs.cms_public_ip_cidrs

  grant_delete_ebs_volumes_lambda_access = true

  general_node_pool = {
    instance_type = "c5a.4xlarge"
    min_size      = "1"
    desired_size  = "1"
    max_size      = "5"

    ## Only when you need cluster with taints/tolerations
    #taints = {
    #  CriticalAddonsOnly = "true:NoSchedule"
    #}
  }

  # Custom nodepool config
  custom_node_pools = {
    #gen-small = {
    #  instance_type = "c6a.xlarge"
    #  desired_size  = 0
    #  max_size      = 4
    #  min_size      = 0
    #  labels = {
    #    general = "true"
    #  }
    #}
    runners = {
      instance_type = "c6a.xlarge"
      desired_size  = 0
      max_size      = 0
      min_size      = 0
      tags = {
        project-number = "072ccs"
        business-owner = "IUSG"
        project-name   = "batcave"
        application    = "gitlab"
        lifecycle      = "dev"
        billing-type   = "ado"
      }
      taints = { runners = "true:NoSchedule" }
      labels = { nongeneral = "true" }
    }
  }

  s3_bucket_access_grants = concat(
    keys(dependency.gitlab_storage.outputs.s3_buckets),
    keys(dependency.loki_storage.outputs.s3_buckets),
    keys(dependency.fluentbit_storage.outputs.s3_buckets),
    keys(dependency.velero_storage.outputs.s3_buckets)
  )
}
