terraform {
  backend "s3" {
    acl                    = "bucket-owner-full-control"
    encrypt                = true
    skip_region_validation = true
  }
}
