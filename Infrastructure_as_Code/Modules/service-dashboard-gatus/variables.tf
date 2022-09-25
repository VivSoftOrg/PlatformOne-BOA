variable "service_name" {
  default = "gatus"
  type    = string
}
variable "iam_role_permissions_boundary" {
  type    = string
  default = "arn:aws:iam::373346310182:policy/cms-cloud-admin/developer-boundary-policy"
}
variable "iam_role_path" {
  type    = string
  default = ""
}
variable "vpc_id" { type = string }
variable "private_subnet_ids" {
  type = list(any)
}
variable "public_subnet_ids" {
  type = list(any)
}

variable "certificate_arns" {
  default = []
  type    = list(any)
}
variable "hosted_zone_dns" {
  type    = string
  default = ""
}

variable "service_fqdn" {
  type    = string
  default = ""
}

variable "repository_gatus" {
  default = "twinproduction/gatus:latest"
}

variable "repository_awscli" {
  default = "artifactory.cloud.cms.gov/gold-image-docker-local/awscli:latest"
}

variable "acm_cert_base_domain" {
  description = "Base domain of the certificate used for the ALB Proxy"
  default     = ""
  type        = string
}

variable "ingress_prefix_lists" {
  type    = list(any)
  default = []
}

variable "ingress_cidrs" {
  type    = list(any)
  default = []
}

variable "config_bucket_name" {
  type = string
}

variable "cluster_name" {
  default = "batcave"
}
