# optional support the IGW for the VDMS vpc if required 
resource "aws_internet_gateway" "igw" {
  count  = "${var.required_igw || var.nat_type=="instance" || var.nat_type=="gateway" ? 1 : 0}"
  vpc_id = "${aws_vpc.vpc.id}"

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-igw"
    Environment    = "${var.environment}"
    Owner          = "${var.owner}"
    Project        = "${var.project}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

# optional suport for IGW route to public subnet
resource "aws_route" "igw_route" {
  count                  = "${var.required_igw ? 1 : 0}"
  route_table_id         = "${aws_route_table.pub.id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.igw.id}"
}
