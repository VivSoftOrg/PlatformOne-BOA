locals {
  application             = "gitlab"
  enable_psql             = false
  rds_deletion_protection = false
  replica_count           = 1
  instance_type           = "db.r4.large"
}
