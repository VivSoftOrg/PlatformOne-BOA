#!/bin/bash

function log { logger -i -t "configure-bastion" -s -- "$1" 2> /dev/console; }

# install & enable amazon ssm agent
if [ "${install_ssm_agent}" = "1" ]; then
  cd /tmp
  sudo yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm --nogpgcheck
  sudo systemctl enable amazon-ssm-agent
  sudo systemctl start amazon-ssm-agent
  log "Amazon SSM Agent installed successfully."
else
  log "Amazon SSM Agent is not installed as install_ssm_agent is set to false"
fi

exit 0