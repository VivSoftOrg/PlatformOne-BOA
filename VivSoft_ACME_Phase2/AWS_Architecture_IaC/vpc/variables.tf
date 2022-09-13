variable "environment" {}

variable "creater" {
  default = "platform-bootstrap-vdms"
}

variable "owner" {
  default = "viv_softcloud"
}

variable "project" {
  default = "viv_softPlatform"
}

variable "client_code" {
  default = "viv_soft"
}

variable "account_code" {
  default = ""
}

variable "build_url" {
  default = "Unknown"
}

# Base AMI to use for hardened RHEL7 instances
variable "baseos_rhel7_ami_id" {}

# Instead of using remote state, we allow variables so we can be deployed standalone.
variable "platform_keypair" {
  default = ""
}

variable "backend_bucket" {
  default = ""
}

# Flexible AZ / subnets and CIDR layout.
variable "vpc_cidr_block" {
  default = "10.64.0.0/16"
}

variable "az_count" {
  default = 2
}

variable "az_cidr_length" {
  default = 1
}

variable "az_cidr_newbits" {
  default = 0
}

variable "subnet_cidr_length" {
  default = 1
}

variable "subnet_cidr_newbits" {
  default = 4
}

variable "required_storage_subnet" {
  default = 0
}

variable "required_packer_subnet" {
  default = 0
}

# Enable/disable various features.
variable "dhcp_options" {
  default = false
}

variable "dns_support" {
  default = true
}

variable "flow_log_traffic_type" {
  default = "ALL"
}

variable "external_cloudtrail" {
  default = 1
}

variable "external_nacl" {
  default = 0
}

variable "required_igw" {
  default = 1
}

variable "required_transit_vgw" {
  default = 0
}

variable "transit_vgw" {
  default = ""
}

# DHCP options.
variable "dhcp_dns_servers" {
  default = ""
}

variable "dhcp_ntp_servers" {
  default = ""
}

# Remote access
variable "ssh_remote_cidr_block" {
  default = ""
}

variable "https_remote_cidr_block" {
  default = ""
}

variable "rdp_remote_cidr_block" {
  default = ""
}

variable "winrm_remote_cidr_block" {
  default = ""
}

variable "vpn_remote_cidr_block" {
  default = ""
}

# Optional NAT feature.
variable "nat_type" {
  default = "instance"
} # Change to "none" or "" to disable the NAT, change to "gateway" to use the NAT gateway.

variable "nat_instance_type" {
  default = "t3.micro"
}

# Optional Bastion feature.
variable "bastion_instance" {
  default = 1
} # Change to 0 to disable the bastion.

variable "bastion_use_public_ip" {
  default = 1
} # Change to 0 to disable using an EIP for the bastion.

variable "bastion_instance_type" {
  default = "t3.micro"
}

variable "expiration_date" {
  default = ""
}

variable "prefix" {}

variable "tfstate_prefixes" {
  type = "map"
  default = {
  }
}

variable "default_tfstate_prefix" {
  default = ""
}

variable "instance_schedule" {}

variable "enable_ssm" {
  default = false
}

variable "install_ssm_agent" {
  default = false
}