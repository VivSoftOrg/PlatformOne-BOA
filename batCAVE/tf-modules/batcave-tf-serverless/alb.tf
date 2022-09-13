module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 6.0"

  name = "${var.service_name}-alb"

  vpc_id                     = var.vpc_id
  subnets                    = var.frontend_subnets
  load_balancer_type         = "application"
  internal                   = true
  security_groups            = [aws_security_group.lambda.id]
  drop_invalid_header_fields = true
  access_logs                = var.alb_access_logs

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
