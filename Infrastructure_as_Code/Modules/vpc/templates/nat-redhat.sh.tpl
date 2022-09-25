#!/bin/bash
#
# nat.sh.tpl
#
# Borrowed most of the code from:
# * https://github.com/plus3it/cfn/blob/master/scripts/configure-nat-eni.sh
# * https://github.com/plus3it/cfn/blob/master/scripts/configure-pat.sh

function log { logger -i -t "configure-nat" -s -- "$1" 2> /dev/console; }

function die {
    [ -n "$1" ] && log "$1"
    log "Failed to attach ENI"'!'
    exit 1
}

# Sanitize PATH
PATH="/usr/sbin:/sbin:/usr/bin:/bin:/usr/local/bin"

# disabling the network configuration done by cloud-init on reboot
cat >/etc/cloud/cloud.cfg.d/30_network.cfg <<-EOF
network:
  config: disabled
EOF

RETRY_DELAY=1   # retry every <delay> seconds
TIMER_NIC_DISCOVERY=20  # wait this many seconds before failing
ENI_ID="${my_eni_id}"

INSTANCE_ID=$(curl --retry 3 --silent --fail http://169.254.169.254/latest/meta-data/instance-id) || \
    die "Could not get instance id."
log "Found instance id '$INSTANCE_ID'."

REGION=$(curl --retry 3 --silent --fail http://169.254.169.254/latest/dynamic/instance-identity/document | awk -F\" '/region/ {print $4}') || \
    die "Could not get region."
log "Found region '$REGION'."

export AWS_DEFAULT_REGION="$REGION"

log "Disabling source_dest_check for this instance..."
delay=5
timer=30
while true; do
    [[ $timer -le 0 ]] && die "Timer expired before source_dest_check disabled successfully."
    
    aws ec2 modify-instance-attribute --instance-id "$INSTANCE_ID" --no-source-dest-check && break
    log "Setting source_dest_check failed. Trying again in $delay second(s). Will timeout if not attached within $timer second(s)."
    sleep $delay
    timer=$(( timer-delay ))
done

log "Attaching ENI '$ENI_ID' to this instance..."
delay=15
timer=180
while true; do
    [[ $timer -le 0 ]] && die "Timer expired before ENI attached successfully."
    
    aws ec2 attach-network-interface --network-interface-id "$ENI_ID" \
        --instance-id "$INSTANCE_ID"  --device-index 1 && break  # break if ENI attached successfully
    log "ENI attachment failed. Trying again in $delay second(s). Will timeout if not attached within $timer second(s)."
    sleep $delay
    timer=$(( timer-delay ))
done

log "ENI '$ENI_ID' is attached to this instance."

ETH="eth1"
log "Waiting for '$ETH' network interface to be discovered by the system..."
delay=$RETRY_DELAY
timer=$TIMER_NIC_DISCOVERY
while true; do
    [[ $timer -le 0 ]] && die "Timer expired before network interface acquired MAC address."
    
    ETH_MAC=$(cat /sys/class/net/"$ETH"/address 2> /dev/null) && break  # break loop if MAC was found
    log "Not found yet. Trying again in $delay second(s). Will timeout if not reachable within $timer second(s)."
    sleep $delay
    timer=$(( timer-delay ))
done

log "Found $ETH MAC '$ETH_MAC'."

log "Configuring '$ETH' network interface and routes."
cat >/etc/sysconfig/network-scripts/ifcfg-"$ETH" <<-EOF
BOOTPROTO=dhcp
DEVICE=$ETH
HWADDR=$ETH_MAC
ONBOOT=yes
TYPE=Ethernet
USERCTL=no
DEFROUTE=yes
ZONE=external
EOF
cat >/etc/sysconfig/network-scripts/route-"$ETH" <<-EOF
169.254.169.254 dev $ETH table 10001
169.254.169.254 dev $ETH metric 10001
EOF
ifup $ETH

log "Waiting for '$ETH' network interface to get an IP address..."
delay=$RETRY_DELAY
timer=$TIMER_NIC_DISCOVERY
while true; do
    [[ $timer -le 0 ]] && die "Timer expired before network interface acquired IP address."
    
    # First try and acquire it from Linux.
    IP_ADDRESS=$(ip addr show dev "$ETH" 2> /dev/null | awk '/inet /{ sub(/\/.*$/,"",$2); print $2 }')
    [[ -n "$IP_ADDRESS" ]] && break  # break loop if IP was found
    
    log "Not found yet. Trying again in $delay second(s). Will timeout if not reachable within $timer second(s)."
    sleep $delay
    timer=$(( timer-delay ))
done

log "Got IP '$IP_ADDRESS' on $ETH."

log "ENI attachment successful"'!'

# On exit, always restore SELinux enforcement.
if [ "$(getenforce)" == "Enforcing" ]; then
    function cleanup() {
        setenforce 1
    }
    trap cleanup EXIT
    setenforce 0
fi

log "Ensuring eth0 is in the internal zone"
sed -e '/^ZONE/d' -i /etc/sysconfig/network-scripts/ifcfg-eth0
echo 'ZONE=internal' >>/etc/sysconfig/network-scripts/ifcfg-eth0
firewall-cmd --permanent --zone=internal --add-interface=eth0

# Get ETH from first parameter, or default to eth0
RETRY_DELAY=1   # retry every <delay> seconds
TIMER_NIC_DISCOVERY=20  # wait this many seconds before failing

VPC_CIDR_URI="http://169.254.169.254/latest/meta-data/network/interfaces/macs/$ETH_MAC/vpc-ipv4-cidr-block"
log "Metadata location for vpc ipv4 range: $VPC_CIDR_URI"

log "Attempting to get the vpc ipv4 range from metadata..."
delay=$RETRY_DELAY
timer=$TIMER_NIC_DISCOVERY
while true; do
    [[ $timer -le 0 ]] && die "Timer expired before retrieving VPC CIDR range from metadata."
    
    VPC_CIDR_RANGE=$(curl --retry 3 --silent --fail "$VPC_CIDR_URI") && break  # break loop if successful
    log "Not found yet. Trying again in $delay second(s). Will timeout if not reachable within $timer second(s)."
    sleep $delay
    timer=$(( timer-delay ))
done
log "Retrieved VPC CIDR range $VPC_CIDR_RANGE from meta-data."

log "Enabling IPv4 forwarding..."
for sf in $(grep -lr 'net\.ipv4\.ip_forward\s*=' /etc/sysctl.d); do
    sed -e '/^net\.ipv4\.ip_forward\s*=/d' -i "$sf"
    echo 'net.ipv4.ip_forward = 1' >>"$sf"
done
sysctl -w 'net.ipv4.ip_forward=1'

log "Enabling PAT..."
firewall-cmd --zone=internal --add-masquerade --permanent 
firewall-cmd --permanent --direct --add-rule ipv4 nat POSTROUTING 0 -o $ETH -s "$VPC_CIDR_RANGE" -j MASQUERADE
firewall-cmd --permanent --direct --add-rule ipv4 filter FORWARD 0 -i eth0 -o $ETH -j ACCEPT
firewall-cmd --permanent --direct --add-rule ipv4 filter FORWARD 0 -i $ETH -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
firewall-cmd --reload

sysctl net.ipv4.ip_forward net.ipv4.conf."$ETH".send_redirects | log
firewall-cmd --permanent --direct --get-all-rules | log

log "Ensuring default routes do not point to eth0"
sed -e '/^DEFROUTE/d' -i /etc/sysconfig/network-scripts/ifcfg-eth0
echo 'DEFROUTE=no' >>/etc/sysconfig/network-scripts/ifcfg-eth0
route del default eth0

log "Configuration of PAT complete."

# restart the network service to persist the changes
service network restart

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