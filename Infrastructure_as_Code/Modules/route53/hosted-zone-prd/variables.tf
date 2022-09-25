variable "cluster_env" {}
variable "admin_elb_dns_name" {}
variable "apps_elb_dns_name" {}
variable "mil_private_dns_zone_name" {}
variable "vpc_id" {}
variable "cluster_name" {}

variable "cluster_tags" {
  type        = map(string)
  default     = {}
  description = "Resource tags used to identify cluster resources and its properties"
}

variable "dns_ttl" {
  //  TODO: This default is based on no real data whatsoever
  default = 10
}

// Postgres SQL 11 RDS endpoints
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
variable "fortify_db_endpoint" {}
variable "fortify_db_reader_endpoint" {}
