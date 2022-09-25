
# ###########################################################
# # R53 Zones
# ###########################################################
# resource "aws_route53_zone" "private_admin_mil" {
#   name  = var.mil_private_dns_zone_name

#   vpc {
#     vpc_id = var.vpc_id
#   }

#   comment = var.cluster_name

#   tags = merge({}, var.cluster_tags)
# }

# // Private only routes that *always* exist
# resource "aws_route53_record" "argocd_mil" {
#   name    = "argocd-dsop-${var.cluster_env}"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private_admin_mil.zone_id
#   records = [var.admin_elb_dns_name]
# }

# resource "aws_route53_record" "twistlock_mil" {
#   name    = "twistlock-${var.cluster_env}"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private_admin_mil.zone_id
#   records = [var.admin_elb_dns_name]
# }

# resource "aws_route53_record" "anchore_mil" {
#   name    = "anchore-${var.cluster_env}"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private_admin_mil.zone_id
#   records = [var.admin_elb_dns_name]
# }

# resource "aws_route53_record" "anchore-api_mil" {
#   name    = "anchore-api-${var.cluster_env}"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private_admin_mil.zone_id
#   records = [var.admin_elb_dns_name]
# }

# resource "aws_route53_record" "grafana_mil" {
#   name    = "grafana-${var.cluster_env}"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private_admin_mil.zone_id
#   records = [var.admin_elb_dns_name]
# }

# resource "aws_route53_record" "prometheus_mil" {
#   name    = "prometheus-${var.cluster_env}"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private_admin_mil.zone_id
#   records = [var.admin_elb_dns_name]
# }

# resource "aws_route53_record" "alertmanager_mil" {
#   name    = "alertmanager-${var.cluster_env}"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private_admin_mil.zone_id
#   records = [var.admin_elb_dns_name]
# }

# resource "aws_route53_record" "kiali_mil" {
#   name    = "kiali-${var.cluster_env}"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private_admin_mil.zone_id
#   records = [var.admin_elb_dns_name]
# }

# resource "aws_route53_record" "tracing_mil" {
#   name    = "tracing-${var.cluster_env}"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private_admin_mil.zone_id
#   records = [var.admin_elb_dns_name]
# }


# # Postgres11 DB's
# resource "aws_route53_record" "anchore-psql-db11" {
#   count = var.anchore_db_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db11.anchore"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.anchore_db_endpoint]
# }

# resource "aws_route53_record" "anchore-psql-db11-reader" {
#   count = var.anchore_db_reader_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db-reader11.anchore"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.anchore_db_reader_endpoint]
# }

# resource "aws_route53_record" "confluence-psql-db11" {
#   count   = var.confluence_db_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db11.confluence"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.confluence_db_endpoint]
# }

# resource "aws_route53_record" "confluence-psql-db11-reader" {
#   count   = var.confluence_db_reader_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db-reader11.confluence"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.confluence_db_reader_endpoint]
# }

# # Gitlab DBSs
# resource "aws_route53_record" "gitlab-psql-db11" {
#   count   = var.gitlab_db_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db11.gitlab"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.gitlab_db_endpoint]
# }

# resource "aws_route53_record" "gitlab-psql-db11-reader" {
#   count   = var.gitlab_db_reader_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db-reader11.gitlab"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.gitlab_db_reader_endpoint]
# }

# # Grafana DB's
# resource "aws_route53_record" "grafana-psql-db11" {
#   count   = var.grafana_db_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db11.grafana"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.grafana_db_endpoint]
# }

# resource "aws_route53_record" "grafana-psql-db11-reader" {
#   count   = var.grafana_db_reader_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db-reader11.grafana"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.grafana_db_reader_endpoint]
# }

# # Jira DB's
# resource "aws_route53_record" "jira-psql-db11" {
#   count   = var.jira_db_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db11.jira"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.jira_db_endpoint]
# }

# resource "aws_route53_record" "jira-psql-db11-reader" {
#   count   = var.jira_db_reader_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db-reader11.jira"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.jira_db_reader_endpoint]
# }

# # Mattermost DB's
# resource "aws_route53_record" "mattermost-psql-db11" {
#   count   = var.mattermost_db_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db11.mattermost"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.mattermost_db_endpoint]
# }

# resource "aws_route53_record" "mattermost-psql-db11-reader" {
#   count   = var.mattermost_db_reader_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db-reader11.mattermost"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.mattermost_db_reader_endpoint]
# }

# # SDElement DB's
# resource "aws_route53_record" "sdelements-psql-db11" {
#   count   = var.sdelements_db_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db11.sdelements"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.sdelements_db_endpoint]
# }

# resource "aws_route53_record" "sdelements-psql-db11-reader" {
#   count   = var.sdelements_db_reader_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db-reader11.sdelements"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.sdelements_db_reader_endpoint]
# }

# # Sonarqube DB's
# resource "aws_route53_record" "sonarqube-psql-db11" {
#   count   = var.sonarqube_db_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db11.sonarqube"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.sonarqube_db_endpoint]
# }

# resource "aws_route53_record" "sonarqube-psql-db11-reader" {
#   count   = var.sonarqube_db_reader_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db-reader11.sonarqube"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.sonarqube_db_reader_endpoint]
# }

# # MySQL DB's
# resource "aws_route53_record" "fortify-db-mysql" {
#   count = var.fortify_db_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db-mysql.fortify"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.fortify_db_endpoint]
# }

# resource "aws_route53_record" "fortify-db-mysql-reader" {
#   count = var.fortify_db_reader_endpoint == "https://no.database.enabled" ? 0 : 1

#   name    = "db-mysql-reader.fortify"
#   type    = "CNAME"
#   ttl     = var.dns_ttl
#   zone_id = aws_route53_zone.private.zone_id
#   records = [var.fortify_db_reader_endpoint]
# }

