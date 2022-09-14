locals {
  k8s_service_account_namespace = "kube-system"
  k8s_service_account_name      = "autoscaler-aws-cluster-autoscaler"
}

resource "aws_iam_policy" "batcave_autoscaler" {
  name = "autoscaler-policy-${var.cluster_name}"
  path = var.iam_path
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "autoscaling:DescribeAutoScalingGroups",
          "autoscaling:DescribeAutoScalingInstances",
          "autoscaling:DescribeLaunchConfigurations",
          "autoscaling:DescribeTags",
          "autoscaling:SetDesiredCapacity",
          "autoscaling:TerminateInstanceInAutoScalingGroup",
          "ec2:DescribeLaunchTemplateVersions",
          "ec2:DescribeInstanceTypes",
          "ec2:GetInstanceTypesFromInstanceRequirements",
          "ec2:DescribeImages",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

module "iam_assumable_role_admin" {
  source                        = "terraform-aws-modules/iam/aws//modules/iam-assumable-role-with-oidc"
  create_role                   = true
  role_name                     = "${var.cluster_name}-cluster-autoscaler"
  provider_url                  = replace(var.cluster_oidc_issuer_url, "https://", "")
  role_policy_arns              = [aws_iam_policy.batcave_autoscaler.arn]
  oidc_fully_qualified_subjects = ["system:serviceaccount:${local.k8s_service_account_namespace}:${local.k8s_service_account_name}"]
  role_path                     = var.iam_path
  role_permissions_boundary_arn = var.permissions_boundary
}
