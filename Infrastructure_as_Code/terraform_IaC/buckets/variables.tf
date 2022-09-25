variable "s3_bucket_names" {
  type = list(string)
  default = []
}

variable "force_destroy" {
  default = true
}
