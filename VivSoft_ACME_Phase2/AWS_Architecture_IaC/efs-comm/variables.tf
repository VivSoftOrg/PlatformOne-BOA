variable "create_efs" {
  type        = bool
  default     = false
  description = "toggle to create efs or not"
}

variable "iam_role" {
  type        = string
  description = "Create IAM policy and attach to workers"
}

variable "cluster_name" {
  type        = string
  description = "Name of cluster"
}

variable "name" {
  type        = string
  description = "Name to prefix to created resources"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID to deploy to"
}

variable "subnet_ids" {
  type = list(string)
}

variable "access_sg_ids" {
  type        = list(string)
  description = "ID of security groups to give 5432 access to"
}

variable "common_tags" {
  type    = map(string)
  default = {}
}