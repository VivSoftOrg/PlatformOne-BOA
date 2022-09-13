variable "environment" {}

variable "owner" {
  default = "viv_softcloud"
}

variable "project" {
  default = "viv_softPlatform"
}

variable "account_code" {}
variable "client_code" {}

variable "build_url" {
  default = "Unknown"
}

variable "core_aws_profile" {
  default = ""
}

variable "core_account_id" {}
variable "core_account_code" {}

variable "core_platform_admin_users" {
  default = ""
}

variable "extra_jenkins_roles" {
  default = ""
}

variable "output_dir" {
  default = "target"
}

variable "platform_bucket" {
  default = ""
}

variable "platform_admin_users" {
  default = ""
}

variable "platform_admin_roles" {
  default = ""
}

variable "expiration_date" {
  default = ""
}

variable "prefix" {}

variable "tfstate_prefixes" {
  type = "map"
  default = {
  }
}

variable "default_tfstate_prefix" {
  default = ""
}

