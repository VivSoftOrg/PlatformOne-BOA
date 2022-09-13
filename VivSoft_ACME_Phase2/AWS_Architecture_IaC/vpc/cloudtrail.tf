resource "aws_cloudtrail" "cloudtrail" {
  count      = "${var.external_cloudtrail ? 0 : 1}"
  depends_on = ["aws_s3_bucket_policy.cloudtrail"]

  name                          = "${var.prefix}-cloudtrail"
  s3_bucket_name                = "${aws_s3_bucket.cloudtrail.id}"
  enable_logging                = true
  include_global_service_events = true
}

resource "aws_s3_bucket" "cloudtrail" {
  count         = "${var.external_cloudtrail ? 0 : 1}"
  bucket        = "${lower(var.client_code)}-${lower(var.prefix)}-cloudtrail"
  region        = "${data.aws_region.current.name}"
  acl           = "log-delivery-write"
  force_destroy = true

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.client_code}-${var.prefix}-cloudtrail"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Product        = "VDMS"
    BuildUrl       = "${var.build_url}"
    Project        = "${var.project}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_s3_bucket_policy" "cloudtrail" {
  count  = "${var.external_cloudtrail ? 0 : 1}"
  bucket = "${aws_s3_bucket.cloudtrail.id}"
  policy = "${data.aws_iam_policy_document.cloudtrail.json}"

  lifecycle {
    ignore_changes = ["policy"]
  }
}

data "aws_iam_policy_document" "cloudtrail" {
  count = "${var.external_cloudtrail ? 0 : 1}"

  statement {
    sid    = "AWSCloudTrailAclCheck"
    effect = "Allow"

    actions = [
      "s3:GetBucketAcl",
    ]

    principals = {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    resources = [
      "arn:${data.aws_partition.current.partition}:s3:::${aws_s3_bucket.cloudtrail.id}",
    ]
  }

  statement {
    sid    = "AWSCloudTrailWrite"
    effect = "Allow"

    actions = [
      "s3:PutObject",
    ]

    principals = {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    resources = [
      "arn:${data.aws_partition.current.partition}:s3:::${aws_s3_bucket.cloudtrail.id}/*",
    ]

    condition = {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }
  }
}
