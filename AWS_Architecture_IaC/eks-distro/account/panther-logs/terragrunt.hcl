locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
  # This is our specific panther account id
  panther_aws_account_id = "115747640837"
}

include "parent" {
  path = find_in_parent_folders()
}


terraform {
    # This will only run if the account is prod
    source = "git::git@github.com:CMSgov/batcave-tf-misc-modules.git//sdl_logs"
}

inputs = {
  panther_aws_account_id = local.panther_aws_account_id
  role_suffix = "${local.common.project}-${local.common.environment}"
  accounts_list = [
    for k, v in local.common.account_map : k
  ]
}
