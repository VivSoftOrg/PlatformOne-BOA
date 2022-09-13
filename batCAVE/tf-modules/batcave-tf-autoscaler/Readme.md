## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |
| <a name="provider_helm"></a> [helm](#provider\_helm) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_iam_policy.batcave_autoscaler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role_policy_attachment.autoscaler_policy_attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [helm_release.autoscaler](https://registry.terraform.io/providers/hashicorp/helm/latest/docs/resources/release) | resource |
| [aws_eks_cluster.cluster](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/eks_cluster) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_cluster_name"></a> [cluster\_name](#input\_cluster\_name) | n/a | `any` | n/a | yes |
| <a name="input_general_asg_name"></a> [general\_asg](#input\_general\_asg) | n/a | `any` | n/a | yes |
| <a name="input_general_asg_max"></a> [general\_asg\_max](#input\_general\_asg\_max) | n/a | `string` | `"5"` | no |
| <a name="input_general_asg_min"></a> [general\_asg\_min](#input\_general\_asg\_min) | n/a | `string` | `"1"` | no |
| <a name="input_helm_name"></a> [helm\_name](#input\_helm\_name) | n/a | `string` | `"auto-scaler"` | no |
| <a name="input_helm_namespace"></a> [helm\_namespace](#input\_helm\_namespace) | ## Helm variables | `string` | `"kube-system"` | no |
| <a name="input_iam_path"></a> [iam\_path](#input\_iam\_path) | n/a | `string` | `"/delegatedadmin/developer/"` | no |
| <a name="input_permissions_boundary"></a> [permissions\_boundary](#input\_permissions\_boundary) | n/a | `string` | `"arn:aws:iam::373346310182:policy/cms-cloud-admin/developer-boundary-policy"` | no |
| <a name="input_provider_url"></a> [provider\_url](#input\_provider\_url) | n/a | `string` | `""` | no |
| <a name="input_runner_asg_name"></a> [runner\_asg](#input\_runner\_asg) | n/a | `any` | n/a | yes |
| <a name="input_runner_asg_max"></a> [runner\_asg\_max](#input\_runner\_asg\_max) | n/a | `string` | `"5"` | no |
| <a name="input_runner_asg_min"></a> [runner\_asg\_min](#input\_runner\_asg\_min) | n/a | `string` | `"0"` | no |
| <a name="input_worker_iam_role_name"></a> [worker\_iam\_role\_name](#input\_worker\_iam\_role\_name) | n/a | `string` | `""` | no |

## Outputs

No outputs.
