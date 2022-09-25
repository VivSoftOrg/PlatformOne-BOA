# Account Level Configurations

## Run me
From this directory:
* Export AWS credentials to ENV
* Run terragrunt inits and plans 
    ```
    terragrunt run-all init --reconfigure && terragrunt run-all plan --terragrunt-source-update
    ```
* The `--reconfigure` flag is important because the backend file cached by terragrunt will refer to the account last used.

* The `--terragrunt-source-update` flag is really only necessary when you have a cached version of a module. You could also run `find . -type d -name ".terragrunt-cache" -prune -exec rm -rf {} \;` from a top level directory.

*  Run `terragrunt run-all apply`
* If you are configuring a new account for the first time, you'll need to put the slack webhook url secret with the local [put-secrets.sh](./security-alerts/put-secret.sh) script.
    ```
    $  security-alerts/put-secret.sh "https://hooks.slack.com/services/XXXXX/XXXX/XXXXXX"
    ```
    * Tip: put a space in front of the command so it doesnt save to your bash history.
* If you configured a brand new account, you'll also need to update production so panther-logs gets the new replication values.

## Modules

[security-alerts](./security-alerts) hosts the Security Hub to slack integration for batCAVE accounts.

[panther-replication](./panther-replication) is run in every account to replicate logs from the cms-cloud logging bucket to a staging bucket in batCAVE prod for SDL ingestion.

[panther-logs](./panther-logs) is only run in batCAVE prod and hosts the configuration for Panther log ingestion from the staging bucket.

[delete-ebs-volumes](./delete-ebs-volumes/) is only run in batcave dev and test. This module deploys a Lambda function to delete EBS volumes whose status is "Available". This function will run everyday at 11 PM Hawaii time (5 AM EST).

## Integrating a new account level module
1. Create a subfolder in this directory
2. Create a terragrunt.hcl file in the new directory
    ```
    locals {
    common = read_terragrunt_config(find_in_parent_folders("common.hcl")).locals
    }

    include "parent" {
    path = find_in_parent_folders()
    }

    terraform {
    source = "git::https://REPOURL.com"
    }
    ```
3. Run-all on each account.