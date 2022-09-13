# Access to specific ports for specific SSH CIDR blocks.
resource "aws_security_group" "ssh-remote-access" {
  count       = "${length(var.ssh_remote_cidr_block) > 0 ? 1 : 0}"
  name        = "${var.prefix}-ssh-remote-access"
  description = "Remote access for SSH"
  vpc_id      = "${aws_vpc.vpc.id}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-ssh-remote-access"
    Environment    = "${var.environment}"
    Project        = "${var.project}"
    Product        = "VDMS"
    Owner          = "${var.owner}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_security_group_rule" "ssh-remote-access" {
  count             = "${length(var.ssh_remote_cidr_block) > 0 ? 1 : 0}"
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  security_group_id = "${aws_security_group.ssh-remote-access.0.id}"
  cidr_blocks       = ["${split(",",var.ssh_remote_cidr_block)}","${var.vpc_cidr_block}"]
  description       = "Remote access for SSH"
}

# Access to specific ports for specific HTTPS CIDR blocks.
resource "aws_security_group" "https-remote-access" {
  count       = "${length(var.https_remote_cidr_block) > 0 ? 1 : 0}"
  name        = "${var.prefix}-https-remote-access"
  description = "Remote access for HTTPS"
  vpc_id      = "${aws_vpc.vpc.id}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-https-remote-access"
    Environment    = "${var.environment}"
    Project        = "${var.project}"
    Product        = "VDMS"
    Owner          = "${var.owner}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_security_group_rule" "https-remote-access" {
  count             = "${length(var.https_remote_cidr_block) > 0 ? 1 : 0}"
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  security_group_id = "${aws_security_group.https-remote-access.0.id}"
  cidr_blocks       = ["${split(",",var.https_remote_cidr_block)}","${var.vpc_cidr_block}"]
  description       = "Remote access for HTTPS"
}

resource "aws_security_group_rule" "k8s-remote-access" {
  count             = "${length(var.ssh_remote_cidr_block) > 0 ? 1 : 0}"
  type              = "ingress"
  from_port         = 6443
  to_port           = 6443
  protocol          = "tcp"
  security_group_id = "${aws_security_group.https-remote-access.0.id}"
  cidr_blocks       = ["${split(",",var.ssh_remote_cidr_block)}","${var.vpc_cidr_block}"]
  description       = "Remote access for K8s Api"
}

# Access to specific ports for specific RDP CIDR blocks.
resource "aws_security_group" "rdp-remote-access" {
  count       = "${length(var.rdp_remote_cidr_block) > 0 ? 1 : 0}"
  name        = "${var.prefix}-rdp-remote-access"
  description = "Remote access for RDP"
  vpc_id      = "${aws_vpc.vpc.id}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-rdp-remote-access"
    Environment    = "${var.environment}"
    Project        = "${var.project}"
    Product        = "VDMS"
    Owner          = "${var.owner}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_security_group_rule" "rdp-remote-access" {
  count             = "${length(var.rdp_remote_cidr_block) > 0 ? 1 : 0}"
  type              = "ingress"
  from_port         = 3389
  to_port           = 3389
  protocol          = "tcp"
  security_group_id = "${aws_security_group.rdp-remote-access.0.id}"
  cidr_blocks       = ["${split(",",var.rdp_remote_cidr_block)}"]
  description       = "Remote access for RDP"
}

# Access to specific ports for specific WinRM HTTPS CIDR blocks.
resource "aws_security_group" "winrm-remote-access" {
  count       = "${length(var.winrm_remote_cidr_block) > 0 ? 1 : 0}"
  name        = "${var.prefix}-winrm-remote-access"
  description = "Remote access for WinRM HTTPS"
  vpc_id      = "${aws_vpc.vpc.id}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-winrm-remote-access"
    Environment    = "${var.environment}"
    Project        = "${var.project}"
    Product        = "VDMS"
    Owner          = "${var.owner}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_security_group_rule" "winrm-remote-access" {
  count             = "${length(var.winrm_remote_cidr_block) > 0 ? 1 : 0}"
  type              = "ingress"
  from_port         = 5986
  to_port           = 5986
  protocol          = "tcp"
  security_group_id = "${aws_security_group.winrm-remote-access.0.id}"
  cidr_blocks       = ["${split(",",var.winrm_remote_cidr_block)}"]
  description       = "Remote access for WinRM HTTPS"
}

# Access to specific ports for any and all known VPN CIDR blocks
resource "aws_security_group" "vpn-remote-access" {
  count       = "${length(var.vpn_remote_cidr_block) > 0 ? 1 : 0}"
  name        = "${var.prefix}-vpn-remote-access"
  description = "VPN Remote Access"
  vpc_id      = "${aws_vpc.vpc.id}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-vpn-remote-access"
    Environment    = "${var.environment}"
    Project        = "${var.project}"
    Product        = "VDMS"
    Owner          = "${var.owner}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_security_group_rule" "vpn-remote-access-ssh" {
  count             = "${length(var.vpn_remote_cidr_block) > 0 ? 1 : 0}"
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  security_group_id = "${aws_security_group.vpn-remote-access.0.id}"
  cidr_blocks       = ["${split(",",var.vpn_remote_cidr_block)}"]
  description       = "VPN access for SSH"
}

resource "aws_security_group_rule" "vpn-remote-access-https" {
  count             = "${length(var.vpn_remote_cidr_block) > 0 ? 1 : 0}"
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  security_group_id = "${aws_security_group.vpn-remote-access.0.id}"
  cidr_blocks       = ["${split(",",var.vpn_remote_cidr_block)}"]
  description       = "VPN access for HTTPS"
}

resource "aws_security_group_rule" "vpn-remote-access-rdp" {
  count             = "${length(var.vpn_remote_cidr_block) > 0 ? 1 : 0}"
  type              = "ingress"
  from_port         = 3389
  to_port           = 3389
  protocol          = "tcp"
  security_group_id = "${aws_security_group.vpn-remote-access.0.id}"
  cidr_blocks       = ["${split(",",var.vpn_remote_cidr_block)}"]
  description       = "VPN access for RDP"
}

resource "aws_security_group_rule" "vpn-remote-access-winrms" {
  count             = "${length(var.vpn_remote_cidr_block) > 0 ? 1 : 0}"
  type              = "ingress"
  from_port         = 5986
  to_port           = 5986
  protocol          = "tcp"
  security_group_id = "${aws_security_group.vpn-remote-access.0.id}"
  cidr_blocks       = ["${split(",",var.vpn_remote_cidr_block)}"]
  description       = "VPN access for WinRM HTTPS"
}
