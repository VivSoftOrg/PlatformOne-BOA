locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals

  # Default to latest release unless overridden in <env>/common.hcl
  tf_cluster_ref = lookup(local.common, "tf_cluster_ref", "6.2.0")
}

terraform {
  source = "git::${local.common.tf_module_source}/batcave-tf-cluster.git//.?ref=${local.tf_cluster_ref}"
}

inputs = {
  env                           = local.common.environment
  environment                   = local.common.environment
  region                        = local.common.aws_region
  cluster_name                  = local.common.cluster_name
  iam_role_path                 = local.common.iam_path
  iam_role_permissions_boundary = local.common.permissions_boundary

  cluster_security_group_additional_rules = {}

  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = false

  acm_cert_base_domain = local.common.base_domain

  # Allow inbound request from cloudvpn and cms security tools
  cluster_additional_sg_prefix_lists = [
    dependency.vpc.outputs.cmscloud_shared_services_pl,
    dependency.vpc.outputs.cmscloud_vpn_pl,
    dependency.vpc.outputs.cmscloud_security_tools_pl,
  ]

  # The ALB Proxy is typically in the Public subnet and restricted to CMS IPs
  create_alb_proxy  = true
  alb_proxy_subnets = dependency.vpc.outputs.subnets.public.ids
  alb_proxy_ingress_cidrs = toset(concat(
    # Allow inbound requests from CMS Public IPs
    dependency.vpc.outputs.cms_public_ip_cidrs,
    # Allow inbound requests from natgateway to public security groups
    dependency.vpc.outputs.nat_gateway_public_ip_cidrs,
  ))
  ##CMS Public IPs [soon to be added to cmscloud-public prefix list, but the prefix list is inaccurate at this time]
  #alb_proxy_ingress_prefix_lists = [dependency.vpc.outputs.cmscloud_public_pl]


  ## Wire VPC values into EKS Cluster
  vpc_id              = dependency.vpc.outputs.vpc_id
  private_subnets     = dependency.vpc.outputs.subnets.private.ids
  alb_subnets_by_zone = dependency.vpc.outputs.subnets.private.azs_to_id

  openid_connect_audiences = ["sigstore"]

  # S3 bucket name for load balancer access logs
  logging_bucket = "cms-cloud-${get_aws_account_id()}-${local.common.aws_region}"

  tags = {
    cluster_name = local.common.cluster_name
  }
}
