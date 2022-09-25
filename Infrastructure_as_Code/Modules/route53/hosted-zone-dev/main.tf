locals {
  /*
  `dns_suffix` exists because overlapping R53 private zones are not allowed.
  In prod, a private r53 zone is created to support admin only routes, and follows the format *.admin.<il>.dsop.io.
    In dev, the admin route is still required, but a top level route of *.<il>.dsop.io is required so that we can re-use
    the same public application dns entries in dev as we would in prod.  Since *.admin.<il>.dsop.io and *.<il>.dsop.io
    cannot exist together on the same VPC, we use TF logic to create *.<il>.dsop.io on dev and append ".admin" to every
    persistent admin route.
  Also, now that multiple clusters share the same VPC, each cluster needs its own R53 private zones, and these zones
    cannot overlap, the cluster name has been prepended to the domain (ln20). This means that the cluster name can only
    consist of letters, numbers, dots (.) and dashes (-) in order to form a valid URL (i.e. no underscores or other
    characters).
  Open to suggestions for better ideas.
  */
  dns_suffix    = "-admin"
  dns_suffix_db = ".admin"
}

###########################################################
# R53 Zones
###########################################################
resource "aws_route53_zone" "private" {
  name = var.private_dns_zone_name

  vpc {
    vpc_id = var.vpc_id
  }

  comment = var.cluster_name

  tags = merge({}, var.cluster_tags)
}

# ###########################################################
# # R53 Records
# ###########################################################
resource "aws_route53_record" "jira" {

  name    = "jira"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "vtc" {
  name    = "vtc"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.jitsi_meet_lb_dns]
}

resource "aws_route53_record" "static-sites" {
  name    = "sso-info"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "airmencoders" {
  name    = "airmencoders"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "onboarding" {
  name    = "onboarding"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "bespin" {
  name    = "bespin"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "spacecamp" {
  name    = "spacecamp"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "arcwerx" {
  name    = "arcwerx"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "commentbox" {
  name    = "commentbox-fe"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "corsairranch" {
  name    = "corsairranch"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "fortify" {
  name    = "fortify"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}


resource "aws_route53_record" "p1" {
  name    = "p1"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "levelup" {
  name    = "levelup"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "confluence" {
  name    = "confluence"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "gitlab" {
  name    = "code"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "gitlab-registry" {
  name    = "registry"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "sonarqube" {
  name    = "sonarqube"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "chat-internal" {
  name    = "chat"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

// Private only routes that *always* exist
resource "aws_route53_record" "argocd" {
  name    = "argocd"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.admin_elb_dns_name]
}

resource "aws_route53_record" "twistlock" {
  name    = "twistlock"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.admin_elb_dns_name]
}

resource "aws_route53_record" "anchore" {
  name    = "anchore"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.admin_elb_dns_name]
}

resource "aws_route53_record" "anchore-api" {
  name    = "anchore-api"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.admin_elb_dns_name]
}

resource "aws_route53_record" "grafana" {
  name    = "grafana"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.admin_elb_dns_name]
}

resource "aws_route53_record" "prometheus" {
  name    = "prometheus"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.admin_elb_dns_name]
}

resource "aws_route53_record" "alertmanager" {
  name    = "alertmanager"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.admin_elb_dns_name]
}

resource "aws_route53_record" "kiali" {
  name    = "kiali"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.admin_elb_dns_name]
}

resource "aws_route53_record" "tracing" {
  name    = "tracing"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.admin_elb_dns_name]
}

# Postgres11 DB's
resource "aws_route53_record" "anchore-psql-db11" {

  name    = "anchore-db"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.anchore_db_endpoint]
}

resource "aws_route53_record" "anchore-psql-db11-reader" {

  name    = "anchore-dbreader"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.anchore_db_reader_endpoint]
}

resource "aws_route53_record" "confluence-psql-db11" {

  name    = "confluence-db"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.confluence_db_endpoint]
}

resource "aws_route53_record" "confluence-psql-db11-reader" {

  name    = "db-reader11.confluence"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.confluence_db_reader_endpoint]
}

resource "aws_route53_record" "gitlab-psql-db11" {

  name    = "gitlab-db"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.gitlab_db_endpoint]
}

resource "aws_route53_record" "gitlab-psql-db11-reader" {

  name    = "gitlab-dbreader"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.gitlab_db_reader_endpoint]
}

resource "aws_route53_record" "grafana-psql-db11" {

  name    = "grafana-db"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.grafana_db_endpoint]
}

resource "aws_route53_record" "grafana-psql-db11-reader" {

  name    = "db-reader11.grafana"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.grafana_db_reader_endpoint]
}

resource "aws_route53_record" "jira-psql-db11" {
  name    = "jira-db"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.jira_db_endpoint]
}

resource "aws_route53_record" "jira-psql-db11-reader" {

  name    = "db-reader11.jira"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.jira_db_reader_endpoint]
}

resource "aws_route53_record" "mattermost-psql-db11" {

  name    = "mattermost-db"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.mattermost_db_endpoint]
}

resource "aws_route53_record" "mattermost-psql-db11-reader" {

  name    = "mattermost-dbreader"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.mattermost_db_reader_endpoint]
}

resource "aws_route53_record" "sdelements-psql-db11" {

  name    = "sdelements-db"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.sdelements_db_endpoint]
}

resource "aws_route53_record" "sdelements-psql-db11-reader" {

  name    = "db-reader11.sdelements"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.sdelements_db_reader_endpoint]
}

resource "aws_route53_record" "sonarqube-psql-db11" {

  name    = "db11.sonarqube"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.sonarqube_db_endpoint]
}

resource "aws_route53_record" "sonarqube-psql-db11-reader" {

  name    = "db-reader11.sonarqube"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.sonarqube_db_reader_endpoint]
}

# MySQL DB's
resource "aws_route53_record" "fortify-db-mysql" {

  name    = "fortify-db"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.fortify_db_endpoint]
}

resource "aws_route53_record" "fortify-db-mysql-reader" {

  name    = "db-mysql-reader.fortify"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.fortify_db_reader_endpoint]
}

# More Misc. Records
resource "aws_route53_record" "sdelements" {
  name    = "sdelements"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "oteguide" {
  name    = "oteguide"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "afcc" {
  name    = "afcc"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "launchboard" {
  name    = "launchboard"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "navalletter" {
  name    = "naval-letter"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "p1collab" {
  name    = "p1-collab"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "stoplight" {
  name    = "stoplight"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "nexus" {
  name    = "nexus"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.apps_elb_dns_name]
}

resource "aws_route53_record" "odoo" {
  name    = "odoo"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.appgate_elb_dns_name]
}

resource "aws_route53_record" "odoo-db" {
  name    = "odoo-db"
  type    = "CNAME"
  ttl     = var.dns_ttl
  zone_id = aws_route53_zone.private.zone_id
  records = [var.odoo_db_endpoint]
}
