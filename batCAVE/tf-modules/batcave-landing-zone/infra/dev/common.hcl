locals {
  ami                  = "ami-00200823951b17192"
  environment          = "dev"
  directory_name       = "dev"
  account              = "cms"
  project              = "batcave"
  owner                = "cms"
  cluster_name         = get_env("CLUSTER_NAME")

  iam_path             = "/delegatedadmin/developer/"
  permissions_boundary = "arn:aws:iam::373346310182:policy/cms-cloud-admin/developer-boundary-policy"

  base_domain          = "batcave-dev.internal.cms.gov"

  tf_module_source  = "git@github.com:CMSgov"

  tf_autoscaler_ref = "main"
  tf_buckets_ref    = "main"
  tf_cluster_ref    = "main"
  tf_configmap_ref  = "main"
  tf_gatus_ref      = "main"
  tf_kms_ref        = "main"
  tf_route53_ref    = "main"
  tf_vpc_ref        = "main"
  tf_postgresql_ref = "main"
  tf_serverless_ref = "main"

  aws_region = get_env("AWS_DEFAULT_REGION", "us-east-1")
  aws_id     = get_aws_account_id()
}
