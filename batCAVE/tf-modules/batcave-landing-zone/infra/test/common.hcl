locals {
  ami                  = "ami-00200823951b17192"
  environment          = "test"
  directory_name       = "test"
  account              = "cms"
  project              = "batcave"
  owner                = "cms"
  cluster_name         = "batcave-test"
  iam_path             = "/delegatedadmin/developer/"
  permissions_boundary = "arn:aws:iam::831579051573:policy/cms-cloud-admin/developer-boundary-policy"
  base_domain          = "batcave-test.internal.cms.gov"

  tf_module_source  = "https://code.batcave.internal.cms.gov/batcave-iac"

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

  gitlab_storage_bucket      = "batcave-test-gitlab-storage"
  gitlab_runner_cache_bucket = "batcave-test-runner-cache"

  aws_region = get_env("AWS_DEFAULT_REGION", "us-east-1")
  aws_id     = get_aws_account_id()
}
