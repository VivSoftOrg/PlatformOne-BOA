# Maintainability and Availability 
 
## Availability and Maintainability of High-Performance Kubernetes Cluster AutoScaler and AWS (Amazon Web Services) Auto Scaling Groups requires IaC (Infrastructure as Code) and CaC. 
 
We configure AWS Autoscaling and Karpenter based Kubernetes cluster scaling using Terraform to maintain high availability for Platform One. 
 
 
## Why we selected karpenter? 
 
**Accelerated Computing**: Karpenter works with all kinds of Kubernetes applications, but it performs particularly well for use cases that require rapid provisioning and deprovisioning large numbers of diverse compute resources quickly. For example, this includes batch jobs to train machine learning models, run simulations, or perform complex financial calculations. You can leverage custom resources of nvidia.com/gpu, amd.com/gpu, and aws.amazon.com/neuron for use cases that require accelerated EC2 instances. 
 
**Provisioners Compatibility**: Kapenter provisioners are designed to work alongside static capacity management solutions like Amazon EKS (Elastic Kubernetes Service) managed node groups and EC2 Auto Scaling groups. You may choose to manage the entirety of your capacity using provisioners, a mixed model with both dynamic and statically managed capacity, or a fully static approach. We recommend not using Kubernetes Cluster AutoScaler at the same time as Karpenter because both systems scale up nodes in response to Un schedulable pods. If configured together, both systems will race to launch and terminate instances for these pods.

## How to use and Configure Karpenter?

When Karpenter is installed in your cluster, Karpenter observes the aggregate resource requests of unscheduled pods and makes decisions to launch new nodes and terminate them to reduce scheduling latencies and infrastructure costs. Karpenter does this by observing events within the Kubernetes cluster and then sending commands to the underlying cloud provider’s compute service, such as Amazon EC2.

### Getting Started with Karpenter on AWS

To get started with Karpenter in any Kubernetes cluster, ensure there is some compute capacity available, and install it using the Helm charts provided in the public repository. Karpenter also requires permissions to provision compute resources on the provider of your choice.

Once installed in your cluster, the default Karpenter provisioner will observe incoming Kubernetes pods, which cannot be scheduled due to insufficient compute resources in the cluster and automatically launch new resources to meet their scheduling and resource requirements.

![Karpenter](Images/karpenter.png)

We want to show a quick start using Karpenter in an Amazon EKS cluster based on Getting Started with Karpenter on AWS. It requires the installation of AWS Command Line Interface (AWS CLI), kubectl, eksctl, and Helm (the package manager for Kubernetes). After setting up these tools, create a cluster with eksctl. This example configuration file specifies a basic cluster with one initial node.

## Requirements

