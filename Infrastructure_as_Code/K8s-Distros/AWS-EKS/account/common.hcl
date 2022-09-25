locals {
    account_id = get_aws_account_id()
    aws_region = "us-east-1"

    # each new account should be specified here with env level and project top level name
    account_map = {
        "373346310182" = {
            "env" = "dev",
            "project" = "batcave"
        },
        "831579051573" = {
            "env" = "test",
            "project" = "batcave"
        },
        "111594127594" = {
            "env" = "impl",
            "project" = "batcave"
        },
        "863306670509" = {
            "env" = "prod",
            "project" = "batcave"
        },
        "368332260651" = {
            "env" = "dev",
            "project" = "sssa"
        },
        "724350100575" = {
            "env" = "test",
            "project" = "sssa"
        },
        "546924760321" = {
            "env" = "prod",
            "project" = "sssa"
        },
    }
    environment = local.account_map[local.account_id]["env"]
    project = local.account_map[local.account_id]["project"]
    cluster_name = "${local.project}-${local.environment}"

    tf_module_source  = "https://code.batcave.internal.cms.gov/batcave-iac"
}
