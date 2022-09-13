output "cluster_endpoint" {
  description = "The cluster endpoint"
  value       = var.enable_mysql ? module.aurora_mysql[0].this_rds_cluster_endpoint : "dummy"
}

output "this_rds_cluster_reader_endpoint" {
  description = "The cluster reader endpoint"
  value       = var.enable_mysql ? module.aurora_mysql[0].this_rds_cluster_reader_endpoint : "dummy"
}

output "port" {
  description = "Port used for the RDS instance"
  value       = module.aurora_mysql[*].this_rds_cluster_port
}

output "master_username_mysql" {
  description = "The master username for RDS instance"
  value       = module.aurora_mysql[*].this_rds_cluster_master_username
}

output "master_database_name_mysql" {
  description = "Name for an automatically created database on cluster creation"
  value       = module.aurora_mysql[*].this_rds_cluster_database_name
}