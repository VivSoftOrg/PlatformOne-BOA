provider "aws" {
  version = "~> 2.25.0"
}

data "aws_region" "current" {}

# This peering need to be accepted from the other side also
resource "aws_vpc_peering_connection" "VDMS" {
  count         = "${var.require_vpc_peering ? 1 : 0}"
  peer_owner_id = "${var.peer_owner_id}"
  peer_vpc_id   = "${var.peer_vpc_id}"
  vpc_id        = "${data.terraform_remote_state.vpc.vpc_id}"
}
