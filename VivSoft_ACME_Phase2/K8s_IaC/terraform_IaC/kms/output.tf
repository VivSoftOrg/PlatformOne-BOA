################################################################################
# AWS KMS Key
################################################################################
output "arn" {
  value = aws_kms_key.this.arn
}

output "key_id" {
  value = aws_kms_key.this.key_id
}

output "tags" {
  value = aws_kms_key.this.tags_all
}
