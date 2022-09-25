variable "env" {
  default = "dev"
}

variable "project" {
  default = "batcave"
}

variable "transport_subnets_exist" {
  description = "Transport subnets are used to house the NLB in situations where a service is required to be exposed to VDI users"
  default     = false
  type        = bool
}

variable "shared_subnets_exist" {
  description = "Shared subnets are used to house resources intended to be shared across ALL CMS Cloud systems via the transit gateway"
  default     = false
  type        = bool
}

variable "shared_subnets_additional_tgw_routes" {
  description = "These CIDR blocks will be added to the shared subnet route tables and routed to the transit gateway"
  default     = []
  type        = list(any)
}

variable "public_pl_exists" {
  description = "The public PL is a work in progress (as of 2022-05-27) by the network team.  It will eventually be rolled out everywhere, but is not yet.  For now, it defaults to false, but can eventually be removed when every ADO VPC has it"
  default     = false
  type        = bool
}

variable "zscaler_pl_exists" {
  description = "The zscaler PL is a work in progress (as of 2022-07-08) by the network team.  It will eventually be rolled out everywhere, but is not yet.  For now, it defaults to false, but can eventually be removed when every ADO VPC has it"
  default     = false
  type        = bool
}
