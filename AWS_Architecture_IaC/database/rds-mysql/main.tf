
##########################################################################
# Mysql                                                            ##
# This is 5.7.12 version of Mysql  ##
##########################################################################

module "aurora_mysql" {
  count = var.enable_mysql ? 1 : 0

  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "2.29.0"

  name = "${var.name}-mysql"

  engine         = "aurora-mysql"
  engine_version = "5.7.12"

  vpc_id  = var.vpc_id
  subnets = var.private_subnet_ids

  username      = var.mysql_username
  password      = var.mysql_password
  database_name = var.mysql_db_name

  replica_count       = var.mysql_replica_count
  instance_type       = var.mysql_instance_type
  storage_encrypted   = true
  apply_immediately   = true
  skip_final_snapshot = true
  ca_cert_identifier  = "rds-ca-2017"

  allowed_security_groups = aws_security_group.aurora-rds-mysql.*.id

  deletion_protection             = var.rds_deletion_protection
  db_parameter_group_name         = aws_db_parameter_group.aurora_db_aurora_mysql57_parameter_group[count.index].id
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.aurora_cluster_aurora_mysql57_parameter_group[count.index].id

  tags = merge(
    {
      application       = var.application
      terraform_managed = "true"
      component         = "database"
    },
    var.cluster_tags,
  )
}

# security group 
resource "aws_security_group" "aurora-rds-mysql" {
  count = var.enable_mysql ? 1 : 0

  name        = "${var.name}-mysql"
  description = "${var.name} p1-k8s mysql rds"
  vpc_id      = var.vpc_id
}

# Security group rule
resource "aws_security_group_rule" "aurora-worker-mysql" {
  count = var.enable_mysql ? length(var.access_sg_ids) : 0

  type                     = "ingress"
  description              = "aurora traffic from aurora mysql db to workers"
  from_port                = module.aurora_mysql[0].this_rds_cluster_port
  to_port                  = module.aurora_mysql[0].this_rds_cluster_port
  protocol                 = "tcp"
  security_group_id        = module.aurora_mysql[0].this_security_group_id
  source_security_group_id = var.access_sg_ids[count.index]
}


# DB Parameter group resource
resource "aws_db_parameter_group" "aurora_db_aurora_mysql57_parameter_group" {
  count = var.enable_mysql ? 1 : 0

  name        = "${var.name}-mysql-parameter-group"
  family      = "aurora-mysql5.7"
  description = "${var.name}-mysql57-parameter-group"

  parameter {
    name  = "max_allowed_packet"
    value = "1073741824"
  }
  parameter {
    name  = "sql_mode"
    value = "TRADITIONAL"
  }
}

# RDS cluster Parameter group
resource "aws_rds_cluster_parameter_group" "aurora_cluster_aurora_mysql57_parameter_group" {
  count = var.enable_mysql ? 1 : 0

  name        = "${var.name}-mysql57-cluster-parameter-group"
  family      = "aurora-mysql5.7"
  description = "${var.name}-mysql57-cluster-parameter-group"
  parameter {
    name  = "max_allowed_packet"
    value = "1073741824"
  }
  parameter {
    apply_method = "pending-reboot"
    name         = "binlog_format"
    value        = "ROW"
  }
  parameter {
    apply_method = "pending-reboot"
    name         = "binlog_format"
    value        = "ROW"
  }
  parameter {
    name  = "log_bin_trust_function_creators"
    value = "1"
  }
}
