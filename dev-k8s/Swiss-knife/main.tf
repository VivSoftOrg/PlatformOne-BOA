terraform {
  required_version = ">= 0.13"
}

provider "aws" {
  region = var.aws_region
}

# our default security group to access the instances
resource "aws_security_group" "default" {
  vpc_id = var.aws_vpc_id

  tags = {
    Name  = var.aws_tag_name,
    Owner = basename(data.aws_caller_identity.current.arn),
  }
}

# allow ingress from client machine
resource "aws_security_group_rule" "ingress_client" {
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = aws_security_group.default.id
  cidr_blocks       = [format("%s/%s", data.external.client_info.result["ip"], 32)]
  # optionally include this rule based on ingress all variable
  count = var.aws_ingress_all ? 0 : 1
}

# allow ingress from anywhere
resource "aws_security_group_rule" "ingress_all" {
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = aws_security_group.default.id
  cidr_blocks       = [var.my_ip]
  # optionally include this rule based on ingress all variable
  count = var.aws_ingress_all ? 1 : 0
}

# allow egress to client machine
resource "aws_security_group_rule" "egress_client" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = aws_security_group.default.id
  cidr_blocks       = [format("%s/%s", data.external.client_info.result["ip"], 32)]
  # optionally include this rule based on airgap variable
  count = var.aws_airgap ? 1 : 0
}

# allow egress to all
resource "aws_security_group_rule" "egress_all" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = aws_security_group.default.id
  cidr_blocks       = [var.my_ip]
  # optionally include this rule based on airgap variable
  count = var.aws_airgap ? 0 : 1
}

# aws key pair to create
resource "aws_key_pair" "auth" {
  public_key = file(var.public_key_path)

  tags = {
    Name  = var.aws_tag_name,
    Owner = basename(data.aws_caller_identity.current.arn),
  }
}

# aws spot instance to create and provision
resource "aws_spot_instance_request" "k3d" {
  ami                    = data.aws_ami.default.id
  instance_type          = var.aws_instance_type
  key_name               = aws_key_pair.auth.id
  vpc_security_group_ids = [aws_security_group.default.id]
  subnet_id              = var.aws_subnet_id
  wait_for_fulfillment   = true

  tags = {
    Name  = var.aws_tag_name,
    Owner = basename(data.aws_caller_identity.current.arn),
  }

  # connection information
  connection {
    type        = "ssh"
    user        = var.ami_instance_user
    private_key = file(var.private_key_path)
    host        = self.public_ip
  }

  # root block device settings
  root_block_device {
    volume_size = var.aws_root_block_size
  }

  # run ansible
  # provide some useful variable templating, other things as well
  # we need to also provide {{ instance_ip }} since we can't easily grab this in ansible itself
  provisioner "local-exec" {
    command = "ANSIBLE_CONFIG=ansible.cfg ANSIBLE_HOST_KEY_CHECKING=${var.ansible_host_key_checking} ANSIBLE_SSH_RETRIES=${var.ansible_ssh_retries} ${var.ansible_pre_args} ansible-playbook ${var.ansible_post_args} -i \"${self.public_ip},\" -u \"${var.ami_instance_user}\" --private-key \"${var.private_key_path}\" --extra-vars \"instance_ip=${self.public_ip}\" ${var.ansible_playbook_path}"
  }
}