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

variable "elb_logs_bucket" {
  default = ""
}

variable "jenkins_allow_tfdeploy" {
  default = false
}

variable "workload_account_ids" {}

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

variable "enable_ssm" {
  default = false
}
