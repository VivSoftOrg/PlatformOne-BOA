variable "cluster_name" {}
variable "cluster_endpoint" {}
variable "cluster_certificate_authority_data" {}

### Karpenter IAM variables
variable "worker_iam_role_name" {
  default = ""
}

variable "iam_path" {
  default = "/delegatedadmin/developer/"
}

variable "permissions_boundary" {
  default = "arn:aws:iam::373346310182:policy/cms-cloud-admin/developer-boundary-policy"
}


### Helm variables
variable "helm_namespace" {
  default = "kube-system"
}

variable "helm_name" {
  default = "auto-scaler"
}

variable "self_managed_node_groups" {
  type = map(any)
}

# ENIConfig Variables
variable "vpc_eni_subnets" {
  type = map(any)
}

variable "worker_security_group_id" {
  type = string
}

variable "rotate_nodes_after_eniconfig_creation" {
  type    = bool
  default = true
}

variable "cluster_oidc_issuer_url" {}

variable "autoscaler_expander_method" {
  default     = "least-waste"
  type        = string
  description = "Method by which CA will select a new instance to launch. Current options: random, most-pods, least-waste. See: https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#what-are-expanders"
}

variable "extraArgs" {
  default     = {}
  type        = map(any)
  description = "List of extraArgs values to pass to the autoscaler chart.  See: https://github.com/kubernetes/autoscaler/blob/master/charts/cluster-autoscaler/values.yaml#L165"
}

# Pod limit values
variable "cpu_limits" {
  default = "50m"
}

variable "cpu_requests" {
  default = "10m"
}

variable "memory_limits" {
  default = "512Mi"
}

variable "memory_requests" {
  default = "50Mi"
}
