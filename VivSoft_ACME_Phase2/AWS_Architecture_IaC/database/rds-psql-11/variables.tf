variable "enable_psql" {
  description = "whether to enable psql database for the application"
  default     = "false"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID to create security groups"
  type        = string
}

variable "application" {
  description = "Application Name"
  type        = string
}

variable "private_subnet_ids" {
  description = "Subnet ids of the cluster private environment"
  type        = list(string)
}

variable "rds_db_name" {
  description = "Database name"
  type        = string
}

variable "rds_username" {
  description = "Username for PSQL user"
  type        = string
}

variable "rds_password" {
  description = "Password for PSQL user"
  type        = string
}

variable "access_sg_ids" {
  description = "Security groups authorized to connect to the database"
  type        = list(string)
}

variable "replica_count" {
  type    = number
  default = 1
}

variable "instance_type" {
  type    = string
  default = "db.r4.large"
}

variable "rds_deletion_protection" {
  type        = bool
  description = "Whether to protect the database from deletion"
}

variable "name" {
  type        = string
  description = "Name of the cluster"
}

variable "cluster_tags" {
  description = "Map of tags to add to all resources created"
  default     = {}
  type        = map(string)
}