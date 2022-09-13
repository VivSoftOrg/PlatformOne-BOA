resource "aws_key_pair" "workloadkey" {
  lifecycle {
    ignore_changes = ["public_key"]
  }

  key_name   = "${var.environment}-${var.project}-workload-${var.account_code}"
  public_key = "${file("${var.output_dir}/ssh-keys/${var.account_code}/${var.environment}-${var.project}-workload-${var.account_code}.pub")}"
}

resource "aws_s3_bucket_object" "workloadkey-pvt" {
  depends_on = ["aws_key_pair.workloadkey"]

  lifecycle {
    ignore_changes = ["source"]
  }

  bucket                 = "${local.platform_bucket}"
  key                    = "ssh-keys/${var.account_code}/${var.environment}-${var.project}-workload-${var.account_code}"
  source                 = "${var.output_dir}/ssh-keys/${var.account_code}/${var.environment}-${var.project}-workload-${var.account_code}"
  server_side_encryption = "aws:kms"
  kms_key_id             = "${aws_kms_key.ssh-keys.arn}"
  acl                    = "bucket-owner-full-control"
}

resource "aws_s3_bucket_object" "workloadkey-pub" {
  depends_on = ["aws_key_pair.workloadkey"]

  lifecycle {
    ignore_changes = ["source"]
  }

  bucket                 = "${local.platform_bucket}"
  key                    = "ssh-keys/${var.account_code}/${var.environment}-${var.project}-workload-${var.account_code}.pub"
  source                 = "${var.output_dir}/ssh-keys/${var.account_code}/${var.environment}-${var.project}-workload-${var.account_code}.pub"
  server_side_encryption = "aws:kms"
  kms_key_id             = "${aws_kms_key.ssh-keys.arn}"
  acl                    = "bucket-owner-full-control"
}
