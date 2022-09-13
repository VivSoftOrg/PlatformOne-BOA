provider "aws" {
  version = "~> 2.25.0"
}

data "aws_region" "current" {
  current = true
}

resource "aws_vpc_peering_connection_accepter" "peer" {
  vpc_peering_connection_id = "${data.terraform_remote_state.vpc.vpc_peer_id}"
  auto_accept               = true

  tags {
    Side        = "Accepter"
    Name        = "${data.terraform_remote_state.vpc.environment}-${data.terraform_remote_state.vpc.project}-peer"
    Environment = "${data.terraform_remote_state.vpc.environment}"
    Owner       = "${data.terraform_remote_state.vpc.owner}"
    Product     = "${data.terraform_remote_state.vpc.project}"
  }
}
