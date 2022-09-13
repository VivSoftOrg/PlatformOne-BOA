variable "project" {
  default = "batcave"
}

variable "environment" {
  default = "dev"
}

variable "service_name" {
  default     = "batcave-status"
  type        = string
  description = "Name of the serverless service"
}

variable "vpc_id" {}

variable "private_subnets" {
  type        = list(any)
  description = "List of subnet ids where the lambda will execute"
}
variable "frontend_subnets" {
  type        = list(any)
  description = "List of subnet ids to house the front-end of this lambda (such as Shared subnet or Transport subnet)"
}

variable "base_domain" {
  type        = string
  description = "The base domain of the services the lambda should be requesting to.  eg: 'batcave.internal.cms.gov'"
}

variable "create_custom_domain" {
  type        = bool
  default     = false
  description = "Optionally create a custom domain for this serverless service"
}
variable "iam_role_path" {
  default = "/delegatedadmin/developer/"
}

variable "iam_role_permissions_boundary" {
  default = ""
}

variable "route53_zone_type" {
  default     = "private"
  type        = string
  description = "Optionally create DNS records, and lookup either 'private' or 'public' r53 zone"
}

variable "custom_subdomain" {
  default     = "status"
  type        = string
  description = "Subdomain for the optionally created dns records"
}

variable "tg_prefix" {
  type        = string
  default     = "lambda"
  description = "Name prefix for target groups created; must be < 6 characters"
}


variable "lambda_path" {
  description = "Path to the lambda code"
  default     = "lambda"
}

variable "lambda_runtime" {
  description = "The runtime environment to use for this lambda (e.g. 'python3.9' or 'nodejs16.x')"
  default     = "nodejs16.x"
  type        = string
}

variable "lambda_handler" {
  description = "The entry point of the lambda (i.e. the fully qualified name of the function to be invoked: file-or-module-name.function-name)"
  type        = string
}

variable "lambda_environment" {
  description = "Environment variables used by the lambda function."
  type        = map(string)
  default     = null
}

variable "lambda_timeout" {
  description = "The number of seconds the lambda will be allowed to execute before timing out"
  type        = number
  # AWS Default for newly created Lambdas
  default     = 3
}

variable "ingress_prefix_lists" {
  description = "List of prefix lists to attach to ALB Security Group"
  default     = []
  type        = list(any)
}

variable "ingress_cidrs" {
  description = "List of CIDR Blocks to attach to ALB Security Group"
  default     = ["10.0.0.0/8"]
  type        = list(any)
}

variable "alb_access_logs" {
  description = "Map of aws_lb access_log config"
  default     = {}
}

variable "ingress_sgs" {
  description = "A list of security groups in which https ingress rules will be created"
  type        = list(string)
  default     = []
}
