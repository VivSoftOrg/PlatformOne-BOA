locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals

  # Default to latest release unless overridden in <env>/common.hcl
  tf_gatus_ref = lookup(local.common, "tf_gatus_ref", "1.0.0")
}

terraform {
  source = "git::${local.common.tf_module_source}/batcave-tf-gatus.git//.?ref=${local.tf_gatus_ref}"
  #source = find_in_parent_folders("modules/batcave-tf-gatus")
}

inputs = {
  iam_role_path                 = local.common.iam_path
  iam_role_permissions_boundary = local.common.permissions_boundary
  acm_cert_base_domain          = local.common.base_domain
  hosted_zone_dns               = local.common.base_domain

  vpc_id             = dependency.vpc.outputs.vpc_id
  private_subnet_ids = dependency.vpc.outputs.subnets.private.ids
  public_subnet_ids  = dependency.vpc.outputs.subnets.public.ids
  ingress_cidrs      = dependency.vpc.outputs.cms_public_ip_cidrs

  config_bucket_name = one(keys(dependency.gatus-storage.outputs.s3_buckets))

  service_fqdn       = "gatus.${local.common.base_domain}"
  service_name       = "${local.common.cluster_name}-gatus"

  alb_log_bucket_name = "cms-cloud-${local.common.aws_id}-${local.common.aws_region}"
}
