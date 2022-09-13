variable "environment" {
  default = "dev"
}
variable "ssh_public_key" {
  description = "public key to import and create keypair"
  type        = string
}

variable "bastion_instance_type" {
  description = "Bastion host instance type"
  type        = string
  default     = "t2.micro"
}

variable "bastion_ami_id" {
  description = "AMI ID to deploy bastion host"
  type        = string
}

variable "bastion_subnet_id" {
  description = "subnet to deploy bastion"
  type        = list(string)
}

variable "bastion_root_volume_size" {
  description = "Size of the root volume for bastion host"
  type        = number
  default     = 100
}

variable "cluster_name" {
  description = "Name of the cluster"
  type        = string
}

variable "tags" {
  description = "Map of tags to add to all resources created"
  default     = {}
  type        = map(string)
}

variable "vpc_id" {
  description = "VPC ID to create security groups"
  type        = string
}

variable "enable_bastion" {
  type        = string
  description = "disable or enable bastion"
}

variable "worker_security_group_id" {}

variable "cluster_security_group_id" {}

variable "cluster_primary_security_group_id" {}
