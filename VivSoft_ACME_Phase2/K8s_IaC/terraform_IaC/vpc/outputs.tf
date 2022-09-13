## VPC Data

output "vpc" {
  value = data.aws_vpc.vpc.cidr_block_associations.*.cidr_block
}

output "vpc_id" {
  description = "The ID of the VPC"
  value       = data.aws_vpc.vpc.id
}

output "vpc_arn" {
  description = "The ARN of the VPC"
  value       = data.aws_vpc.vpc.arn
}


output "private_subnets" {
  description = "List of IDs of private subnets"
  value       = data.aws_subnet_ids.private.ids
}

output "public_subnets" {
  description = "List of IDs of public subnets"
  value       = data.aws_subnet_ids.public.ids
}

output "container_subnets" {
  description = "List of IDs of container subnets"
  value       = data.aws_subnet_ids.container.ids
}

output "transport_subnets" {
  description = "List of IDs of transport subnets"
  value       = try(data.aws_subnet_ids.transport[0].ids, [])
}
output "transport_subnet_cidr_blocks" {
  description = "map of IDs to transport subnet cidrs"
  value       = { for subnet in data.aws_subnet.transport : subnet.id => subnet.cidr_block }
}
