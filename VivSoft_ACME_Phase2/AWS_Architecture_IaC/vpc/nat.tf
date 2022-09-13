resource "aws_eip" "nat" {
  count      = "${var.nat_type=="instance" || var.nat_type=="gateway" ? var.az_count : 0}"
  vpc        = true
  depends_on = ["aws_internet_gateway.igw"]

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-nat-${element(data.aws_availability_zones.zones.names, count.index)}"
    Environment    = "${var.environment}"
    Project        = "${var.project}"
    Product        = "VDMS"
    Owner          = "${var.owner}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_eip_association" "nat" {
  count                = "${var.nat_type=="instance" ? var.az_count : 0}"
  allocation_id        = "${element(aws_eip.nat.*.id, count.index)}"
  network_interface_id = "${element(aws_network_interface.nat.*.id, count.index)}"
  depends_on           = ["aws_autoscaling_group.nat"]

  provisioner "local-exec" {
    command = "sleep 10"
  }
}

resource "aws_nat_gateway" "nat" {
  count         = "${var.nat_type=="gateway" ? var.az_count : 0}"
  allocation_id = "${element(aws_eip.nat.*.id, count.index)}"
  subnet_id     = "${element(aws_subnet.pub.*.id, count.index)}"
  depends_on    = ["aws_internet_gateway.igw"]

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-nat"
    Environment    = "${var.environment}"
    Project        = "${var.project}"
    Product        = "VDMS"
    Owner          = "${var.owner}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

data "template_file" "nat_userdata" {
  count    = "${var.nat_type=="instance" ? var.az_count : 0}"
  template = "${file("${path.module}/templates/nat-redhat.sh.tpl")}"

  vars {
    my_eni_id         = "${element(aws_network_interface.nat.*.id, count.index)}"
    install_ssm_agent = "${var.install_ssm_agent}"
  }
}

resource "aws_security_group" "nat" {
  count       = "${var.nat_type=="instance" ? 1 : 0}"
  name        = "${var.prefix}-nat"
  description = "NAT instance security group"
  vpc_id      = "${aws_vpc.vpc.id}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-nat"
    Environment    = "${var.environment}"
    Project        = "${var.project}"
    Product        = "VDMS"
    Owner          = "${var.owner}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_security_group_rule" "nat-ingress-rule-all" {
  count             = "${var.nat_type=="instance" ? 1 : 0}"
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = "${aws_security_group.nat.id}"
  cidr_blocks       = ["${var.vpc_cidr_block}"]
  description       = "Allow icmp ingress from VPC only"
}

resource "aws_security_group_rule" "nat-ingress-rule-icmp" {
  count             = "${var.nat_type=="instance" ? 1 : 0}"
  type              = "ingress"
  from_port         = -1
  to_port           = -1
  protocol          = "icmp"
  security_group_id = "${aws_security_group.nat.id}"
  cidr_blocks       = ["${var.vpc_cidr_block}"]
  description       = "Allow all ingress from VPC only"
}

resource "aws_security_group_rule" "nat-egress-rule" {
  count             = "${var.nat_type=="instance" ? 1 : 0}"
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = "${aws_security_group.nat.id}"
  cidr_blocks       = ["0.0.0.0/0"]
  description       = "Allow egress to all"
}

resource "aws_network_interface" "nat" {
  count             = "${var.nat_type=="instance" ? var.az_count : 0}"
  subnet_id         = "${element(aws_subnet.pub.*.id, count.index)}"
  source_dest_check = false
  security_groups   = ["${aws_security_group.nat.id}", "${aws_security_group.ssh-remote-access.*.id}"]

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-nat"
    Environment    = "${var.environment}"
    Project        = "${var.project}"
    Product        = "VDMS"
    Owner          = "${var.owner}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_iam_role_policy" "nat" {
  count = "${var.nat_type=="instance" ? 1 : 0}"
  name  = "${var.prefix}-nat"
  role  = "${aws_iam_role.nat.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:AttachNetworkInterface",
        "ec2:ModifyInstanceAttribute"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role" "nat" {
  count = "${var.nat_type=="instance" ? 1 : 0}"
  name  = "${var.prefix}-nat"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
    "Effect": "Allow",
    "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "nat" {
  count      = "${var.nat_type=="instance" && var.enable_ssm ? 1 : 0}"
  role       = "${aws_iam_role.nat.name}"
  policy_arn = "${data.terraform_remote_state.iam.ssm_core_policy_arn}"
}

resource "aws_iam_instance_profile" "nat" {
  count = "${var.nat_type=="instance" ? 1 : 0}"
  name  = "${var.prefix}-nat"
  role  = "${aws_iam_role.nat.name}"
}

resource "aws_launch_configuration" "nat" {
  count = "${var.nat_type=="instance" ? var.az_count : 0}"

  name_prefix          = "${var.prefix}-nat-${element(data.aws_availability_zones.zones.names, count.index)}"
  image_id             = "${var.baseos_rhel7_ami_id}"
  instance_type        = "${var.nat_instance_type}"
  security_groups      = ["${aws_security_group.nat.id}"]
  key_name             = "${local.platform_keypair}"
  depends_on           = ["aws_iam_instance_profile.nat"]
  iam_instance_profile = "${aws_iam_instance_profile.nat.name}"
  user_data            = "${element(data.template_file.nat_userdata.*.rendered, count.index)}"

  associate_public_ip_address = true

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "nat" {
  count                = "${var.nat_type=="instance" ? var.az_count : 0}"
  vpc_zone_identifier  = ["${element(aws_subnet.pub.*.id, count.index)}"]
  name                 = "${var.prefix}-nat-${element(data.aws_availability_zones.zones.names, count.index)}"
  min_size             = 1
  max_size             = 1
  desired_capacity     = 1
  force_delete         = true
  launch_configuration = "${element(aws_launch_configuration.nat.*.id, count.index)}"

  tag {
    key                 = "Name"
    value               = "${var.prefix}-nat-${element(data.aws_availability_zones.zones.names, count.index)}"
    propagate_at_launch = true
  }

  tag {
    key                 = "Environment"
    value               = "${var.environment}"
    propagate_at_launch = true
  }

  tag {
    key                 = "Owner"
    value               = "${var.owner}"
    propagate_at_launch = true
  }

  tag {
    key                 = "Project"
    value               = "${var.project}"
    propagate_at_launch = true
  }

  tag {
    key                 = "BuildUrl"
    value               = "${var.build_url}"
    propagate_at_launch = true
  }

  tag {
    key                 = "Product"
    value               = "VDMS"
    propagate_at_launch = true
  }

  tag {
    key                 = "ExpirationDate"
    value               = "${var.expiration_date}"
    propagate_at_launch = true
  }

  tag {
    key                 = "Schedule"
    value               = "${var.instance_schedule}"
    propagate_at_launch = true
  }
}

resource "aws_route" "nat_instance_route" {
  count                  = "${var.nat_type=="instance" ? var.az_count : 0}"
  route_table_id         = "${element(aws_route_table.priv.*.id, count.index)}"
  destination_cidr_block = "0.0.0.0/0"
  network_interface_id   = "${element(aws_network_interface.nat.*.id, count.index)}"
}

resource "aws_route" "nat_gateway_route" {
  count                  = "${var.nat_type=="gateway" ? var.az_count : 0}"
  route_table_id         = "${element(aws_route_table.priv.*.id, count.index)}"
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = "${element(aws_nat_gateway.nat.*.id, count.index)}"
}

data "aws_eip" "nat" {
  count      = "${var.nat_type=="instance" ? var.az_count : 0}"
  id         = "${element(aws_eip.nat.*.id, count.index)}"
  depends_on = ["aws_eip_association.nat"]
}
