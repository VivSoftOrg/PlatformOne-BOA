variable "cluster_name" {}
variable "provider_url" {
    default = ""
}

### Karpenter IAM variables

variable "worker_iam_role_name" {
    default = ""
}

variable "iam_path" {
  default = ""
}

variable "permissions_boundary" {
  default = ""
}


### Helm variables

variable "helm_namespace" {
    default = "karpenter"
}
variable "helm_create_namespace" {
    type = bool
    default = true
}
variable "helm_name" {
    default = "karpenter"
}
variable "cluster_endpoint" {
    default = ""
}