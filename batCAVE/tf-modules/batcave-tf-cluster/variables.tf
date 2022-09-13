variable "region" {
  default = "us-east-1"
}

variable "environment" {
  default = "dev"
}

variable "cluster_version" {
  default = "1.21"
}

## Default node group
variable "general_node_pool" {
  type        = any
  description = "General node pool, required for hosting core services"
  default = {
    instance_type = "c5.2xlarge"
    desired_size  = 3
    max_size      = 5
    min_size      = 2
    # Map of label flags for kubelets.
    labels = { general = "true" }
    # Map of taint flags for kubelets.
    # Ex: `{MyTaint = "true:NoSchedule"}`
    taints = {}
    #tags = {}

    # Extra args for kubelet in form of: "--node-labels=general=true <...>'.  Will be in _addition_ to any 
    # other args added by the labels and taints values
    #extra_args = "--node-labels=general=true"


    #volume_size                  = "300"
    #volume_type                  = "gp3"
    #volume_delete_on_termination = true
  }
}

variable "custom_node_pools" {
  type    = any
  default = {}
  #  runners = {
  #    instance_type = "c4.xlarge"
  #    desired_size = 1
  #    max_size = 1
  #    min_size = 1
  #    labels = { gitlab-runners-go-here = "true" }
  #    taints = { better-watch-out-for-gitlab-runners = "true:NoSchedule" }
  #  }
}

variable "cluster_name" {}

variable "iam_role_path" {
  default = "/delegatedadmin/developer/"
}

variable "iam_role_permissions_boundary" {
  default = "arn:aws:iam::373346310182:policy/cms-cloud-admin/developer-boundary-policy"
}

variable "vpc_id" {}

variable "private_subnets" {
  type = list(any)
}

variable "transport_subnet_cidr_blocks" {
  type    = map(string)
  default = {}
}

variable "transport_subnets_by_zone" {
  type    = map(string)
  default = {}
}

variable "transport_subnets" {
  type    = list(any)
  default = []
}

variable "alb_subnets_by_zone" {
  type = map(string)
}

variable "cluster_endpoint_private_access" {
  default = "true"
}
variable "cluster_endpoint_public_access" {
  default = "true"
}

variable "cluster_enabled_log_types" {
  description = "A list of the desired control plane logging to enable. For more information, see Amazon EKS Control Plane Logging documentation (https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html)"
  type        = list(string)
  default     = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
}

variable "enable_irsa" {
  default = "true"
}

### AWS Launch Template variables

variable "lt_name_prefix" {
  default = "eks-lt-"
}
variable "lt_description" {
  default = "Default Launch-Template"
}
variable "lt_update_default_version" {
  default = "true"
}
variable "lt_image_id" {
  default = "ami-0d111bb0f1e4a9787"
}


### Block device mappings

variable "block_device_name" {
  default = "/dev/xvda"
}
variable "block_volume_size" {
  type    = number
  default = 100
}
variable "block_volume_type" {
  default = "gp2"
}
variable "block_delete_on_termination" {
  default = "true"
}
variable "block_encrypted" {
  default = "true"
}


### Monitoring
variable "lt_monitoring_enabled" {
  default = "true"
}


### Network Interfaces
variable "network_int_associate_public_ip_address" {
  default = "false"
}
variable "network_int_delete_on_termination" {
  default = "true"
}


### Resource tags

variable "instance_tag" {
  default = "Instance custom tag"
}
variable "volume_tag" {
  default = "Volume custom tag"
}
variable "network_interface_tag" {
  default = "Network Interface custom tag"
}

variable "general_nodepool_tags" {
  type = any
  default = {
  }
}
### Launch template tags

variable "lt_CustomTag" {
  default = "Launch template custom tag"
}


# ## KMS Key ARN from KMS module
# variable "kms_key_arn" {}

variable "transport_proxy_static_ip" {
  type    = bool
  default = true
}

variable "transport_proxy_is_internal" {
  type        = bool
  default     = true
  description = "Boolean to trigger a public transport proxy ip"
}

variable "cluster_additional_sg_prefix_lists" {
  type = list(string)
}

variable "cluster_security_group_additional_rules" {
  type        = map(any)
  description = "Map of security group rules to attach to the cluster security group, as you cannot change cluster security groups without replacing the instance"
  default     = {}
}

variable "grant_delete_ebs_volumes_lambda_access" {
  type = bool
  default = false
  description = "When set to true, a cluster role and permissions will be created to grant the delete-ebs-volumes Lambda access to the PersistentVolumes API."
}

variable "node_https_ingress_cidr_blocks" {
  description = "List of CIDR blocks to allow into the node over the HTTPs port"
  default     = ["10.0.0.0/8"]
  type        = list(string)
}

variable "create_alb_proxy" {
  type        = bool
  description = "Create an Application Load Balancer proxy to live in front of the K8s ALB and act as a proxy from the public Internet"
  default     = false
}
variable "alb_proxy_is_internal" {
  type        = bool
  description = "If the ALB Proxy should be using internal ips.  Defaults to false, because the reason for ALB proxy existing is typically to make it accessible over the Internet"
  default     = false
}

variable "alb_proxy_subnets" {
  description = "List of subnet ids for the ALB Proxy to be deployed into"
  default     = []
  type        = list(string)
}

variable "acm_cert_base_domain" {
  description = "Base domain of the certificate used for the ALB Proxy"
  default     = ""
  type        = string
}

variable "alb_proxy_ingress_cidrs" {
  description = "List of CIDR blocks allowed to access the ALB Proxy; used to restrict public access to a certain set of IPs"
  default     = []
  type        = list(string)
}
variable "alb_proxy_ingress_prefix_lists" {
  description = "List of Prefix List IDs allowed to access the ALB Proxy; used to restrict public access to a certain set of IPs"
  default     = []
  type        = list(string)
}
variable "alb_deletion_protection" {
  description = "Enable/Disable ALB deletion protection for both ALBs"
  default     = false
  type        = bool
}
variable "s3_bucket_access_grants" {
  description = "A list of s3 bucket names to grant the cluster roles R/W access to"
  default     = null
  type        = list(string)
}

variable "logging_bucket" {
  description = "Name of the S3 bucket to send load balancer access logs."
  default     = null
  type        = string
}

### Cosign OpenID Connect Audiences
variable "openid_connect_audiences" {
  description = "OpenID Connect Audiences"
  default     = []
  type        = list(string)
}
variable "create_cosign_iam_role" {
  description = "Flag to create Cosign IAM role"
  default     = false
}

variable "autoscaling_group_tags" {
  description = "Tags to apply to all autoscaling groups created"
  default     = {}
  type        = map(any)
}
