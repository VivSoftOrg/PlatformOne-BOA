output "endpoint_psql" {
  description = "A list of all cluster instance endpoints"
  value = var.enable_psql ? module.aurora_postgres[0].rds_cluster_endpoint : "dummy"
}

output "reader_endpoint_psql" {
  description = "The cluster reader endpoint"
  value = var.enable_psql ? module.aurora_postgres[0].rds_cluster_reader_endpoint : "dummy"
}

output "engine_version" {
  description = "The cluster engine version"
  value       = module.aurora_postgres[*].rds_cluster_engine_version
}

output "port" {
  description = "Port used for the RDS instance"
  value       = module.aurora_postgres[*].rds_cluster_port
}

output "master_username_psql" {
  description = "The master username for RDS instance"
  value       = module.aurora_postgres[*].rds_cluster_master_username
  sensitive   = true
}

output "master_database_name_psql" {
  description = "Name for an automatically created database on cluster creation"
  value       = module.aurora_postgres[*].rds_cluster_database_name
}
