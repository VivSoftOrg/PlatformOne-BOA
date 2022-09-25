#!/usr/bin/env bash

set -e

# Verifies target env matches env currently logged into and the current
# kubernetes context is pointed at the expected cluster
$(dirname "$0")/../../helpers/check_aws_env.sh "$0" "$1"

ENV_DIR="$1"

# Sets cluster name for the requested environment otherwise
# EXPECTED_CLUSTER will use your CLUSTER_NAME for dev and k3d
case $ENV_DIR in
  dev|k3d)
    EXPECTED_CLUSTER="$CLUSTER_NAME"
  ;;
  test|impl|prod)
    EXPECTED_CLUSTER="batcave-$ENV_DIR"
  ;;
  *)
    # default to the cluster name matching the folder name
    EXPECTED_CLUSTER="$ENV_DIR"
  ;;
esac

# update the cluster config
aws eks update-kubeconfig --name "$EXPECTED_CLUSTER" --region us-east-1

cd "$(dirname "$0")/envs/${ENV_DIR}"

INFRA_DIR="../../../../infra/${ENV_DIR}"

echo "Checking if K8s nodes are ready"
if ! kubectl wait --for=condition=ready --timeout 300s nodes --all; then
  echo "Timed out waiting for nodes to become ready"
  exit 1
fi

# Updating cluster to use container subnets
kubectl set env daemonset aws-node -n kube-system AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true
kubectl set env daemonset aws-node -n kube-system ENI_CONFIG_LABEL_DEF=failure-domain.beta.kubernetes.io/zone
kubectl apply -f ../../base/eni-crd.yaml

# Clean terragrunt cache and re-init needed subdirs
find ${INFRA_DIR}/ -type d -name ".terragrunt-cache" -prune -exec rm -rf {} \;
find ${INFRA_DIR}/ -name ".terraform*" -prune -exec rm -rf {} \;
terragrunt init --terragrunt-working-dir ${INFRA_DIR}/eks-cluster
terragrunt init --terragrunt-working-dir ${INFRA_DIR}/vpc

# Fetch node security group
echo "Fetching eks node security group id..."
node_sg="$(terragrunt output --terragrunt-log-level error --terragrunt-no-auto-init --terragrunt-working-dir ${INFRA_DIR}/eks-cluster -json worker_security_group_id)"

# Fetch az to subnet map
echo "Fetching az to subnet map..."
subnet_azs_to_id="$(terragrunt output --terragrunt-log-level error --terragrunt-no-auto-init --terragrunt-working-dir ${INFRA_DIR}/vpc -json subnets | jq '.["container"]["azs_to_id"]')"

function create_eni_by_subnet_az(){
  subnet_az=${1}
  subnet_id=${2}
  cat <<EOF | kubectl apply -f -
apiVersion: crd.k8s.amazonaws.com/v1alpha1
kind: ENIConfig
metadata:
 name: ${subnet_az}
spec:
 subnet: "${subnet_id}"
 securityGroups:
  - ${node_sg}
EOF
}

# Create ENI resources
echo "Creating ENI resources..."
create_eni_by_subnet_az us-east-1a "$(echo $subnet_azs_to_id | jq -r '.["us-east-1a"]')"
create_eni_by_subnet_az us-east-1b "$(echo $subnet_azs_to_id | jq -r '.["us-east-1b"]')"
create_eni_by_subnet_az us-east-1c "$(echo $subnet_azs_to_id | jq -r '.["us-east-1c"]')"

# Fetch self-managed node group names
echo "Fetching self-managed node group names..."
self_managed_node_groups="$(terragrunt output --terragrunt-log-level error --terragrunt-no-auto-init --terragrunt-working-dir ${INFRA_DIR}/eks-cluster -json self_managed_node_groups | jq -r '. | keys | .[]')"
echo "Found:"
echo "$self_managed_node_groups"

# Terminating instances to load new eni config
for node_group_name in $self_managed_node_groups; do
  if [ -z "$(aws ec2 describe-instances --filter "Name=tag:Name,Values=$EXPECTED_CLUSTER-${node_group_name}" "Name=instance-state-name,Values=running" --query "Reservations[].Instances[].[InstanceId]" --output text)" ]; then
    echo "No ${node_group_name} node pool instances found"
  else
    echo "Terminating ${node_group_name} node pool instances"
    aws ec2 terminate-instances --instance-ids "$(aws ec2 describe-instances --filter "Name=tag:Name,Values=$EXPECTED_CLUSTER-${node_group_name}" "Name=instance-state-name,Values=running" --query "Reservations[].Instances[].[InstanceId]" --output text)" --output text
  fi
done

SLEEP_SECONDS=300
echo "Waiting ${SLEEP_SECONDS} seconds for instances to terminate..."
sleep ${SLEEP_SECONDS}

echo "Checking if K8s nodes are ready"
if ! kubectl wait --for=condition=ready --timeout 300s nodes --all; then
  echo "Timed out waiting for nodes to become ready"
  exit 1
fi
