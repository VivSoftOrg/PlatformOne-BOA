locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals

  # Default to latest release unless overridden in <env>/common.hcl
  tf_route53_ref = lookup(local.common, "tf_route53_ref", "1.0.0")
}

terraform {
  source = "git::${local.common.tf_module_source}/batcave-tf-route53.git//.?ref=${local.tf_route53_ref}"
}

inputs = {
  hosted_zone_dns = local.common.base_domain
}
