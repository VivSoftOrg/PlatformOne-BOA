resource "aws_cloudwatch_log_group" "flow_log" {
  name = "${var.prefix}-vpc_flowlog"
}

resource "aws_iam_role" "flow_log" {
  name               = "${var.prefix}-vpc_flowlog"
  assume_role_policy = "${data.aws_iam_policy_document.flow_log-assumerole.json}"
}

resource "aws_iam_role_policy" "flow_log" {
  name   = "${var.prefix}-vpc_flowlog"
  role   = "${aws_iam_role.flow_log.id}"
  policy = "${data.aws_iam_policy_document.flow_log.json}"
}

resource "aws_flow_log" "flow_log" {
  log_destination = "${aws_cloudwatch_log_group.flow_log.arn}"
  iam_role_arn   = "${aws_iam_role.flow_log.arn}"
  vpc_id         = "${aws_vpc.vpc.id}"
  traffic_type   = "${var.flow_log_traffic_type}"
}

# RD-730 - Giving the VPC service access to logs:CreateLogGroup can prevent an apply, destroy, apply from working
# https://github.com/hashicorp/terraform/issues/14750
# Removing the logs:CreateLogGroup permission will prevent the VPC service from recreating the Log Group.
# The downside is that the VPC Flow log console will display this message:
# The IAM role for your flow logs does not have sufficient permissions to send logs to the CloudWatch log group.
data "aws_iam_policy_document" "flow_log" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
    ]

    resources = [
      "*",
    ]
  }
}

data "aws_iam_policy_document" "flow_log-assumerole" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    principals = {
      type        = "Service"
      identifiers = ["vpc-flow-logs.amazonaws.com"]
    }
  }
}
