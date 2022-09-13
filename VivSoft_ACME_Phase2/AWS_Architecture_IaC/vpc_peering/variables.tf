variable "require_vpc_peering" {}
variable "remote_bucket" {}
variable "remote_key" {}
variable "peer_owner_id" {}
variable "peer_vpc_id" {}
variable "client_code" {}
variable "environment" {}
variable "project" {}
variable "account_code" {}

variable "prefix" {}

variable "tfstate_prefixes" {
  type = "map"
  default = {
  }
}

variable "default_tfstate_prefix" {
  default = ""
}
