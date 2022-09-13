locals {
  ami                  = "ami-00200823951b17192"
  environment          = "impl"
  directory_name       = "impl"
  account              = "cms"
  project              = "batcave"
  owner                = "impl"
  cluster_name         = "batcave-impl"
  iam_path             = "/delegatedadmin/developer/"
  permissions_boundary = "arn:aws:iam::111594127594:policy/cms-cloud-admin/developer-boundary-policy"
  base_domain          = "batcave-impl.internal.cms.gov"

  tf_module_source = "git@github.com:CMSgov"

  aws_region = get_env("AWS_DEFAULT_REGION", "us-east-1")
  aws_id     = get_aws_account_id()
}
