resource "aws_key_pair" "corekey" {
  lifecycle {
    ignore_changes = ["public_key"]
  }

  key_name   = "${var.environment}-${var.project}-core"
  public_key = "${file("${var.output_dir}/ssh-keys/${var.account_code}/${var.environment}-${var.project}-core.pub")}"
}

resource "aws_s3_bucket_object" "corekey-pvt" {
  depends_on = ["aws_key_pair.corekey"]

  lifecycle {
    ignore_changes = ["source"]
  }

  bucket                 = "${local.platform_bucket}"
  key                    = "ssh-keys/${var.account_code}/${var.environment}-${var.project}-core"
  source                 = "${var.output_dir}/ssh-keys/${var.account_code}/${var.environment}-${var.project}-core"
  server_side_encryption = "aws:kms"
  kms_key_id             = "${aws_kms_key.ssh-keys.arn}"
  acl                    = "bucket-owner-full-control"
}

resource "aws_s3_bucket_object" "corekey-pub" {
  depends_on = ["aws_key_pair.corekey"]

  lifecycle {
    ignore_changes = ["source"]
  }

  bucket                 = "${local.platform_bucket}"
  key                    = "ssh-keys/${var.account_code}/${var.environment}-${var.project}-core.pub"
  source                 = "${var.output_dir}/ssh-keys/${var.account_code}/${var.environment}-${var.project}-core.pub"
  server_side_encryption = "aws:kms"
  kms_key_id             = "${aws_kms_key.ssh-keys.arn}"
  acl                    = "bucket-owner-full-control"
}
