output "zone_data" {
  value = data.aws_route53_zone.cms_zone
}

output "records" {
  value = toset(flatten([for mod in module.records : mod.records]))
}
