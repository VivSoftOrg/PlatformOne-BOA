module "lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 3.1"

  depends_on = [
    aws_security_group.lambda
  ]

  function_name = var.service_name
  handler       = var.lambda_handler
  runtime       = var.lambda_runtime

  recreate_missing_package = true
  source_path              = "${path.module}/${var.lambda_path}"

  vpc_subnet_ids         = var.private_subnets
  vpc_security_group_ids = [aws_security_group.lambda.id]
  attach_network_policy  = true

  role_path                 = var.iam_role_path
  policy_path               = var.iam_role_path
  role_permissions_boundary = var.iam_role_permissions_boundary
  timeout                   = var.lambda_timeout

  environment_variables = var.lambda_environment
}

# These resources attach the ALB to the Lambda
resource "aws_lambda_permission" "alb_to_lambda" {
  statement_id  = "AllowExecutionFromPublicALB"
  action        = "lambda:InvokeFunction"
  principal     = "elasticloadbalancing.amazonaws.com"
  function_name = module.lambda.lambda_function_arn
  source_arn    = module.alb.target_group_arns[0]
}

resource "aws_lb_target_group_attachment" "alb_to_lambda" {
  target_group_arn = module.alb.target_group_arns[0]
  target_id        = module.lambda.lambda_function_arn
  depends_on       = [aws_lambda_permission.alb_to_lambda]
}
