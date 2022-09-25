output "vpc_id" {
  value = "${aws_vpc.vpc.id}"
}

output "vpc_cidr" {
  value = "${aws_vpc.vpc.cidr_block}"
}

output "pub_route_table_id" {
  value = "${aws_route_table.pub.id}"
}

output "priv_route_table_ids" {
  value = "${join(",", aws_route_table.priv.*.id)}"
}

output "pub_subnets" {
  value = "${join(",", aws_subnet.pub.*.id)}"
}

output "priv_subnets" {
  value = "${join(",", aws_subnet.priv.*.id)}"
}

output "mgmt_subnets" {
  value = "${join(",", aws_subnet.mgmt.*.id)}"
}

output "storage_subnets" {
  value = "${join(",", aws_subnet.storage.*.id)}"
}

output "packer_subnets" {
  value = "${join(",", aws_subnet.packer.*.id)}"
}

output "az_count" {
  value = "${var.az_count}"
}

output "all_egress_sg" {
  value = "${join(",",aws_security_group.all-egress.*.id)}"
}

output "vpc_egress_sg" {
  value = "${join(",",aws_security_group.vpc-egress.*.id)}"
}

output "vpn_remote_cidr_block" {
  value = "${var.vpn_remote_cidr_block}"
}

output "vpn_remote_access_sg" {
  value = "${join(",",aws_security_group.vpn-remote-access.*.id)}"
}

output "ssh_remote_cidr_block" {
  value = "${var.ssh_remote_cidr_block}"
}

output "ssh_remote_access_sg" {
  value = "${join(",",aws_security_group.ssh-remote-access.*.id)}"
}

output "https_remote_cidr_block" {
  value = "${var.https_remote_cidr_block}"
}

output "https_remote_access_sg" {
  value = "${join(",",aws_security_group.https-remote-access.*.id)}"
}

output "rdp_remote_cidr_block" {
  value = "${var.rdp_remote_cidr_block}"
}

output "rdp_remote_access_sg" {
  value = "${join(",",aws_security_group.rdp-remote-access.*.id)}"
}

output "winrm_remote_cidr_block" {
  value = "${var.winrm_remote_cidr_block}"
}

output "winrm_remote_access_sg" {
  value = "${join(",",aws_security_group.winrm-remote-access.*.id)}"
}

output "nat_eips" {
  value = "${aws_eip.nat.*.id}"
}

output "nat_eip_instances" {
  value = "${data.aws_eip.nat.*.instance_id}"
}

output "nat_ext_eips" {
  value = "${aws_eip.nat.*.public_ip}"
}

output "nat_lc_names" {
  value = "${join(",",aws_launch_configuration.nat.*.name)}"
}

output "nat_asg_names" {
  value = "${join(",",aws_autoscaling_group.nat.*.name)}"
}

output "bastion_lc_names" {
  value = "${join(",",aws_launch_configuration.bastion.*.name)}"
}

output "bastion_asg_names" {
  value = "${join(",",aws_autoscaling_group.bastion.*.name)}"
}

output "bastion_instance_sg" {
  value = "${join(",",aws_security_group.bastion.*.id)}"
}

output "project" {
  value = "${var.project}"
}

output "environment" {
  value = "${var.environment}"
}

output "owner" {
  value = "${var.owner}"
}

output "creator" {
  value = "${var.creater}"
}

output "expiration_date" {
  value = "${var.expiration_date}"
}

output "nat_enis" {
  value = "${aws_network_interface.nat.*.id}"
}

output "dhcp_dns_servers" {
  value = "${var.dhcp_dns_servers}"
}

output "dhcp_ntp_servers" {
  value = "${var.dhcp_ntp_servers}"
}

output "availability_zones" {
  value = "${data.aws_availability_zones.zones.names}"
}

output "nat_gateways" {
  value = "${join(",",aws_nat_gateway.nat.*.id)}"
}

output "bastion_role_tag" {
  value = "${var.prefix}-bastion"
}

output "nat_role_arn" {
  value = "${join(",",aws_iam_role.nat.*.arn)}"
}

output "nat_policy_name" {
  value = "${join(",", aws_iam_role_policy.nat.*.name)}"
}

output "bastion_role_arn" {
  value = "${join(",",aws_iam_role.bastion.*.arn)}"
}

output "ssm_core_policy_arn" {
  value = "${data.terraform_remote_state.iam.ssm_core_policy_arn}"
}