# -- Postgres11

module "aurora_postgres" {
  count = var.enable_psql ? 1 : 0

  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "5.2.0"

  name = "${var.name}-psql-${replace(var.engine_version, ".", "-")}"

  engine         = var.aurora_engine
  engine_version = var.engine_version

  vpc_id  = var.vpc_id
  subnets = var.private_subnet_ids

  username      = var.rds_username
  password      = var.rds_password
  database_name = var.rds_db_name

  create_random_password = false

  replica_count       = var.replica_count
  instance_type       = var.instance_type
  storage_encrypted   = true
  apply_immediately   = true
  skip_final_snapshot = true
  ca_cert_identifier  = var.ca_cert_identifier

  allowed_security_groups = aws_security_group.aurora-rds.*.id

  deletion_protection             = var.rds_deletion_protection
  db_parameter_group_name         = aws_db_parameter_group.aurora_db_postgres_parameter_group[count.index].id
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.aurora_cluster_postgres_parameter_group[count.index].id

  tags = merge(
  {
    application       = var.application
    terraform_managed = "true"
    component         = "database"
  },
  var.cluster_tags,
  )
}

resource "aws_security_group" "aurora-rds" {
  count = var.enable_psql ? 1 : 0

  name        = "${var.name}-psql-${replace(var.engine_version, ".", "-")}"
  description = "${var.name}-p1-k8s psql rds"
  vpc_id      = var.vpc_id
}

resource "aws_db_parameter_group" "aurora_db_postgres_parameter_group" {
  count = var.enable_psql ? 1 : 0

  name        = "${var.name}-psql-${replace(var.engine_version, ".", "-")}"
  family      = var.db_parameter_group
  description = "${var.name}-aurora-postgres-${replace(var.engine_version, ".", "-")}-parameter-group"
}

resource "aws_rds_cluster_parameter_group" "aurora_cluster_postgres_parameter_group" {
  count = var.enable_psql ? 1 : 0

  name        = "${var.name}-aurora-postgres-${replace(var.engine_version, ".", "-")}-cluster-parameter-group"
  family      = var.cluster_parameter_group
  description = "${var.name}-aurora-postgres-${replace(var.engine_version, ".", "-")}-cluster-parameter-group"

  parameter {
    apply_method = "pending-reboot"
    name         = "rds.logical_replication"
    value        = 1
  }
}

resource "aws_security_group_rule" "aurora-worker" {
  count = var.enable_psql ? length(var.access_sg_ids) : 0

  description              = "aurora traffic from aurora db to workers"
  type                     = "ingress"
  from_port                = module.aurora_postgres[0].rds_cluster_port
  to_port                  = module.aurora_postgres[0].rds_cluster_port
  protocol                 = "tcp"
  security_group_id        = module.aurora_postgres[0].security_group_id
  source_security_group_id = var.access_sg_ids[count.index]
}