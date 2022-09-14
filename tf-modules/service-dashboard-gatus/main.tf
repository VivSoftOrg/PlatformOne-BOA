module "gatus" {
  source           = "USSBA/easy-fargate-service/aws"
  version          = "~> 9.1"
  family           = var.service_name
  task_policy_json = data.aws_iam_policy_document.fargate.json
  container_definitions = [
    {
      name         = "gatus" # Arbitrary name for the container
      image        = var.repository_gatus
      portMappings = [{ containerPort = 8080 }]
      dependsOn = [{
        condition     = "HEALTHY"
        containerName = "s3sync"
      }]
    },
    {
      name  = "s3sync"
      image = var.repository_awscli
      entrypoint = ["bash", "-cx", <<-EOT
         while true; do
           aws s3 sync "$SOURCE_LOCATION" "$DEST_LOCATION";
           sleep $SYNC_PERIOD;
         done
       EOT
      ]
      healthCheck = {
        command     = ["CMD-SHELL", "ls /config/config.yaml || exit 1"]
        interval    = 10
        retries     = 3
        startPeriod = 5
        timeout     = 2
      }
      environment = [
        { name = "SOURCE_LOCATION", value = "s3://${var.config_bucket_name}" },
        { name = "DEST_LOCATION", value = "/config" },
        { name = "SYNC_PERIOD", value = "30" },
      ]
    }
  ]
  nonpersistent_volume_configs = [
    {
      container_name = "gatus"
      volume_name    = "config"
      container_path = "/config"
    },
    {
      container_name = "s3sync"
      volume_name    = "config"
      container_path = "/config"
    },
  ]

  container_port = 8080

  cluster_name = var.cluster_name

  iam_role_path                 = var.iam_role_path
  iam_role_permissions_boundary = var.iam_role_permissions_boundary

  vpc_id             = var.vpc_id
  private_subnet_ids = var.private_subnet_ids
  public_subnet_ids  = var.public_subnet_ids
  certificate_arns   = concat(var.certificate_arns, try([data.aws_acm_certificate.acm_certificate[0].arn], []))

  alb_security_group_ids = [aws_security_group.alb_sg.id]
}

resource "aws_route53_record" "dns" {
  count   = var.hosted_zone_dns != "" && var.service_fqdn != "" ? 1 : 0
  zone_id = data.aws_route53_zone.cms_zone.id
  name    = var.service_fqdn
  type    = "CNAME"
  alias {
    name                   = module.gatus.alb_dns
    zone_id                = module.gatus.alb.zone_id
    evaluate_target_health = false
  }
  allow_overwrite = true
}

resource "aws_security_group" "alb_sg" {
  name_prefix = var.service_name
  description = "Access to gatus in fargate"
  vpc_id      = var.vpc_id

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

resource "aws_security_group_rule" "ingress_cidrs_80" {
  count             = length(var.ingress_cidrs) > 0 ? 1 : 0
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = var.ingress_cidrs
  security_group_id = aws_security_group.alb_sg.id
}
resource "aws_security_group_rule" "ingress_cidrs" {
  count             = length(var.ingress_cidrs) > 0 ? 1 : 0
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = var.ingress_cidrs
  security_group_id = aws_security_group.alb_sg.id
}
resource "aws_security_group_rule" "ingress_prefix_list_80" {
  count             = length(var.ingress_prefix_lists) > 0 ? 1 : 0
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  prefix_list_ids   = var.ingress_prefix_lists
  security_group_id = aws_security_group.alb_sg.id
}
resource "aws_security_group_rule" "ingress_prefix_list" {
  count             = length(var.ingress_prefix_lists) > 0 ? 1 : 0
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  prefix_list_ids   = var.ingress_prefix_lists
  security_group_id = aws_security_group.alb_sg.id
}

data "aws_iam_policy_document" "fargate" {
  statement {
    actions = [
      "s3:List*",
      "s3:GetObject",
    ]
    resources = [
      "arn:aws:s3:::${var.config_bucket_name}/*",
    ]
  }
  statement {
    actions = [
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::${var.config_bucket_name}",
    ]
  }
}

data "aws_acm_certificate" "acm_certificate" {
  count       = var.acm_cert_base_domain != "" ? 1 : 0
  domain      = var.acm_cert_base_domain
  types       = ["AMAZON_ISSUED"]
  most_recent = true
}
data "aws_route53_zone" "cms_zone" {
  name         = var.hosted_zone_dns
  private_zone = true
}
