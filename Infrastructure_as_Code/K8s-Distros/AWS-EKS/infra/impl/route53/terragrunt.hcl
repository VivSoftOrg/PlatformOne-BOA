locals {
  common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
}

include "parent" {
  path = find_in_parent_folders()
}

include "eks-cluster-dependency" {
  path = "../../base/eks-cluster/dependency.hcl"
}

include "route53" {
  path = "../../base/route53/terragrunt.hcl"
}

inputs = {
  endpoint_subdomain_map = {
    public = {
      endpoint = dependency.eks-cluster.outputs.batcave_alb_proxy_dns
      subdomains = [
        "argocd",
        "easi",
        "eppe-drupal",
        "grafana",
        "home",
        "knight-light"
      ]
    }
    private = {
      endpoint = dependency.eks-cluster.outputs.batcave_lb_dns
      subdomains = [
        "kiali",
        "cost",
        "tracing",
        "alertmanager",
      ]
    }
  }
}
