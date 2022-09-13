# viv_soft-VPC
This Cookbook creates basic infrastructure with VPC, IGW, NAT, ROUTES, SUBNETS, ROUTES, and also captures log onto CloudWatch

## Terraform Script
```
backend
bastion
cloudtrial
dhcp
flow_log
IGW
main
nat
outputs
remote_access
variables
```
## input_variables

**Variables**                | **Description**
-----------------------------|-------------------------------------------------------------------
**baseos_rhel7_ami_id**      | base OS Image ID (AMI_ID)
**platform_keypair**         | platform key pair for accesss
**platform_bucket**          | S3 bucket for storing the tfstate files
**vpc_cidr_block**           | cidr block for VPC (EX: 10.0.0.0/16)
##### Enable/disable various features
**Variables**                | **Description**
-----------------------------|-------------------------------------------------------------------
**dhcp_options**             | DHCP feature false 
**dns_support**              | DNS True
**flow_log_traffic_type**    | All Flow log 
**external_cloudtrail**      | Set it to 0 to create the cloudtrail resources. Default: 1
**external_nacl**            | External network control access False
**required_igw**             | Require Internet gateway True
##### Remote access
ssh_remote, https_remote, rdp_remote, winrm_remote, vpn_remote
##### NAT and BASTION

**Variables**                | **Description**
-----------------------------|-------------------------------------------------------------------
**nat_type**                 | Change to "none" or "" to disable the NAT, change to "gateway" to use the NAT gateway.
**nat_instance_type**        | If using instnace mention instance type or Change it to "none"
**bastion_instance**         | Mention 1 to enable or 0 to disable
**bastion_use_public_ip**    | Mention 1 to enable public IP or 0 to disable
**bastion_instance_type**    | Assign type of instance used for bastion host

##### Backend
``` Configures S3 as a Backend and Terraform will use this backend unless the backend configuration changes 
```

##### Bastion
```hcl 
    Launches a Bastion instance with launch config to 
        1. allow VPN access with any resource associated with the VPC created in VDMS 
        2. allow SSH remote access with the resources associated with the VPC created in VDMS
            security_groups      = [
  	        "${aws_security_group.bastion.id}",
  	        "${aws_security_group.vpn-remote-access.*.id}",
  	        "${aws_security_group.ssh-remote-access.*.id}"
            ]
        3. we use autoscaling to launch the Bastion instance, where we specify the max and min size of the instances we want. 
```

##### Cloudtrail
```hcl
    Enabling global events and log files monitoring, and uploading results to the S3 bucket with policies that allow GetAccessControl List and PutObject into S3 Bucket with policy
    statement {
		sid = "AWSCloudTrailAclCheck"
		effect = "Allow"
		
		actions = [
            "s3:GetBucketAcl"
        ]
    statement {
        sid = "AWSCloudTrailWrite"
		effect = "Allow"
		
		actions = [
            "s3:PutObject"
        ]

```
##### DHCP
```
    standard for passing configuration information to hosts on a TCP/IP network. The options field of a DHCP message contains the configuration parameters. 
    
    Some of those parameters are the DNS, NTP. here we have multiple DNS and NTP servers we split them by using , 
    domain_name_servers = ["${split(",", var.dhcp_dns_servers)}"]
    ntp_servers         = ["${split(",", var.dhcp_ntp_servers)}"]
```
##### Flow Log
```hcl
    in this cloud watch we are creating a *flow_log_group* that has a STS assume sole assigned to it and a 
    policy that does following actions: 

        "logs:CreateLogGroup",
			"logs:CreateLogStream",
			"logs:PutLogEvents",
			"logs:DescribeLogGroups",
			"logs:DescribeLogStreams"

    now creating a flow_log which is assigned to the *flow_log_group* and to the sts_assume iam role with 
    the mentioned policy actions that can perform

```

##### IGW
``` hcl
    Here we are assigning internet gateway to instance by

```

##### NACL

```hcl 
    Network access list, bascially at VPC level they are firewall rules at network level, to only allow particular egress, ingress and allocate to subnets we need to use the NACL.
```
##### NAT instance

```hcl
    
```
Nat instance, here is the launch configuration for NAT instance that autoscaling uses while spinning up a nat instance or a nat_gateway, we are creating and EIP based on IGW and assigning it to the VPC. 
we are allocating Subnets and EIP to the Natgateway that we are creating. assign new poliies to the nat instance were actions we allow are 
```
    "Action":                           #Policy that will be attached to nat instance along with the role mentioned below
     "ec2:AttachNetworkInterface",
        "ec2:ModifyInstanceAttribute"

    "Action": "sts:AssumeRole",         #ROLE
      "Principal": {
        "Service": "ec2.amazonaws.com"
```
assign this polocy to the nat instance makes it possible for us to make changes on nat instance on internal level, we use terraform template file as a userdata. 

##### NAT-REDHAT.SH.TPL

Terraform template will be able to dump the userdata on to the nat-instance that we launch, and we are attaching ENI (Elastic Network Insterface) that will allow instance to use other resources of the AWS and modify 

A network interface can include the following attributes:

A primary private IPv4 address from the IPv4 address range of your VPC

One or more secondary private IPv4 addresses from the IPv4 address range of your VPC

One Elastic IP address (IPv4) per private IPv4 address

One public IPv4 address

One or more IPv6 addresses

One or more security groups

A MAC address

A source/destination check flag

we are searching for the Instance and then making source and destination check is false,
attach the ENI_ID to the instance that we launched and use time intervals to re try

```hcl
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
```

Once ENI is attached start configuring the ETH and changes network and routes 

ensuring that the ETH changes are internal zone, cause for security reasons we want to make sure whole organization uses same IP ex: 24.30.10.10

we use PAT for associating different ports for different sessions. 

PAT session will have ex: 24.30.10.10: 5000, 24.30.10.10:5001 unique port for every session 
