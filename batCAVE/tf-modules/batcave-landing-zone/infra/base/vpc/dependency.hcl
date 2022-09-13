locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

dependency "vpc" {
  config_path = "${get_repo_root()}/infra/${local.common.directory_name}/vpc"
  mock_outputs = {
    vpc_id                      = "dummy"
    cmscloud_vpn_sg             = "dummy"
    shared_services_sg          = "dummy"
    cmscloud_shared_services_pl = "dummy"
    cmscloud_vpn_pl             = "dummy"
    cmscloud_security_tools_pl  = "dummy"
    nat_gateway_public_ip_cidrs = ["dummy"]
    cms_public_ip_cidrs         = ["0.0.0.0/32"]

    subnets = { for subnet in ["private", "shared", "transport", "public", "container"] :
      subnet => {
        ids         = ["dummy"],
        azs_to_id   = { "dummy" = "dummy" },
        ids_to_cidr = { "dummy" = "dummy" },
      }
    }
  }
}
