# vpc id
data "aws_vpc" "vpc" {
  tags = {
    Name = "${var.project}-*-${var.env}"
  }
}

# private subnets
data "aws_subnet_ids" "private" {
  vpc_id = data.aws_vpc.vpc.id
  filter {
    name = "tag:Name"
    values = [
      "${var.project}-*-${var.env}-private-*"
    ]
  }
}

# public subnets
data "aws_subnet_ids" "public" {
  vpc_id = data.aws_vpc.vpc.id
  filter {
    name = "tag:Name"
    values = [
      "${var.project}-*-${var.env}-public-*"
    ]
  }
}

# container subnets
data "aws_subnet_ids" "container" {
  vpc_id = data.aws_vpc.vpc.id
  filter {
    name = "tag:Name"
    values = [
      "${var.project}-*-${var.env}-unroutable-*"
    ]
  }
}

# transport subnets
data "aws_subnet_ids" "transport" {
  count  = var.transport_subnets_exist ? 1 : 0
  vpc_id = data.aws_vpc.vpc.id
  filter {
    name = "tag:Name"
    values = [
      "${var.project}-*-${var.env}-transport-*"
    ]
  }
}

## subnet resources
data "aws_subnet" "private" {
  for_each = data.aws_subnet_ids.private.ids
  id       = each.value
}

data "aws_subnet" "public" {
  for_each = data.aws_subnet_ids.public.ids
  id       = each.value
}

data "aws_subnet" "container" {
  for_each = data.aws_subnet_ids.container.ids
  id       = each.value
}

data "aws_subnet" "transport" {
  for_each = try(data.aws_subnet_ids.transport[0].ids, toset([]))
  id       = each.value
}
