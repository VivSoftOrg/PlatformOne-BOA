# vpc id
data "aws_vpc" "batcave_vpc" {
  tags = {
    Name = "${var.project}-*-${var.env}"
  }
}

# private subnets
data "aws_subnets" "private" {
  filter {
    name = "tag:Name"
    values = [
      "${var.project}-*-${var.env}-private-*"
    ]
  }
}

# public subnets
data "aws_subnets" "public" {
  filter {
    name = "tag:Name"
    values = [
      "${var.project}-*-${var.env}-public-*"
    ]
  }
}

# container subnets
data "aws_subnets" "container" {
  filter {
    name = "tag:Name"
    values = [
      "${var.project}-*-${var.env}-unroutable-*"
    ]
  }
}

# transport subnets
data "aws_subnets" "transport" {
  count = var.transport_subnets_exist ? 1 : 0
  filter {
    name = "tag:Name"
    values = [
      "${var.project}-*-${var.env}-transport-*"
    ]
  }
}

# shared subnets
data "aws_subnets" "shared" {
  count = var.shared_subnets_exist ? 1 : 0
  filter {
    name = "tag:Name"
    values = [
      "${var.project}-*-${var.env}-shared-*"
    ]
  }
}

## subnet resources
data "aws_subnet" "private" {
  for_each = toset(data.aws_subnets.private.ids)
  id       = each.value
}

data "aws_subnet" "public" {
  for_each = toset(data.aws_subnets.public.ids)
  id       = each.value
}

data "aws_subnet" "container" {
  for_each = toset(data.aws_subnets.container.ids)
  id       = each.value
}

data "aws_subnet" "transport" {
  for_each = var.transport_subnets_exist ? toset(data.aws_subnets.transport[0].ids) : toset([])
  id       = each.value
}

data "aws_subnet" "shared" {
  for_each = var.shared_subnets_exist ? toset(data.aws_subnets.shared[0].ids) : toset([])
  id       = each.value
}

data "aws_ec2_managed_prefix_list" "vpn_prefix_list" {
  name = "cmscloud-vpn"
}

data "aws_ec2_managed_prefix_list" "cmscloud_shared_services_pl" {
  name = "cmscloud-shared-services"
}

data "aws_ec2_managed_prefix_list" "cmscloud_security_tools" {
  name = "cmscloud-security-tools"
}

data "aws_ec2_managed_prefix_list" "cmscloud_public_pl" {
  count = var.public_pl_exists ? 1 : 0
  name  = "cmscloud-public"
}

data "aws_ec2_managed_prefix_list" "zscaler_pl" {
  count = var.zscaler_pl_exists ? 1 : 0
  name  = "zscaler"
}

data "aws_route_table" "shared" {
  for_each  = toset(try(data.aws_subnets.shared[0].ids, []))
  subnet_id = each.key
}

data "aws_ec2_transit_gateway" "shared_services" {
  filter {
    name   = "owner-id"
    values = ["921617238787"]
  }
}

locals {
  # shared subnet route table ids
  shared_subnet_route_tables = [for rt in data.aws_route_table.shared : rt.route_table_id]
  # Map of routes and CIDRs
  shared_subnet_additional_routes = { for each in setproduct(local.shared_subnet_route_tables, var.shared_subnets_additional_tgw_routes)
    : "${each[0]}_${each[1]}" =>
    { route_table_id = each[0], cidr = each[1] }
  }
}
resource "aws_route" "shared_subnet_additional_routes_to_tgw" {
  for_each = local.shared_subnet_additional_routes

  route_table_id         = each.value.route_table_id
  destination_cidr_block = each.value.cidr
  transit_gateway_id     = data.aws_ec2_transit_gateway.shared_services.id
}

locals {
  all_subnets = merge({
    "public"    = data.aws_subnet.public
    "private"   = data.aws_subnet.private
    "container" = data.aws_subnet.container
    },
    var.shared_subnets_exist ? { "shared" = data.aws_subnet.shared } : {},
    var.transport_subnets_exist ? { "transport" = data.aws_subnet.transport } : {},
  )
}

data "aws_eips" "nat_gateways" {
  tags = {
    Name = "${var.project}-*-${var.env}-nat-gateway-*"
  }
}
