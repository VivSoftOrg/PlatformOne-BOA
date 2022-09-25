variable "subnet_id" {
  type = string
}

variable "aws_region" {
  type = string
  default = "us-east-1"
}

variable "ssh_user" {
  type = string
  default = "ec2-user"
}


variable "hardening" {
  type = string
  description = "Type of hardening to apply to the built image, currently on supports stig or none"
  default = "stig"
}

variable "http_proxy" {
  type = string
  default = ""
}

variable "https_proxy" {
  type = string
  default = ""
}

variable "no_proxy" {
  type = string
  default = ""
}

data "amazon-ami" "rhel8" {
  filters = {
    name                = "RHEL-8.3*"
    virtualization-type = "hvm"
    root-device-type    = "ebs"
  }
  owners      = ["var.base_ami_owner"]
  region      = var.aws_region
  most_recent = true
}

source "amazon-ebs" "generic-rhel8" {
  ami_name = "rhel8-{{timestamp}}"
  source_ami = data.amazon-ami.rhel8.id

  region = var.aws_region

  subnet_id = var.subnet_id
  instance_type = "t3a.medium"
  ena_support = true
  ami_virtualization_type = "hvm"

  ssh_username = var.ssh_user

  launch_block_device_mappings {
    device_name = "/dev/sda1"
    volume_size = 20
    volume_type = "gp2"
    delete_on_termination = true
  }
  launch_block_device_mappings {
    device_name = "/dev/sde"
    volume_size = 20
    volume_type = "gp2"
    delete_on_termination = true
  }

  ami_block_device_mappings {
    device_name = "/dev/sda1"
    volume_size = 20
    volume_type = "gp2"
    delete_on_termination = true
  }
  ami_block_device_mappings {
    device_name = "/dev/sde"
    volume_size = 20
    volume_type = "gp2"
    delete_on_termination = true
  }

  tags = {
    "OS" = "rhel8"
    "BuildDate" = "{{ isotime }}"
  }

  run_tags = {
    "Name" = "rhel8-packer-builder-{{ timestamp }}"
  }
}

build {
  sources = [
    "source.amazon-ebs.generic-rhel8-rke2"
  ]

  provisioner "shell" {
    inline = ["while [ ! -f /var/lib/cloud/instance/boot-finished ]; do echo 'Waiting for cloud-init...'; sleep 5; done"]
  }

  provisioner "shell" {
    inline = ["sudo lsblk"]
  }

  provisioner "shell" {
    execute_command = "echo 'ec2-user' | {{.Vars}} sudo -S -E bash '{{.Path}}'"
    script = "scripts/partition.sh"

    # partitioning reboots
    expect_disconnect = "true"
    start_retry_timeout = "15m"
  }

  provisioner "shell" {
    inline = ["sudo lsblk"]
  }

  provisioner "ansible" {
    playbook_file = "ansible/roles/rhel8-stig/ami.yml"
    user = var.ssh_user
    ansible_env_vars = [
      "ANSIBLE_REMOTE_TEMP='/tmp/.ansible/'",
    ]
    extra_arguments = [
      "-vv",
      "--extra-vars",
      "ansible_python_interpreter=/usr/libexec/platform-python aws_region=${var.aws_region} hardening=${var.hardening} cis_15_enabled=${var.cis_15_enabled}"
    ]
  }

}