- EKS Cluster

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |
| <a name="provider_helm"></a> [helm](#provider\_helm) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_iam_assumable_role_karpenter"></a> [iam\_assumable\_role\_karpenter](#module\_iam\_assumable\_role\_karpenter) | terraform-aws-modules/iam/aws//modules/iam-assumable-role-with-oidc | 4.7.0 |

## Resources

| Name | Type |
|------|------|
| [aws_iam_instance_profile.karpenter](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_instance_profile) | resource |
| [aws_iam_policy.karpenter_contoller](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_policy.ssm_managed_instance](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role_policy_attachment.karpenter_contoller_policy_attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.karpenter_ssm_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [helm_release.karpenter](https://registry.terraform.io/providers/hashicorp/helm/latest/docs/resources/release) | resource |
| [aws_eks_cluster.cluster](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/eks_cluster) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_cluster_endpoint"></a> [cluster\_endpoint](#input\_cluster\_endpoint) | Cluster Endpoint | `string` | `""` | no |
| <a name="input_cluster_name"></a> [cluster\_name](#input\_cluster\_name) | EKS Cluster Name | `any` | "" | yes |
| <a name="input_helm_create_namespace"></a> [helm\_create\_namespace](#input\_helm\_create\_namespace) | Create Namespace for Karpenter | `bool` | `true` | no |
| <a name="input_helm_name"></a> [helm\_name](#input\_helm\_name) | Helm Name | `string` | `"karpenter"` | no |
| <a name="input_helm_namespace"></a> [helm\_namespace](#input\_helm\_namespace) | Helm Chart Install Namespace | `string` | `"karpenter"` | no |
| <a name="input_iam_path"></a> [iam\_path](#input\_iam\_path) | IAM Path if applicable | `string` | `""` | no |
| <a name="input_permissions_boundary"></a> [permissions\_boundary](#input\_permissions\_boundary) | permissions boundary if applicable | `string` | `""` | no |
| <a name="input_provider_url"></a> [provider\_url](#input\_provider\_url) | Provider URL | `string` | `""` | no |
| <a name="input_worker_iam_role_name"></a> [worker\_iam\_role\_name](#input\_worker\_iam\_role\_name) | Worker Nodes IAM Role | `string` | `""` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_hr_manifest"></a> [hr\_manifest](#output\_hr\_manifest) | The rendered manifest of the release as JSON |
| <a name="output_karpenter_iam"></a> [karpenter\_iam](#output\_karpenter\_iam) | IAM policy created for Karpenter's use |

## Install

Plan:
`terraform plan`

Deploy:
`terraform apply`

Destroy:
`tterraform destroy`

## Creating Provisioner profile for Karpenter
```
cat <<EOF | kubectl apply -f -
apiVersion: karpenter.sh/v1alpha5
kind: Provisioner
metadata:
name: default
spec:
#Requirements that constrain the parameters of provisioned nodes. 
#Operators { In, NotIn } are supported to enable including or excluding values
  requirements:
    - key: "node.kubernetes.io/instance-type" #If not included, all instance types are considered
      operator: In
      values: ["m5.large", "m5.2xlarge"]
    - key: "topology.kubernetes.io/zone" #If not included, all zones are considered
      operator: In
      values: ["us-east-1a", "us-east-1b"]
    - key: "kubernetes.io/arch" #If not included, all architectures are considered
   operator: In
      values: ["arm64", "amd64"]
    - key: " karpenter.sh/capacity-type" #If not included, the webhook for the AWS cloud provider will default to on-demand
      operator: In
      values: ["spot", "on-demand"]
  provider:
    instanceProfile: KarpenterNodeInstanceProfile-eks-karpenter-demo
  ttlSecondsAfterEmpty: 30  
EOF
```

Testing Karpenter

Usecase : Create some pods using a deployment and watch Karpenter provision nodes in response.

`kubectl create deployment inflate --image=public.ecr.aws/eks-distro/kubernetes/pause:3.2 --requests.cpu=1`

Let’s scale the deployment and check out the logs of the Karpenter controller.

```
$ kubectl scale deployment inflate --replicas 10
$ kubectl logs -f -n karpenter $(kubectl get pods -n karpenter -l karpenter=controller -o name)
2021-11-23T04:46:11.280Z        INFO    controller.allocation.provisioner/default       Starting provisioning loop      {"commit": "abc12345"}
2021-11-23T04:46:11.280Z        INFO    controller.allocation.provisioner/default       Waiting to batch additional pods        {"commit": "abc123456"}
2021-11-23T04:46:12.452Z        INFO    controller.allocation.provisioner/default       Found 9 provisionable pods      {"commit": "abc12345"}
2021-11-23T04:46:13.689Z        INFO    controller.allocation.provisioner/default       Computed packing for 10 pod(s) with instance type option(s) [m5.large]  {"commit": " abc123456"}
2021-11-23T04:46:16.228Z        INFO    controller.allocation.provisioner/default       Launched instance: i-01234abcdef, type: m5.large, zone: us-east-1a, hostname: ip-192-168-0-0.ec2.internal    {"commit": "abc12345"}
2021-11-23T04:46:16.265Z        INFO    controller.allocation.provisioner/default       Bound 9 pod(s) to node ip-192-168-0-0.ec2.internal  {"commit": "abc12345"}
2021-11-23T04:46:16.265Z        INFO    controller.allocation.provisioner/default       Watching for pod events {"commit": "abc12345"}
```

The provisioner’s controller listens for Pods changes, which launched a new instance and bound the provisionable Pods into the new nodes.

Now, delete the deployment. After 30 seconds (ttlSecondsAfterEmpty = 30), Karpenter should terminate the empty nodes.

```bash
$ kubectl delete deployment inflate
$ kubectl logs -f -n karpenter $(kubectl get pods -n karpenter -l karpenter=controller -o name)
2021-11-23T04:46:18.953Z        INFO    controller.allocation.provisioner/default       Watching for pod events {"commit": "abc12345"}
2021-11-23T04:49:05.805Z        INFO    controller.Node Added TTL to empty node ip-192-168-0-0.ec2.internal {"commit": "abc12345"}
2021-11-23T04:49:35.823Z        INFO    controller.Node Triggering termination after 30s for empty node ip-192-168-0-0.ec2.internal {"commit": "abc12345"}
2021-11-23T04:49:35.849Z        INFO    controller.Termination  Cordoned node ip-192-168-116-109.ec2.internal   {"commit": "abc12345"}
2021-11-23T04:49:36.521Z        INFO    controller.Termination  Deleted node ip-192-168-0-0.ec2.internal    {"commit": "abc12345"}
```

If you delete a node with kubectl, Karpenter will gracefully cordon, drain, and shut down the corresponding instance. Under the hood, Karpenter adds a finalizer to the node object, which blocks deletion until all pods are drained, and the instance is terminated.
