resource "aws_network_acl" "guardrail" {
  count  = "${var.external_nacl ? 0 : 1}"
  vpc_id = "${aws_vpc.vpc.id}"

  subnet_ids = [
    "${aws_subnet.priv.*.id}",
    "${aws_subnet.pub.*.id}",
    "${aws_subnet.mgmt.*.id}",
    "${aws_subnet.storage.*.id}",
    "${aws_subnet.packer.*.id}",
  ]

  egress {
    protocol   = "tcp"
    rule_no    = 100
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 20
    to_port    = 21
  }

  egress {
    protocol   = "tcp"
    rule_no    = 110
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 23
    to_port    = 23
  }

  egress {
    protocol   = "tcp"
    rule_no    = 120
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 110
    to_port    = 110
  }

  egress {
    protocol   = "tcp"
    rule_no    = 130
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 143
    to_port    = 143
  }

  egress {
    protocol   = "udp"
    rule_no    = 140
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 161
    to_port    = 162
  }

  egress {
    protocol   = "-1"
    rule_no    = 32766
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  ingress {
    protocol   = "tcp"
    rule_no    = 100
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 20
    to_port    = 21
  }

  ingress {
    protocol   = "tcp"
    rule_no    = 110
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 23
    to_port    = 23
  }

  ingress {
    protocol   = "tcp"
    rule_no    = 120
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 110
    to_port    = 110
  }

  ingress {
    protocol   = "tcp"
    rule_no    = 130
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 143
    to_port    = 143
  }

  ingress {
    protocol   = "udp"
    rule_no    = 140
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 161
    to_port    = 162
  }

  ingress {
    protocol   = "-1"
    rule_no    = 32766
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-guardrail"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Project        = "${var.project}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}
