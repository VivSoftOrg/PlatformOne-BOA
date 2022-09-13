# AWS (Amazon Web Services) Architecture IaC (Infrastructure as Code) 
 
## But what is IaC? 
 
Instead of standing up the infrastructure manually, we use code to declaratively define the whole infrastructure. A format definition for IaC states this: 
IaC is provisioning infrastructure via software to achieve consistent and predictable environment. 
 
**Current Limitations:** 
 
- It is difficult for you know what resources you have created over Cloud. 
- Creating those resource manually is a time-consuming task. 
- There are chances of human errors while configuring those resources. 
- No versioning of resource configuration. 
- Replicating resources for creating separate environment would be a painful job 
 
For Infrastructure as Code, we recommend using Terraform. 
 
# Why Terraform? 
 
Terraform provides an efficient way of provisioning and managing the infrastructure. Terraform is an opensource project, which is developed by Hashi Corp, which helps in achieving the Infrastructure as Code. It helps in building, changing and version infrastructure safely and efficiently. Terraform can not only create new resources for you but can also import your existing infrastructure into code. Terraform used HCL (Hashi Corp Configuration language) for managing the configuration. 
 
# Advantage of using Terraform 
 
- **Declarative**: This means that a DevSecOps Engineer need not write the whole APIs (Application Programming Interfaces). We can just pass parameters for the resources we want to create and Terraform will automatically create those resources for us. 
 
- **Idempotent**: This means that terraform maintains the existing state and whenever we create new configs to setup infrastructure, it will initially check the new configuration with the existing state and checks what are new creations, updating and destruction in the current state. 
 
- **Push Mechanism**: This means that we need to push the configuration explicitly to Terraform to make necessary changes. Terraform will not pick the changes without push. 
 
# Advantages 
 
- **Documented Architecture**: Terraform lets us to keep track of what resources we are creating as they are defined in the code 
- **Automated Deployment**: Creation of these resources are quick and automated. 
- **Consistent Environment**: Since there is no human intervention, that spawned up infra remains consistent 
- **Reusable Components**: Replicating the resources for setting up a different environment can be done very quickly as the scripts are already prepared. 
- **Source Controlled Infrastructure**: The Infrastructure code is source controlled and hence can be easily versioned. 
 
# What included in this folder? 
 
- core-iam: IaC using Terraform that will create IAM (Identity and Access Management) policies, Roles and Groups. 
- database: IaC using Terraform that will create different databases available in AWS. 
- efs-comm: IaC using Terraform that will create Network File Systems (NAS) in AWS. 
- efs-ap: IaC using Terraform that will create mounts on EFS. 
- exiting_vpc: IaC using Terraform that will deploy resources into existing VPC (Virtual Private Cloud) 
- route53: IaC using Terraform that will deploy and manage DNS (Domain Name System) route53 in AWS. 
- vpc: IaC using Terraform that will create virtual private cloud 
- vpc_peering: IaC using Terraform will create VPC peering request  
- vpc_peering_acceptance: IaC using Terraform that will accept VPC peering. 
- workload-iam: IaC using Terraform that will create IAM roles. 
