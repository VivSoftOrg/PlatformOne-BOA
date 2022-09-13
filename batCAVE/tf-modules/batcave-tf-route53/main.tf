# Extract existing data from AWS
data "aws_route53_zone" "cms_zone" {
  name         = var.hosted_zone_dns
  private_zone = true
}

module "records" {
  source = "./records"

  # Iterate over the provided map
  for_each = var.endpoint_subdomain_map

  hosted_zone_id  = data.aws_route53_zone.cms_zone.id
  hosted_zone_dns = var.hosted_zone_dns
  endpoint        = each.value.endpoint
  subdomains      = each.value.subdomains
  ttl             = var.ttl
}
