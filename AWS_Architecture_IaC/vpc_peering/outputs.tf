output "vpc_peer_id-${var.peer_vpc_id}" {
  value = "${aws_vpc_peering_connection.VDMS.id}"
}
