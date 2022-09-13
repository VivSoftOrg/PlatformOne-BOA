locals {
  ami                  = "ami-00200823951b17192"
  environment          = "prod"
  directory_name       = "prod"
  account              = "cms"
  project              = "batcave"
  owner                = "cms"
  cluster_name         = "batcave-prod"
  iam_path             = "/delegatedadmin/developer/"
  permissions_boundary = "arn:aws:iam::863306670509:policy/cms-cloud-admin/developer-boundary-policy"
  base_domain          = "batcave.internal.cms.gov"

  tf_module_source  = "git@github.com:CMSgov"

  gitlab_storage_bucket      = "batcave-prod-gitlab-storage"
  gitlab_runner_cache_bucket = "batcave-prod-runner-cache"

  aws_region = get_env("AWS_DEFAULT_REGION", "us-east-1")
  aws_id     = get_aws_account_id()
}
