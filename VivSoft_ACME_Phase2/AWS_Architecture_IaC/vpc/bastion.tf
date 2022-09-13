resource "aws_security_group" "bastion" {
  count       = "${var.bastion_instance ? 1 : 0}"
  name        = "${var.prefix}-bastion"
  description = "Bastion instance security group"
  vpc_id      = "${aws_vpc.vpc.id}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-bastion"
    Environment    = "${var.environment}"
    Project        = "${var.project}"
    Product        = "VDMS"
    Owner          = "${var.owner}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_security_group_rule" "bastion-ingress" {
  count             = "${var.bastion_instance ? 1 : 0}"
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = "${aws_security_group.bastion.id}"
  cidr_blocks       = ["${var.vpc_cidr_block}"]
  description       = "All Access for internal network"
}

resource "aws_security_group_rule" "bastion-egress" {
  count             = "${var.bastion_instance ? 1 : 0}"
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = "${aws_security_group.bastion.id}"
  cidr_blocks       = ["0.0.0.0/0"]
  description       = "All Access for outbound"
}

resource "aws_iam_role" "bastion" {
  count    = "${var.bastion_instance && var.enable_ssm ? 1 : 0}"
  name  = "${var.prefix}-bastion"

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

resource "aws_iam_role_policy_attachment" "bastion" {
  count    = "${var.bastion_instance && var.enable_ssm ? 1 : 0}"
  role       = "${aws_iam_role.bastion.name}"
  policy_arn = "${data.terraform_remote_state.iam.ssm_core_policy_arn}"
}

resource "aws_iam_instance_profile" "bastion" {
  count    = "${var.bastion_instance && var.enable_ssm ? 1 : 0}"
  name  = "${var.prefix}-bastion"
  role  = "${aws_iam_role.bastion.name}"
}

resource "aws_launch_configuration" "bastion" {
  count         = "${var.bastion_instance ? local.bastion_instance_count : 0}"
  name_prefix   = "${var.prefix}-bastion-${element(data.aws_availability_zones.zones.names, count.index)}"
  image_id      = "${var.baseos_rhel7_ami_id}"
  instance_type = "${var.bastion_instance_type}"
  user_data = "${element(concat(data.template_file.bastion.*.rendered, list("")), 0)}"
  iam_instance_profile = "${var.enable_ssm ? element(concat(aws_iam_instance_profile.bastion.*.name, list("")), 0) : ""}"

  security_groups = [
    "${aws_security_group.bastion.id}",
    "${aws_security_group.vpn-remote-access.*.id}",
    "${aws_security_group.ssh-remote-access.*.id}",
  ]

  key_name                    = "${local.platform_keypair}"
  associate_public_ip_address = "${var.bastion_use_public_ip ? true : false}"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "bastion" {
  count                = "${var.bastion_instance ? local.bastion_instance_count : 0}"
  vpc_zone_identifier  = ["${element(aws_subnet.pub.*.id, count.index)}"]
  name                 = "${var.prefix}-bastion-${element(data.aws_availability_zones.zones.names, count.index)}"
  min_size             = "${local.bastion_asg_min_count}"
  max_size             = 1
  desired_capacity     = 1
  force_delete         = true
  launch_configuration = "${element(aws_launch_configuration.bastion.*.id, count.index)}"

  tag {
    key                 = "Name"
    value               = "${var.prefix}-bastion-${element(data.aws_availability_zones.zones.names, count.index)}"
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
    key                 = "Product"
    value               = "VDMS"
    propagate_at_launch = true
  }

  tag {
    key                 = "BuildUrl"
    value               = "${var.build_url}"
    propagate_at_launch = true
  }

  tag {
    key                 = "ExpirationDate"
    value               = "${var.expiration_date}"
    propagate_at_launch = true
  }

  tag {
    key                 = "Role"
    value               = "${var.prefix}-bastion"
    propagate_at_launch = true
  }

  tag {
    key                 = "Schedule"
    value               = "${var.instance_schedule}"
    propagate_at_launch = true
  }
}

data "template_file" "bastion" {
  count    = "${var.bastion_instance ? 1 : 0}"
  template = "${file("${path.module}/templates/userdata-bastion.sh.tpl")}"

  vars {
    install_ssm_agent = "${var.install_ssm_agent}"
  }
}
