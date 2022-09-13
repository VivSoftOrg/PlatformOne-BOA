# [variables.tf](variables.tf)

Variables file for sub-project **core-iam**.
It defines all variables which are useful for **core-iam** sub-project.
Variables defined in [**customer.yml**](../../config/example-customer.yml) file overrides similar variables in this file


## Details

| Variables               | Description                               | Default Value                      |Data Type|
|-------------------------|-------------------------------------------|------------------------------------|---------|
| environment             | Defines the environment. Used in tagging resources created   | -     | String  |
| owner     | Specifies owner of resources that are created in this sub-project. Also used in tagging | viv_softcloud                 | String |
| project                | Project for which the resources are created. Used in tagging the resources               | viv_softPlatform                     | String  |
| client_code            | Used for resources that have "global" naming space. Mostly for S3               | -                                 | String |
| account_code | Core account code | - | String |
| output_dir | Output directory | target | String |
| platform_bucket | Bucket to push tfstate and other atifacts to | - | String |
| platform_admin_users    | A list of IAM user name(s) that should be allowed to administer the platform infrastructure.| - | List |
| elb_logs_bucket | Bucket name to store ELB logs in | - | String |
| jenkins_allow_tfdeploy | Shall jenkins be allowed to assume tfdeploy role | false | Boolean | 
| workload_account_ids | Comma-delimited list of AWS account ID(s) for workload accounts| -  | String  |
| expiration_date         | Expiration date for the resource created               | -                        | String |