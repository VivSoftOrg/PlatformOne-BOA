# [variables.tf](variables.tf)

Variables file for sub-project **workload-iam**.
It defines all variables which are useful for **workload-iam** sub-project.
Variables defined in [**customer.yml**](../../config/example-customer.yml) file overrides similar variables in this file


## Details

| Variables               | Description                               | Default Value                      |Data Type|
|-------------------------|-------------------------------------------|------------------------------------|---------|
| environment             | Defines the environment. Used in tagging resources created   | -     | String  |
| owner     | Specifies owner of resources that are created in this sub-project. Also used in tagging | viv_softcloud                 | String |
| project                | Project for which the resources are created. Used in tagging the resources               | viv_softPlatform                     | String  |
| account_code | Core account code | - | String |
| client_code            | Used for resources that have "global" naming space. Mostly for S3               | -                                 | String |
| build_url    | Build URL of Jenkins. If executed locally it is set to Unknown | Unknown                        | String |
| core_aws_profile | AWS Profile name for core account | - | String |
| core_account_id | AWS Account ID for core account | - | String |
| core_account_code | Account code defined for core account | - | String |
| core_platform_admin_users | Comma-delimited list of users with admin access in core account | - | String |
| extra_jenkins_roles | Allow the main Jenkins role to run bootstrap. Not useful locally. | - | String |
| output_dir | Output directory | target | String |
| platform_bucket | Bucket to push tfstate and other atifacts to | - | String |
| platform_admin_users    | A list of IAM user name(s) that should be allowed to administer the platform infrastructure.| - | String |
| expiration_date         | Expiration date for the resource created               | -                        | String |