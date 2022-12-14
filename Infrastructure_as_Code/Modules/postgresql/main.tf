
module "aurora" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "6.1.4"

  name           = var.name
  engine         = "aurora-postgresql"
  engine_version = "13.4"
  instances = {
    1 = {
      instance_class      = "db.r5.xlarge"
      publicly_accessible = var.publicly_accessible
    }
  }

  endpoints = {
    static = {
      identifier = "static-custom-endpt"
      type       = "ANY"
    }
  }

  vpc_id                  = var.vpc_id
  subnets                 = var.subnets
  create_db_subnet_group  = true
  create_security_group   = true
  allowed_security_groups = var.allowed_security_groups
  security_group_egress_rules = {
    to_cidrs = {
      cidr_blocks = ["0.0.0.0/0"]
      description = "Egress to Internet"
    }
  }

  iam_database_authentication_enabled = true
  master_username                     = var.master_username
  create_random_password              = true
  database_name                       = var.database_name

  apply_immediately   = true
  skip_final_snapshot = false

  db_parameter_group_name         = aws_db_parameter_group.db_parameter_group.id
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.db_cluster_parameter_group.id
  enabled_cloudwatch_logs_exports = ["postgresql"]

  tags = var.tags
}

resource "aws_db_parameter_group" "db_parameter_group" {
  name        = "${var.name}-aurora-db-postgres13-parameter-group"
  family      = "aurora-postgresql13"
  description = "${var.name}-aurora-db-postgres13-parameter-group"
  tags        = var.tags
}
resource "aws_rds_cluster_parameter_group" "db_cluster_parameter_group" {
  name        = "${var.name}-aurora-postgres13-cluster-parameter-group"
  family      = "aurora-postgresql13"
  description = "${var.name}-aurora-postgres13-cluster-parameter-group"
  tags        = var.tags
}

resource "aws_route53_record" "www" {
  zone_id = var.route53_zone_id
  name    = var.route53_record_name
  type    = "CNAME"
  ttl     = "60"
  records = ["${module.aurora.cluster_endpoint}"]
}


# postgres egress rule for cluster_security_group
resource "aws_security_group_rule" "db-egress-cluster_security_group" {
  type                     = "egress"
  description              = "postgres traffic"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
  source_security_group_id = module.aurora.security_group_id
  security_group_id        = var.cluster_security_group_id
}

# postgres egress rule for worker_security_group
resource "aws_security_group_rule" "db-egress-worker_security_group" {
  type                     = "egress"
  description              = "postgres traffic"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
  source_security_group_id = module.aurora.security_group_id
  security_group_id        = var.worker_security_group_id
}

# postgres egress rule for cluster_primary_security_group
resource "aws_security_group_rule" "db-egress-cluster_primary_security_group" {
  type                     = "egress"
  description              = "postgres traffic"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
  source_security_group_id = module.aurora.security_group_id
  security_group_id        = var.cluster_primary_security_group_id
}
