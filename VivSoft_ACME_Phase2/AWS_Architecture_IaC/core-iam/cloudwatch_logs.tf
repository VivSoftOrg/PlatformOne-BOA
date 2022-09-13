# RD-323 - IAM policy to allow instance write access to CloudWatch Logs

data "aws_iam_policy_document" "cloudwatch_logs_write_access-document" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
    ]

    resources = [
      "arn:${data.aws_partition.current.partition}:logs:*:*:*",
    ]
  }
}

resource "aws_iam_policy" "cloudwatch_logs_write_access-policy" {
  name   = "${var.prefix}-cloudwatch_logs_write_access"
  policy = "${data.aws_iam_policy_document.cloudwatch_logs_write_access-document.json}"
}
