# About the K3D Environment

Deploying BatCAVE into K3D requires some slight deviation from how we deploy into a development environment. This environment inherits from and patches the dev environment.

## Persistent Volume Claims

Our K3D deployment does not support the `ebs` or `ebs-immediate` StorageClass, so any PersistentVolumeClaims that would normally use those must be modified to use `local-path` which will store the persistent volume data on the EC2 instance boot volume.

## Terragrunt Vars Config Map

Information about your environment such as the name of the cluster and the S3 bucket locations to use for various application is stored in the `terragrunt-vars` ConfigMap. This ConfigMap should automatically be created when  you create the K3D deployment.

# Instructions

Once you have created a K3D cluster in AWS using the [k3d-dev-env repository](https://code.batcave.internal.cms.gov/batcave-iac/k3d-dev-env#k3d-dev-env), the next step is to install BatCAVE.

## [Optional] Create a Branch for your Changes

Because helm chart configuration is synchronized with Git via Flux, if you want to customize elements of this configuration, it is necessary to create a branch to house your changes and to point Flux at that branch. To do so create a branch and modify the GitRepository manifest in [`batcave-landing-zone.yaml`](../dev/batcave-landing-zone.yaml) to specify your branch as the target ref:

```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: batcave-landing-zone
  namespace: batcave
spec:
  interval: 1m0s
  url: ssh://git@github.com/CMSgov/batcave-landing-zone.git
  ref:
    branch: <YOUR-BRANCH-NAME-HERE>
```

## Run `2-deploy.sh`

_When deploying BatCAVE into a K3D cluster it is not necessary to run `1-update-eni-config.sh`, which deals with [EKS](https://aws.amazon.com/eks/) specific network configuration._

When running `2-deploy.sh` be sure that your `AWS_PROFILE` environment variable is set to point at the `batcave-dev` environment, and your current kubectl context is set to your K3D cluster (check this by running `kubectl config current-context`).

```bash
./2-deploy.sh k3d
```

The `2-deploy.sh` script will create prerequisite namespaces and secrets, and run `kustomize build` in the `envs/k3d` folder and create the resulting resources in your K3d cluster.

## Accessing Services

BatCAVE services running in your K3D cluster will be available via port 80 & 443 via the private IP of your EC2 instance. To get this IP you can run `terraform output` from the `k3d-dev-env` repository folder. In order to be able to access services via your web browser you will need to follow these steps:

### Add `/etc/hosts` File Entries

Add entries like the following to your `/etc/hosts` file, replacing `10.202.x.x` with the IP address of your instance.

```
10.202.x.x grafana-<your-cluster-name>.batcave-dev.internal.cms.gov
10.202.x.x argocd-<your-cluster-name>.batcave-dev.internal.cms.gov
10.202.x.x kiali-<your-cluster-name>.batcave-dev.internal.cms.gov
10.202.x.x tracing-<your-cluster-name>.batcave-dev.internal.cms.gov
10.202.x.x alertmanager-<your-cluster-name>.batcave-dev.internal.cms.gov
```

### Trust the Self-Signed Istio Certificate

How to trust this certificate will depend on your operating system.

#### Mac OS

 * Save the public certificate to a file (this assumes you have set up your `/etc/hosts` file entries:
```bash
# Save the SSL certificate to a file: batcave-dev.cer
openssl s_client -connect grafana.batcave-dev.internal.cms.gov:443 -showcerts < /dev/null 2> /dev/null | openssl x509 > batcave-dev.cer
```
 * Open the "Keychain Access app" and install the certificate into your "login" Keychain by dragging and dropping.
 * Open the certificate, expand the "Trust" section, and change the "When using the certificate" dropdown to "Always Trust"

#### Windows

[Instructions for Windows](https://techcommunity.microsoft.com/t5/windows-server-essentials-and/installing-a-self-signed-certificate-as-a-trusted-root-ca-in/ba-p/396105)