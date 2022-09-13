variable "enable_mysql" {
  description = "whether to enable mysql database for the application"
  default     = "false"
  type        = string
}

variable "application" {
  description = "Application Name"
  type        = string
}

variable "name" {
  type        = string
  description = "Name to prefix to created resources"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID to deploy to"
}

variable "cluster_tags" {
  type    = map(string)
  default = {}
}

variable "private_subnet_ids" {
  type    = list(string)
  default = []
}

variable "rds_deletion_protection" {
  type        = bool
  description = "Whether to protect the database from deletion"
}

variable "impact_level" {
  description = "the environment or impact level deployed"
  type        = string
}

# MySQL Inputs

variable "mysql_username" {
  type        = string
  description = "Username to use for mysql admin user"
}

variable "mysql_password" {
  type        = string
  description = "Password to use for mysql admin user"
}

variable "mysql_db_name" {
  type    = string
  default = "dbadmin"
}

variable "mysql_replica_count" {
  type    = number
  default = 1
}

variable "mysql_instance_type" {
  type    = string
  default = "db.r4.large"
}

variable "access_sg_ids" {
  type = list(string)
}
