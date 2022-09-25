variable "cluster_name" {
  type        = string
  description = "General cluster name to append to AWS resource names"
}

variable "cluster_tags" {
  type        = map(string)
  default     = {}
  description = "Resource tags used to identify cluster resources and its properties"
}

variable "dns_ttl" {
  //  TODO: This default is based on no real data whatsoever
  default = 10
}

// NOTE: This variable is set through pipeline environment variables
variable "private_dns_zone_name" {}

variable "vpc_id" {}

// Postgres SQL 11 RDS endpoints
variable "apps_elb_dns_name" {}
variable "admin_elb_dns_name" {}
variable "appgate_elb_dns_name" {}
variable "anchore_db_endpoint" {}
variable "anchore_db_reader_endpoint" {}
variable "confluence_db_endpoint" {}
variable "confluence_db_reader_endpoint" {}
variable "gitlab_db_endpoint" {}
variable "gitlab_db_reader_endpoint" {}
variable "grafana_db_endpoint" {}
variable "grafana_db_reader_endpoint" {}
variable "jira_db_endpoint" {}
variable "jira_db_reader_endpoint" {}
variable "mattermost_db_endpoint" {}
variable "mattermost_db_reader_endpoint" {}
variable "sdelements_db_endpoint" {}
variable "sdelements_db_reader_endpoint" {}
variable "sonarqube_db_endpoint" {}
variable "sonarqube_db_reader_endpoint" {}

// MySQL 11 RDS endpoints
variable "fortify_db_endpoint" {
  default = "dummy"
  type    = string
}
variable "fortify_db_reader_endpoint" {
  default = "dummy"
  type    = string
}

variable "odoo_db_endpoint" {
  default = "dummy"
  type    = string
}

variable "jitsi_meet_lb_dns" {}

