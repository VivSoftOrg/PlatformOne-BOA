locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

dependency "eks-cluster" {
  config_path = "${get_repo_root()}/infra/${local.common.directory_name}/eks-cluster"
  mock_outputs_merge_strategy_with_state = "shallow"
  mock_outputs = {
    batcave_lb_dns                     = "dummy"
    batcave_alb_proxy_dns              = "dummy"
    worker_security_group_id           = "dummy"
    cluster_security_group_id          = "dummy"
    cluster_endpoint                   = "https://0.0.0.0"
    cluster_certificate_authority_data = "ZHVtbXkK"
    cluster_primary_security_group_id  = "dummy"
    worker_iam_role_name               = "dummy"
    provider_url                       = "dummy"
    cluster_endpoint                   = "dummy"
    private_alb_security_group_id      = "dummy"
    cluster_oidc_issuer_url            = "dummy"
    cosign_iam_role_arn                = "dummy"

    self_managed_node_groups = { general = {
      autoscaling_group_name     = "dummy"
      autoscaling_group_max_size = -1
      autoscaling_group_min_size = -1
      iam_role_name              = "dummy"
    } }
  }
}
