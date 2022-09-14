# batcave-landing-zone

This project contains the Infrastructure as Code to build and deploy the Batcave platform

___
## Architecture
Latest architecture documentation can be found in the Batcave Coda at the following locations:
- [Technology Diagram](https://coda.io/d/batCAVE-Team-1-Gotham-Infrastructure_dBNMCvHi11e/Technology-Diagram_su4ja#_luFA6)
- [ADO Workflow Diagram](https://coda.io/d/batCAVE-Team-1-Gotham-Infrastructure_dBNMCvHi11e/ADO-Workflow-Diagram_su2aF#_luYmr)
- Other diagrams can be found in this [Coda folder](https://coda.io/d/batCAVE-Team-1-Gotham-Infrastructure_dBNMCvHi11e/Documentation_suOqF#_luVeH)
### Environments
#### Dev
- Short-lived environment used for Batcave development and testing
#### Test
- Long-lived pre-prod environment used to test changes and upgrades to the Batcave
- Contains the Batcave Utility Belt and an instance of Gitlab to test changes and upgrades to the Pipeline team infrastructure
#### Prod
- Long-lived production environment used daily by the Pipeline team
- Contains prod instances of Utility Belt and Gitlab
#### Impl
- Long-lived shared development environment used to smoke test and test drive new pipeline features
- This is the first environment that many ADOs will be onboarded onto

## Getting Started
New developers should visit [Onboarding and Prerequisites](docs/onboarding/Onboarding-and-Prerequisites.md) to setup their machines to do development work on Batcave. These are mandatory steps before proceeding with the Quickstart instructions below.

## Quickstart
### Install Flux
You will need the Flux CLI at exactly v0.31.5, binary can be downloaded [here](https://github.com/fluxcd/flux2/releases/tag/v0.31.5)
- note that the Flux CLI is not currently [backwards compatible](https://fluxcd.io/docs/migration/timetable/) and the required version to run Batcave changes with most Big Bang upgrades

### Build the AWS Infrastructure
Deploy the AWS infrastructure supporting Batcave using `terragrunt`
```shell
## ENV = [dev | test | prod]
cd infra/<ENV>
terragrunt run-all apply
```

### Deploying Batcave
Run the following 2 shell scripts to deploy Batcave
```shell
## ENV = [dev | test | prod]
cd infra/<ENV>
../../apps/batcave/1-update-eni-config.sh <ENV>
../../apps/batcave/2-deploy.sh <ENV>
```

A few notes on running the above scripts
- Those scripts should not be run on long-lived clusters, ONLY on dev clusters
- The scripts *must* be run from the `infra/<ENV>` directory to pick up certain environment variables
- Running the `1-update-eni-config.sh` script is mandatory, failure to run it could result in running out of IP addresses in the subnet
- When you run `1-update-eni-config.sh`, a new KUBECONFIG file is created if it doesn't exist, or updated if it already exists, and the current kube context is updated to the newly created cluster 
