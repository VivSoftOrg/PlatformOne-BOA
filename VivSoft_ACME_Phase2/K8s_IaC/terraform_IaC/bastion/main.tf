# lauch bastion instance in public subet so we can access private DNS and also internal load balancer
# This is already created and we provide public key
resource "aws_key_pair" "ssh_public_key" {
  count      = var.enable_bastion ? 1 : 0
  key_name   = "${var.cluster_name}-key"
  public_key = var.ssh_public_key
}

# security group for bastion
resource "aws_security_group" "bastion" {
  count       = var.enable_bastion ? 1 : 0
  name        = "${var.cluster_name}-p1-k8s-bastion-sg"
  description = "${var.cluster_name} p1 k8s bastion SG"
  vpc_id      = var.vpc_id
  tags = {
    Name = "${var.cluster_name}-p1-k8s-bastion-sg"
  }
}

# bastion egress rule
resource "aws_security_group_rule" "bastion-outbound" {
  count             = var.enable_bastion ? 1 : 0
  type              = "egress"
  description       = "outbound bastion traffic"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.bastion[0].id
}

# data "http" "ip" {
#   url = "https://ifconfig.me"
# }

# # bastion ingress rule
# resource "aws_security_group_rule" "bastion-ssh" {
#   count             = var.enable_bastion ? 1 : 0
#   type              = "ingress"
#   description       = "bastion ssh traffic"
#   from_port         = 22
#   to_port           = 22
#   protocol          = "tcp"
#   cidr_blocks       = [""]
#   security_group_id = aws_security_group.bastion[0].id
# }

# bastion ingress rule for cluster_security_group
resource "aws_security_group_rule" "bastion-ssh-cluster_security_group" {
  count                    = var.enable_bastion ? 1 : 0
  type                     = "ingress"
  description              = "bastion ssh traffic"
  from_port                = 22
  to_port                  = 22
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.bastion[0].id
  security_group_id        = var.cluster_security_group_id
}

# bastion ingress rule for cluster_security_group :443
resource "aws_security_group_rule" "bastion-k8s-cluster_security_group" {
  count                    = var.enable_bastion ? 1 : 0
  type                     = "ingress"
  description              = "bastion ssh traffic"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.bastion[0].id
  security_group_id        = var.cluster_security_group_id
}

# bastion ingress rule for worker_security_group
resource "aws_security_group_rule" "bastion-ssh-worker_security_group" {
  count                    = var.enable_bastion ? 1 : 0
  type                     = "ingress"
  description              = "bastion ssh traffic"
  from_port                = 22
  to_port                  = 22
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.bastion[0].id
  security_group_id        = var.worker_security_group_id
}

# bastion ingress rule for cluster_primary_security_group
resource "aws_security_group_rule" "bastion-ssh-cluster_primary_security_group" {
  count                    = var.enable_bastion ? 1 : 0
  type                     = "ingress"
  description              = "bastion ssh traffic"
  from_port                = 22
  to_port                  = 22
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.bastion[0].id
  security_group_id        = var.cluster_primary_security_group_id
}

# bastion ingress rule for cluster_primary_security_group
resource "aws_security_group_rule" "bastion-k8s-cluster_primary_security_group" {
  count                    = var.enable_bastion ? 1 : 0
  type                     = "ingress"
  description              = "bastion k8s traffic"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.bastion[0].id
  security_group_id        = var.cluster_primary_security_group_id
}

# Bastion instance
resource "aws_instance" "bastion" {
  count                       = var.enable_bastion ? 1 : 0
  instance_type               = var.bastion_instance_type
  ami                         = var.bastion_ami_id
  key_name                    = aws_key_pair.ssh_public_key[0].key_name
  subnet_id                   = var.bastion_subnet_id[0]
  vpc_security_group_ids      = [aws_security_group.bastion[0].id, var.worker_security_group_id]
  associate_public_ip_address = true
  user_data              = <<-EOF
		#! /bin/bash
    sudo yum -y install python3
	EOF

  root_block_device {
    volume_size = var.bastion_root_volume_size
    volume_type = "gp2"
  }

  tags = merge(
    {
      "Name" = "${var.cluster_name}-p1-k8s-bastion"
      "Role" = "bastion"
    },
    var.tags,
  )
}

# security group for bastion
resource "aws_security_group" "bastion" {
  count       = var.enable_bastion ? 1 : 0
  name        = "${var.cluster_name}-p1-k8s-bastion"
  description = "${var.cluster_name} p1 k8s bastion"
  vpc_id      = var.vpc_id
}

# bastion egress rule
resource "aws_security_group_rule" "bastion-outbound" {
  count             = var.enable_bastion ? 1 : 0
  type              = "egress"
  description       = "outbound bastion traffic"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.bastion[0].id
}

data "http" "ip" {
  url = "https://ifconfig.me"
}

# bastion ingress rule
resource "aws_security_group_rule" "bastion-ssh" {
  count             = var.enable_bastion ? 1 : 0
  type              = "ingress"
  description       = "bastion ssh traffic"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["${data.http.ip.body}/32"]
  security_group_id = aws_security_group.bastion[0].id
}
