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
  # Map to associate LB endpoints with DNS subdomains.  The key
  # is not used outside of the terraform resource name
  endpoint_subdomain_map = {
    shared = {
      endpoint = dependency.eks-cluster.outputs.batcave_alb_proxy_dns
      subdomains = [
        "code",
        "defectdojo",
      ]
    }
    private = {
      endpoint = dependency.eks-cluster.outputs.batcave_lb_dns
      subdomains = [
        "argocd",
        "home",
        "cost",
        "kiali",
        "grafana",
        "tracing",
        "alertmanager",
      ]
    }
  }
}
