# S3 buckets for landing zone
resource "aws_s3_bucket" "landing_zone_buckets" {
  count  = length(var.s3_bucket_names)
  bucket = var.s3_bucket_names[count.index]
  force_destroy = var.force_destroy
}

resource "aws_s3_bucket_acl" "example" {
  bucket = aws_s3_bucket.landing_zone_buckets[0].id
  acl    = "private"
}

# resource "aws_s3_bucket_policy" "bucket_policy" {
#   count  = length(var.s3_bucket_names)
#   bucket = var.s3_bucket_names[count.index]
#   policy = data.aws_iam_policy_document.bucket_policy.json
# }

# data "aws_iam_policy_document" "bucket_policy" {
#   statement {
#     effect = "Allow"
#     actions = [
#       "s3:ListBucket",
#       "s3:PutObject",
#       "s3:GetObject",
#       "s3:DeleteObject",
#       "s3:PutObjectAcl"
#     ]
#     resources = [
#       "arn:aws:s3:::git-lfs",
#     ]
#   }
# }
