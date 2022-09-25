## VPC-Peering 

VPC-peering can be inside a same account or cross account, VPC peering doesn't require STS assume roles for peering, variables( information we need for doing a VPC peering are):

##### Variables

**Variables**                | **Description**
-----------------------------|-------------------------------------------------------------------
**require_vpc_peering**      | how many vpc peering connections are required !
**remote_bucket**            | S3 bucket that stores state file that has configuration of the 
**remote_key**               | The path to the state file inside the bucket
**peer_owner_id**            | The AWS account ID of the owner of the peer VPC
**peer_vpc_id**              | The ID of the VPC with which you are creating the VPC Peering Connection
**client_code**              | 
**environment**              |
**account_code**             | Account number of which we want VPC to peer

##### Backend 

```hcl
    config {
      bucket = "${lower(var.client_code)}-${lower(var.environment)}-${lower(var.project)}" 
      key = "tfstate/${var.account_code}/vdms-vpc"
      region = "${data.aws_region.current.id}"
      encryption = true
  }
  ```
    accessing S3 bucket that is storing the tfstate file and the Key value for the VDMS-VPC
    that will enable the program get access to the vdms account get information of the vpc that needs to be peered! to another account 

##### Main
    Shake hand between VPC's need to happen from both sides, i.e., VDMS-VPC and the requesting VPC. 
