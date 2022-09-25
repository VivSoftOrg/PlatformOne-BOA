variable "name" {
  default = "cms"
}
variable "description" {
  default = "KMS key"
}
  
variable "deletion_window_in_days" {
  default = "10"
}

variable "key_usage" {
  default = "ENCRYPT_DECRYPT"
}
  
variable "customer_master_key_spec" {
  default = "SYMMETRIC_DEFAULT"
}

variable "is_enabled" {
  default = "true"
}
  
variable "enable_key_rotation" {
  default = "true"
}

variable "multi_region" {
  default = "false"
}
