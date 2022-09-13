# Onboarding and Prerequisites
The instructions in this doc assume you have completed all [Batcave Onboarding](https://coda.io/d/batCAVE-Onboarding_dn7v5wg97i-/batCAVE-ONBOARDING-WELCOME_suXVs) including having all required job codes and CMS Cloud VPN access.

## Add Batcave Infra Team Job Codes
The following Batcave infra team job codes need to be requested, follow (and bookmark!) this [link](https://eua.cms.gov/iam/im/pri/cui7/index.jsp?task.tag=ModifyMyJobCodes) and add the following job codes:
```
BAT_CLUSTER_ADMIN
BAT_DEV_CLUSTER_ADM
BAT_SIG_CLUSTER_ADMIN
BAT_SIG_DEV_CLUSTER_ADM
BAT_SIG_TEST_CLUSTER_ADM
BAT_TEST_CLUSTER_ADM
BAT_TEST_USER
BAT_USER
```

## Connect to the VPN
You have 2 options for connecting your machine to the CMS Cloud VPN
1. Cisco AnyConnect Client (preferred): follow the instructions [here](https://coda.io/d/batCAVE-Onboarding_dn7v5wg97i-/CMS-VPN-Guide-Cisco-AnyConnect_sueJk#_lu72h)
2. Openconnect VPN CLI client: use this option to connect to the CMS Cloud VPN if you prefer to use the CLI or the Cisco Anyconnect client is malfunctioning. Add the following as a script in the location of your choice
```
sudo openconnect --user <your cms eua id> --protocol=anyconnect --servercert pin-sha256:YGoq3wg0ihK9NgKXt5YWF9MrtQgiVizhNVk2kr2V3PE= cloudvpn.cms.gov
```

## Cloudtamer AWS Access (VPN Required!)
CMS uses [Cloudtamer](https://cloudtamer.cms.gov/portal) (must be on VPN to access) to manage access AWS accounts. In order to log into CMS AWS accounts via the CLI, you will first need to set up a few things, see instructions [here](./Cloudtamer-Access.md).  

## Direnv
In order to minimize mistakes and automate environment-specific setups we require all devs to use [direnv](https://direnv.net/)
```
brew install direnv
```

Note if you are using `zsh` you will also need to add the following line to your `.zshrc` file:
```shell
eval "$(direnv hook zsh)"
```

In the root of the this cloned repo, create a copy of `.envrc.example`, rename it to `.envrc` and update it with your desired DEV cluster name (typically something like yourFirstName-dev). This is done so that the dev environment variables are loaded by default, which prevents inadvertently applying changes to other clusters. 

You will then need to run `direnv allow .` to allow `direnv` to load the environment variables. If everything was successful you should see output like:
```
direnv: loading ~/workspace/cms/batcave-landing-zone/.envrc
direnv: export +AWS_DEFAULT_REGION +CLUSTER_NAME
```

IMPORTANT: verify this worked by running `export | grep CLUSTER_NAME` and verifying it is set to the value you wrote in above.  

You'll also notice that `.envrc` files have been placed throughout the repo in the `infra/<ENV>` and `apps/batcave/envs/<ENV>` folders. When you `cd` into those folders, the new environment variables for that particular environment will be loaded, and when you leave that folder they will be unloaded and replaced by the dev environment variables created above.

## Additional Required Packages
Additional packages that need to be installed :
```
brew install kubectl helm kustomize terraform terragrunt
```

Now that all prerequisites have been met, proceed to the Quickstart over in the [README](../../README.md#quickstart)