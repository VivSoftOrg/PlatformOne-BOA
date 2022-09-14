################################################################################
# Bastion
################################################################################
output "subnet_id" {
  value = var.bastion_subnet_id
}
output "bastion_ssh_keyname" {
  value = aws_key_pair.ssh_public_key[*].key_name
}
output "bastion_ipaddress" {
  value = aws_instance.bastion[*].public_ip
}

################################################################################
# AWS Security Group
################################################################################

output "bastion_security_group_id" {
  description = "ID of the security group"
  value = aws_security_group.bastion[0].id
}
output "bastion_security_group_arn" {
  description = "ARN of the security group"
  value = aws_security_group.bastion[0].arn
}
output "bastion_security_group_owner_id" {
  description = "Owner ID"
  value = aws_security_group.bastion[0].owner_id
}
output "bastion_security_group_tags" {
  description = "A map of tags assigned to the resource"
  value = aws_security_group.bastion[0].tags_all
}

################################################################################
# AWS Security Group Rules
################################################################################
output "bastion_sg_outbound_id" {
  description = "Id of the security group rule"
  value = aws_security_group_rule.bastion-outbound[0].id
}

output "bastion_sg_ssh_cluster_id" {
  description = "Id of the security group rule"
  value = aws_security_group_rule.bastion-ssh-cluster_security_group[0].id
}

output "bastion_sg_ssh_worker_id" {
  description = "Id of the security group rule"
  value = aws_security_group_rule.bastion-ssh-worker_security_group[0].id
}

output "bastion_sg_ssh_cluster_primary_id" {
  description = "Id of the security group rule"
  value = aws_security_group_rule.bastion-ssh-cluster_primary_security_group[0].id
}

################################################################################
# AWS Key Pair
################################################################################

output "bastion_ssh_id" {
  description = "The key pair name"
  value = aws_key_pair.ssh_public_key[*].id
}

output "bastion_ssh_arn" {
  description = "The key pair ARN"
  value = aws_key_pair.ssh_public_key[*].arn
}

output "bastion_ssh_key_name" {
  description = "The key pair name"
  value = aws_key_pair.ssh_public_key[*].key_name
}

output "bastion_ssh_key_pair_id" {
  description = "The key pair ID"
  value = aws_key_pair.ssh_public_key[*].key_pair_id
}

output "bastion_ssh_fingerprint" {
  description = "The MD5 public key fingerprint as specified in section 4 of RFC 4716"
  value = aws_key_pair.ssh_public_key[*].fingerprint
}

output "bastion_ssh_tags" {
  description = "A map of tags assigned to the resource"
  value = aws_key_pair.ssh_public_key[*].tags_all
}

