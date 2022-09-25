# Creates a pair of Load Balancers to make the service publicly accessible


variable "transport_subnet_cidr_blocks" {
  description = "Map of transport subnets to cidrs for creating the NLB"
  type        = map(any)
}
variable "transport_subnet_ip_index" {
  default     = 6
  description = "The X'th IP within each transport subnet cidr block to assign to the NLB"
}

# This NLB is the front-end of the service.
# It lives in the transport subnet to be accessible by
# services outside of CMSCloud
module "nlb" {
  depends_on = [
    module.alb
  ]
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 6.0"

  name = "${var.service_name}-nlb"

  load_balancer_type = "network"
  internal           = true

  vpc_id = var.vpc_id
  #subnets = var.private_subnets
  subnet_mapping = [for k, v in var.transport_subnet_cidr_blocks : { subnet_id = k, private_ipv4_address = cidrhost(v, var.transport_subnet_ip_index) }]

  #access_logs = {
  #  bucket = "my-nlb-logs"
  #}

  target_groups = [
    {
      #name_prefix      = "${var.service_name}-80-"
      backend_protocol = "TCP"
      backend_port     = 80
      target_type      = "alb"
      vpc_id           = var.vpc_id
      targets = [
        {
          target_id = module.alb.lb_arn
        },
      ]
    },
    {
      #name_prefix      = "${var.service_name}-443-"
      backend_protocol = "TCP"
      backend_port     = 443
      target_type      = "alb"
      vpc_id           = var.vpc_id
      targets = [
        {
          target_id = module.alb.lb_arn
        },
      ]
    },
  ]

  #https_listeners = [
  #]

  http_tcp_listeners = [
    {
      port               = 80
      protocol           = "TCP"
      target_group_index = 0
    },
    {
      port     = 443
      protocol = "TCP"
      #certificate_arn    = var.create_custom_domain ? data.aws_acm_certificate.acm_certificate[0].arn : null
      target_group_index = 1
    }
  ]

  #tags = {
  #  Environment = "Test"
  #}
}


# This ALB routes requests to the lambda that executes inside the VPC
module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 6.0"

  name = "${var.service_name}-alb"

  load_balancer_type = "application"

  vpc_id          = var.vpc_id
  internal        = true
  subnets         = var.private_subnets
  security_groups = [aws_security_group.lambda.id]

  drop_invalid_header_fields = true

  #access_logs = {
  #  bucket = "my-alb-logs"
  #}

  target_groups = [
    {
      target_type = "lambda"
      ## Can't use targets because the module doesn't have a mechanism for adding ALB permissions to the Lambda function
      #targets = [
      #  {
      #    target_id = module.lambda.lambda_function_arn
      #  },
      #]
    }
  ]

  https_listeners = [
    {
      port               = 443
      protocol           = "HTTPS"
      certificate_arn    = var.create_custom_domain ? data.aws_acm_certificate.acm_certificate[0].arn : null
      target_group_index = 0
    }
  ]

  http_tcp_listeners = [
    {
      port        = 80
      protocol    = "HTTP"
      action_type = "redirect"
      redirect = {
        port        = "443"
        protocol    = "HTTPS"
        status_code = "HTTP_301"
      }
    }
  ]
}
