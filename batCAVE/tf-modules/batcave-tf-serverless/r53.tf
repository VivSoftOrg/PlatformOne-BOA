locals {
  create_route53_records_count = var.route53_zone_type == "" ? 0 : 1
}

data "aws_route53_zone" "dns" {
  count        = local.create_route53_records_count
  name         = var.base_domain
  private_zone = var.route53_zone_type == "private"
}

resource "aws_route53_record" "dns" {
  count           = local.create_route53_records_count
  zone_id         = data.aws_route53_zone.dns[0].zone_id
  name            = "${var.custom_subdomain}.${var.base_domain}"
  type            = "CNAME"
  ttl             = "300"
  allow_overwrite = true
  records         = [module.alb.lb_dns_name]
}
