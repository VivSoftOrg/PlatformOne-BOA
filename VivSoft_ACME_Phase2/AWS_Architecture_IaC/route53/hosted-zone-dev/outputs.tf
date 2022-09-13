output "argocd_fqdn" {
  value = aws_route53_record.argocd.fqdn
}


// Endpoints
output "cypress_test_endpoints" {
  value = [
    aws_route53_record.argocd.fqdn,
    aws_route53_record.arcwerx.fqdn,
    aws_route53_record.spacecamp.fqdn,
    aws_route53_record.stoplight.fqdn,
    aws_route53_record.afcc.fqdn,
    aws_route53_record.launchboard.fqdn,
    aws_route53_record.navalletter.fqdn,
    aws_route53_record.p1collab.fqdn,
    aws_route53_record.alertmanager.fqdn,
    aws_route53_record.grafana.fqdn,
    aws_route53_record.prometheus.fqdn,
    aws_route53_record.kiali.fqdn,
    aws_route53_record.tracing.fqdn,
    aws_route53_record.twistlock.fqdn,
    aws_route53_record.anchore.fqdn,
    aws_route53_record.anchore-api.fqdn,
    aws_route53_record.jira.fqdn,
    aws_route53_record.confluence.fqdn,
    aws_route53_record.static-sites.fqdn,
    aws_route53_record.airmencoders.fqdn,
    aws_route53_record.oteguide.fqdn,
    aws_route53_record.onboarding.fqdn,
    aws_route53_record.bespin.fqdn,
    aws_route53_record.commentbox.fqdn,
    aws_route53_record.corsairranch.fqdn,
    aws_route53_record.p1.fqdn,
    aws_route53_record.levelup.fqdn,
    aws_route53_record.gitlab.fqdn,
    aws_route53_record.gitlab-registry.fqdn,
    aws_route53_record.chat-internal.fqdn,
    aws_route53_record.sdelements.fqdn,
    aws_route53_record.sonarqube.fqdn,
    aws_route53_record.vtc.fqdn
  ]
}

# output "database_endpoints" {
#   value = [
#     aws_route_53_record.anchore-psql-db11.fqdn,
#     aws_route_53_record.anchore-psql-db11-reader.fqdn,
#     aws_route_53_record.confluence-psql-db11.fqdn,
#     aws_route_53_record.confluence-psql-db11-reader.fqdn,
#     aws_route_53_record.gitlab-psql-db11.fqdn,
#     aws_route_53_record.gitlab-psql-db11-reader.fqdn,
#     aws_route_53_record.grafana-psql-db11.fqdn,
#     aws_route_53_record.grafana-psql-db11-reader.fqdn,
#     aws_route_53_record.jira-psql-db11.fqdn,
#     aws_route_53_record.jira-psql-db11-reader.fqdn,
#     aws_route_53_record.mattermost-psql-db11.fqdn,
#     aws_route_53_record.mattermost-psql-db11-reader.fqdn,
#     aws_route_53_record.sdelements-psql-db11.fqdn,
#     aws_route_53_record.sdelements-psql-db11-reader.fqdn,
#     aws_route_53_record.sonarqube-psql-db11.fqdn,
#     aws_route_53_record.sonarqube-psql-db11-reader.fqdn,
#     aws_route_53_record.fortify-db-mysql.fqdn,
#     aws_route_53_record.fortify-db-mysql-reader.fqdn,
#   ]
# }

# output "database_endpoints" {
#   value = [for i in "${aws_route_53_record.*.fqdn}": i if regex("^db.*", i) ]
# }

output "anchore-db-endpoint" {
  value = aws_route53_record.anchore-psql-db11.fqdn
}

output "fortify-db-endpoint" {
  value = aws_route53_record.fortify-db-mysql.fqdn
}

output "sdelements-db-endpoint" {
  value = aws_route53_record.sdelements-psql-db11.fqdn
}

output "mattermost-db-endpoint" {
  value = aws_route53_record.mattermost-psql-db11.fqdn
}

output "mattermost-db-reader" {
  value = aws_route53_record.mattermost-psql-db11-reader.fqdn
}
output "grafana-db-endpoint" {
  value = aws_route53_record.grafana-psql-db11.fqdn
}

output "confluence-db-endpoint" {
  value = aws_route53_record.confluence-psql-db11.fqdn
}

output "jira-db-endpoint" {
  value = aws_route53_record.jira-psql-db11.fqdn
}

output "gitlab-db-endpoint" {
  value = aws_route53_record.gitlab-psql-db11.fqdn
}

output "odoo-end-point" {
  value = aws_route53_record.odoo.fqdn
}

output "odoo-db-endpoint" {
  value = aws_route53_record.odoo-db.fqdn
}