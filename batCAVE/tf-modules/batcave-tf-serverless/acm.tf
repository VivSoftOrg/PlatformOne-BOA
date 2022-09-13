data "aws_acm_certificate" "acm_certificate" {
  count       = var.create_custom_domain ? 1 : 0
  domain      = var.base_domain
  types       = ["AMAZON_ISSUED"]
  most_recent = true
}

