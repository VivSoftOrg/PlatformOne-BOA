resource "aws_vpc_dhcp_options" "dhcp" {
  count               = "${var.dhcp_options ? 1 : 0}"
  domain_name_servers = ["${split(",", var.dhcp_dns_servers)}"]
  ntp_servers         = ["${split(",", var.dhcp_ntp_servers)}"]

  tags {
    CreatedBy      = "${var.creater}"
    Name           = "${var.prefix}-dhcp"
    Environment    = "${var.environment}"
    Project        = "${var.project}"
    Product        = "VDMS"
    Owner          = "${var.owner}"
    BuildUrl       = "${var.build_url}"
    ExpirationDate = "${var.expiration_date}"
  }
}

resource "aws_vpc_dhcp_options_association" "dhcp" {
  count           = "${var.dhcp_options ? 1 : 0}"
  vpc_id          = "${aws_vpc.vpc.id}"
  dhcp_options_id = "${aws_vpc_dhcp_options.dhcp.id}"
}
