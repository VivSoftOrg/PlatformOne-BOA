# Swiss Knife - Sofware Development BOA Support Area

Deploy a multi-node k8s cluster on an AWS EC2 instance using terraform, ansible, and k3d; primarily for deploying the bigbang baseline.

# Requirements

## Supported Systems

Other systems may be used, but documentation is written for the following:
* MacOS

## Install Packages

Install the required packages (MacOS):

```
brew install awscli terraform ansible kubectl
```

If you are planning on building the required k3d AMI

```
brew install packer
```

## AWS Configuration

**Note**: You will need to obtain access to a supported AWS account and region to use this project.

All required AWS resources are stored in the BigBang AWS account, and shared to several other supported accounts and regions.

Using unlisted AWS accounts or regions is currently not supported.

Only the following AWS account IDs are supported:
* `373346310182` (batcave-dev)

Only the following AWS regions are supported:
* `us-east-1`

Configure your AWS credentials and region:
* Make sure this region equals the `aws_region` variable.

```
aws configure
```

## SSH Key

Make sure to generate an SSH key:
* If you use something other than `<home_full_path>/.ssh/id_rsa`, make sure to update the `private_key_path` and the `public_key_path` variables.

```
ssh-keygen
```

## Variable File Configuration

Set up (and optionally modify) your `terraform.tfvars.json` file:

```
cp terraform.tfvars.json.example terraform.tfvars.json
```

## EC2 Instance Name

* Open variables.tf
* Change the default tag under "aws_tag_name" to change your instance name of the EC2

# Initialization

## If you plan on making k3d infra modifications, follow here, if not move to next heading

Check out the latest stable release into a unique local dev branch you own:

```
release=$(git describe --match "release-v*" --abbrev=0 --tags master)
git fetch --tags origin
git checkout tags/$release -b <your_local_dev_branch_name>
git reset --hard $release
```

If you already have a unique local dev branch, bring in the latest release changes:

```
git fetch --all
release=$(git describe --match "release-v*" --abbrev=0 --tags master)
git checkout <your_local_dev_branch_name>
git merge $release
```

## Initialize terraform module

Initialize the terraform module, this only needs to be done once:

```
terraform init
```

# Variables / Customization

All custom variables must be defined in the `terraform.tfvars.json` file.

This file must exist, and is the only tfvars file type allowed.

**No other method of passing variables is supported.**

This is due to limitations with passing terraform variables to ansible.

# Running

Steps that will be done after application:
* A security group will be created that only allows your IP ingress.
* Your SSH key will be created and linked as a new AWS keypair.
* An EC2 instance is spawned from the `k3d-dev-env` AMI.
* A k3d cluster will be created according to set requirements.
* (Optional) Your local kubeconfig file will be overwritten.
* Output information will be populated for debugging use.

Plan the terraform module:

```
terraform plan
```

Apply the terraform module:

```
terraform apply
```

# Grabbing kubeconfig

Several methods of grabbing the kubeconfig exist, the easiest is to scp it

This method replaces your kubeconfig, if you want to add it to an existing kubeconfig, use the [KUBECONFIG](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/#set-the-kubeconfig-environment-variable) variable

```
scp -i $(terraform output -raw private_key_path) $(terraform output -raw ami_user)@$(terraform output -raw instance_ip):.kube/config config
sed -i '' "s|0.0.0.0|$(terraform output -raw instance_ip)|g" config
mv config ~/.kube/
```

# Proxying

Several methods of ingress proxying can be used, here is one example:

```
ssh -i $(terraform output -raw private_key_path) $(terraform output -raw ami_user)@$(terraform output -raw instance_ip)
```

# Verifying

Check to see if your cluster is up and running:

```
kubectl get nodes -o wide
```

# Destroying

Please make sure to destroy your resources when not in use:

```
terraform destroy --auto-approve
```

# Packer

If you want to build the k3d AMI image, follow the README in the `packer` directory

# **** DEPRECATED NOTES BELOW ****

# Other Notes

* The VPC / security group is tied to your local client public IP address, only this IP address will have access to the created infrastructure. If you need to open this up, do so using the AWS web management console or the AWS command line tool.
* Each AWS resource is tagged with a name and an owner, this allows you to more easily search for the infrastructure in the AWS console for debugging; the owner tag will be the top-level username retrieved from the configured AWS credentials.
* Check to make sure you're not connected to a VPN, and that your local firewall filter is not causing issues. Both of these may conflict with some of the AWS resources, and are hard to debug. If possible, disconnect from your VPN and disable your firewall filter.

# Cheat Sheet

Additionally, you can also generate an `/etc/hosts` entry with all virtual service gateways in your cluster:

```
echo "$(terraform output instance_ip) $(kubectl get vs -A -o json | jq -r '[.items[] | .spec.hosts[]] | join (" ")')"
```

The output should be similar to this:

```
111.1.111.111 jaeger.bigbang.dev kiali.bigbang.dev grafana.bigbang.dev prometheus.bigbang.dev alertmanager.bigbang.dev twistlock.bigbang.dev
```

If you use other clusters, leverage the `KUBECONFIG` environment variable along with the `kubeconfig_path` terraform variable.

```
export KUBECONFIG="<home_full_path>/.kube/config:<home_full_path>/.kube/k3d-dev-env
```

# Notable Features

## Airgap Support

Test airgap capability is available by using the following variables:

* `k3d_upload_images` - Optionally load images from tar into k3d cluster
* `k3d_images_tarball` - Local path to the images tarball (tar.gz) to load into k3d
* `aws_airgap` - Optionally disallow any egress except to the client machine

Combining these variables allows you to test an airgap deployment of an application using a previously generated tarball of container images.

To generate this tarball, leverage the `hack/bundle_images.sh` script.

Also provided are `hack/k8s_dashboard_images.txt` and `hack/k8s_dashboard.yaml`, these files can be used to test an example deployment of the Kubernetes Dashboard in an airgapped enviornment.

An example tarball generation using this image list would be:

```
./hack/bundle_images.sh --image-list hack/k8s_dashboard_images.txt --images hack/images.tar.gz
```

With the additional variable settings in `terraform.tfvars.json` of:

```
{
    ...
    "k3d_upload_images": true,
    "k3d_images_tarball": "<project_full_path>/hack/images.tar.gz",
    "aws_airgap": true,
    ...
}
```

All images provided in the tarball are loaded before cluster creation into each node, and all baseline images required by k3d / k3s are already loaded into the cluster (regardless of airgap variable settings), so there is no need to specify any k3d / k3s cluster specific container images.

# Contributing

Additional documentation can be found in several README files throughout the repository.

These files are meant to assist baseline development for this module and its components.

If you would like to request a feature or report a bug, please [open a GitLab issue](https://repo1.dso.mil/platform-one/big-bang/terraform-modules/k3d-dev-env/-/issues).

If you would like to submit a merge request, refer to the [contributor documentation](./CONTRIBUTING.md) for more information.
