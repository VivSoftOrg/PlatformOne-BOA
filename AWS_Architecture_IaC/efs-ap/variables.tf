variable "name" {
  type        = string
  description = "Name to prefix to created resources"
}

variable "create_efs" {
  type        = bool
  default     = false
  description = "toggle to create efs or not"
}

variable "efs_id" {
  type        = string
  description = "efs id to mount"
}
variable "gid" {
  type =  string
  default = ""
}

variable "uid" {
  type = string 
  default = "" 
}

variable "secondary_gids" {
  type = list(string)
  default = [""]
}

variable "mount_path" {
  type = string
  default= ""
}