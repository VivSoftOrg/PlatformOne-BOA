variable "name" {}
variable "engine_version" {}
variable "publicly_accessible" {
  default = "false"
}

variable "vpc_id" {}

variable "subnets" {
  type = list(string)
}

variable "allowed_security_groups" {
  type = list(string)
}

variable "master_username" {}
variable "database_name" {}

variable "tags" {
  default = {
    Owner = "Batcave"
  }
}

variable "route53_zone_id" {}
variable "route53_record_name" {}

variable "worker_security_group_id" {}
variable "cluster_security_group_id" {}
variable "cluster_primary_security_group_id" {}

