output "endpoint_psql11" {
  description = "A list of all cluster instance endpoints"
  value = var.enable_psql ? module.aurora11[0].this_rds_cluster_endpoint : "dummy"
}

output "reader_endpoint_psql11" {
  description = "The cluster reader endpoint"
  value = var.enable_psql ? module.aurora11[0].this_rds_cluster_reader_endpoint : "dummy"
}

output "port" {
  description = "Port used for the RDS instance"
  value       = module.aurora11[*].this_rds_cluster_port
}

output "master_username_psql11" {
  description = "The master username for RDS instance"
  value       = module.aurora11[*].this_rds_cluster_master_username
}

output "master_database_name_psql11" {
  description = "Name for an automatically created database on cluster creation"
  value       = module.aurora11[*].this_rds_cluster_database_name
}
