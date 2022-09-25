output "records" {
  value = formatlist("%s.${var.hosted_zone_dns}", var.subdomains)
}
