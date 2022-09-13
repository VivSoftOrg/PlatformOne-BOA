output "peering-id" {
  value = "${data.terraform_remote_state.vpc.vpc_peer_id}"
}
