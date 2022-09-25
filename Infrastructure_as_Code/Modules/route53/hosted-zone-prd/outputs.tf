# output "cypress_test_endpoints_mil" {
#   value = var.dns_dev ? [] : [
#     aws_route53_record.argocd_mil[0],
#     aws_route53_record.twistlock_mil[0],
#     aws_route53_record.anchore_mil[0],
#     aws_route53_record.anchore-api_mil[0],
#     aws_route53_record.grafana_mil[0],
#     aws_route53_record.prometheus_mil[0],
#     aws_route53_record.alertmanager_mil[0],
#     aws_route53_record.kiali_mil[0],
#     aws_route53_record.tracing_mil[0],
#     aws_route53_record.db_mil[0],
#     aws_route53_record.db-reader_mil[0],
#     aws_route53_record.db-mysql_mil[0],
#     aws_route53_record.db11_mil[0],
#     aws_route53_record.db-reader11_mil[0]
#   ]
# }