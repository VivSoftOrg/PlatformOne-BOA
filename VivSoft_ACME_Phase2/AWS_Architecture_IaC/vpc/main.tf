provider "aws" {
  version = "~> 2.25.0"
}

data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}
data "aws_region" "current" {}
data "aws_availability_zones" "zones" {}

locals {
  platform_keypair = "${coalesce(var.platform_keypair, "${var.environment}-${var.project}-core")}"
  bastion_instance_count = "${var.environment == "prod" ? var.az_count : 1 }"
  bastion_asg_min_count = "${var.environment == "prod" ? 1 : 0 }"
  platform_bucket  = "${coalesce(var.backend_bucket, "${lower(var.client_code)}-${lower(var.environment)}-${lower(var.project)}")}"
}

data "terraform_remote_state" "iam" {
  backend = "s3"

  config {
    bucket                 = "${local.platform_bucket}"
    key                    = "tfstate/${var.account_code}${lookup(var.tfstate_prefixes, "core-iam", var.default_tfstate_prefix)}/core-iam"
    skip_region_validation = true
  }
}

resource "aws_vpc" "vpc" {
  cidr_block         = "${var.vpc_cidr_block}"
  enable_dns_support = "${var.dns_support}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-vpc"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Project        = "${var.project}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

# Egress to the VPC only.
resource "aws_security_group" "vpc-egress" {
  name        = "${var.prefix}-vpc-egress"
  description = "Egress to same VPC"
  vpc_id      = "${aws_vpc.vpc.id}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-vpc-egress"
    Environment    = "${var.environment}"
    Project        = "${var.project}"
    Product        = "VDMS"
    Owner          = "${var.owner}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_security_group_rule" "vpc-egress-rule" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = "${aws_security_group.vpc-egress.id}"
  cidr_blocks       = ["${var.vpc_cidr_block}"]
  description       = "Allow egress to VPC only"
}

# Egress to anywhere
resource "aws_security_group" "all-egress" {
  name        = "${var.prefix}-all-egress"
  description = "Egress to anywhere"
  vpc_id      = "${aws_vpc.vpc.id}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-all-egress"
    Environment    = "${var.environment}"
    Project        = "${var.project}"
    Product        = "VDMS"
    Owner          = "${var.owner}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_security_group_rule" "all-egress-rule" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = "${aws_security_group.all-egress.id}"
  cidr_blocks       = ["0.0.0.0/0"]
  description       = "Allow egress to anywhere"
}

resource "aws_vpc_endpoint" "s3e" {
  lifecycle {
    ignore_changes = [
      "vpc_endpoint_type",
    ]
  }

  vpc_id          = "${aws_vpc.vpc.id}"
  route_table_ids = ["${aws_route_table.priv.*.id}", "${aws_route_table.pub.id}"]
  service_name    = "com.amazonaws.${data.aws_region.current.name}.s3"
}

resource "aws_subnet" "pub" {
  count             = "${var.az_count}"
  availability_zone = "${element(data.aws_availability_zones.zones.names, count.index)}"
  vpc_id            = "${aws_vpc.vpc.id}"
  cidr_block        = "${cidrsubnet(cidrsubnet(var.vpc_cidr_block, var.az_cidr_newbits, var.az_cidr_length * count.index), var.subnet_cidr_newbits, 0)}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-pub-${element(data.aws_availability_zones.zones.names, count.index)}"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Project        = "${var.project}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_subnet" "priv" {
  count             = "${var.az_count}"
  availability_zone = "${element(data.aws_availability_zones.zones.names, count.index)}"
  vpc_id            = "${aws_vpc.vpc.id}"
  cidr_block        = "${cidrsubnet(cidrsubnet(var.vpc_cidr_block, var.az_cidr_newbits, var.az_cidr_length * count.index), var.subnet_cidr_newbits, var.subnet_cidr_length * 1)}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-priv-${element(data.aws_availability_zones.zones.names, count.index)}"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Project        = "${var.project}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_subnet" "mgmt" {
  count             = "${var.az_count}"
  availability_zone = "${element(data.aws_availability_zones.zones.names, count.index)}"
  vpc_id            = "${aws_vpc.vpc.id}"
  cidr_block        = "${cidrsubnet(cidrsubnet(var.vpc_cidr_block, var.az_cidr_newbits, var.az_cidr_length * count.index), var.subnet_cidr_newbits, var.subnet_cidr_length * 2)}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-MGMT-${element(data.aws_availability_zones.zones.names, count.index)}"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Project        = "${var.project}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_subnet" "storage" {
  count             = "${var.required_storage_subnet>0 ? var.az_count : 0}"
  availability_zone = "${element(data.aws_availability_zones.zones.names, count.index)}"
  vpc_id            = "${aws_vpc.vpc.id}"
  cidr_block        = "${cidrsubnet(cidrsubnet(cidrsubnet(var.vpc_cidr_block, var.az_cidr_newbits, var.az_cidr_length * count.index), var.subnet_cidr_newbits, var.subnet_cidr_length * 7),5, 30)}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-storage-${element(data.aws_availability_zones.zones.names, count.index)}"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Project        = "${var.project}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

# FYI: Throw the packer subnet all the way at the end of the VPC cidr block.
resource "aws_subnet" "packer" {
  count             = "${var.required_packer_subnet>0 ? var.az_count : 0}"
  availability_zone = "${element(data.aws_availability_zones.zones.names, count.index)}"
  vpc_id            = "${aws_vpc.vpc.id}"
  cidr_block        = "${cidrsubnet(cidrsubnet(cidrsubnet(var.vpc_cidr_block, var.az_cidr_newbits, var.az_cidr_length * count.index), var.subnet_cidr_newbits, var.subnet_cidr_length * 7),6, 63)}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-packer-${element(data.aws_availability_zones.zones.names, count.index)}"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Project        = "${var.project}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_route_table" "pub" {
  vpc_id = "${aws_vpc.vpc.id}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-pub"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Project        = "${var.project}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_route_table" "priv" {
  count  = "${var.az_count}"
  vpc_id = "${aws_vpc.vpc.id}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-priv"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Project        = "${var.project}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_route_table_association" "pub" {
  count          = "${var.az_count}"
  route_table_id = "${aws_route_table.pub.id}"
  subnet_id      = "${element(aws_subnet.pub.*.id, count.index)}"
}

resource "aws_route_table_association" "priv" {
  count          = "${var.az_count}"
  route_table_id = "${element(aws_route_table.priv.*.id, count.index)}"
  subnet_id      = "${element(aws_subnet.priv.*.id, count.index)}"
}

resource "aws_route_table_association" "mgmt" {
  count          = "${var.az_count}"
  route_table_id = "${element(aws_route_table.priv.*.id, count.index)}"
  subnet_id      = "${element(aws_subnet.mgmt.*.id, count.index)}"
}

resource "aws_route_table_association" "storage" {
  count          = "${var.required_storage_subnet>0 ? var.az_count : 0}"
  route_table_id = "${element(aws_route_table.priv.*.id, count.index)}"
  subnet_id      = "${element(aws_subnet.storage.*.id, count.index)}"
}

resource "aws_route_table_association" "packer" {
  count          = "${var.required_packer_subnet>0 ? var.az_count : 0}"
  route_table_id = "${element(aws_route_table.priv.*.id, count.index)}"
  subnet_id      = "${element(aws_subnet.packer.*.id, count.index)}"
}

resource "aws_vpn_gateway_attachment" "vpn_attachment" {
  count          = "${var.required_transit_vgw ? 1 : 0}"
  vpc_id         = "${aws_vpc.vpc.id}"
  vpn_gateway_id = "${var.transit_vgw}"
}

resource "aws_vpn_gateway_route_propagation" "vgw_route_pub" {
  count          = "${var.required_transit_vgw ? 1 : 0}"
  depends_on     = ["aws_vpn_gateway_attachment.vpn_attachment"]
  vpn_gateway_id = "${var.transit_vgw}"
  route_table_id = "${aws_route_table.pub.id}"
}

resource "aws_vpn_gateway_route_propagation" "vgw_route_priv" {
  count          = "${var.required_transit_vgw ? var.az_count : 0}"
  depends_on     = ["aws_vpn_gateway_attachment.vpn_attachment"]
  vpn_gateway_id = "${var.transit_vgw}"
  route_table_id = "${element(aws_route_table.priv.*.id, count.index)}"
}
