terraform {
  backend "s3" {}
}

data "terraform_remote_state" "vpc" {
  backend = "s3"

  config {
    bucket                 = "${lower(var.client_code)}-${lower(var.environment)}-${lower(var.project)}"
    key                    = "tfstate/${var.account_code}${lookup(var.tfstate_prefixes, "vdms-vpc", var.default_tfstate_prefix)}/vdms-vpc"
    region                 = "${data.aws_region.current.id}"
    encryption             = true
    skip_region_validation = true
  }
}
