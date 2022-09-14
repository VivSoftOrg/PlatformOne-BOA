#!/usr/bin/env bash

set -e

# usage: ./2-deploy.sh env
ENV_DIR="$1"

# Verifies target env matches env currently logged into and the current
# kubernetes context is pointed at the expected cluster
$(dirname "$0")/../../helpers/check_aws_env.sh "$0" "$ENV_DIR"

cd "$(dirname "$0")/envs/${ENV_DIR}"

# fn to create prerequisite namespace and artifactory registry secret
create_ns_and_registry_secret() {
  kubectl create ns "$1" --dry-run=client -o yaml | kubectl apply -f -
  if kubectl get secret private-registry -n "$1" 2> /dev/null; then
    kubectl delete secret private-registry -n "$1"
  fi
  kubectl create secret docker-registry private-registry -n "$1" \
     --docker-server=artifactory.cloud.cms.gov \
     --docker-username="${ARTIFACTORY_USER}" \
     --docker-password="${ARTIFACTORY_PASS}" \
     --docker-email=batcave@internal.cms.gov || true
}

ARTIFACTORY_USER="$(aws secretsmanager get-secret-value --secret-id artifact_repo_service_name_ro --query SecretString --output text)"
ARTIFACTORY_PASS="$(aws secretsmanager get-secret-value --secret-id artifact_repo_service_pass_ro --query SecretString --output text)"

# Deploy flux and wait for it to be ready
echo "Installing Flux"
flux check --pre
create_ns_and_registry_secret flux-system
kustomize build ../../base/flux/ | kubectl apply -f -
flux check

# create git repository credentials
if kubectl get secret gh-credentials -n batcave 2> /dev/null; then
  kubectl delete secret gh-credentials -n batcave
fi
ssh-keyscan github.com > ./known_hosts
aws secretsmanager get-secret-value --secret-id /github/deploy_key/batcave-landing-zone --query SecretString --output text > ./git-repo

kubectl create secret generic gh-credentials -n batcave --from-file=identity=./git-repo --from-file=./known_hosts

rm known_hosts
rm git-repo

# delete default gp2 sc if it exists
if kubectl get sc gp2 2> /dev/null; then
  echo "Deleting gp2 StorageClass"
  kubectl delete sc gp2
fi

# create registry secrets for third-party apps
case $ENV_DIR in
  dev|test|prod|k3d)
    create_ns_and_registry_secret defectdojo
    create_ns_and_registry_secret falco
    create_ns_and_registry_secret rapidfort
  ;;
  impl)
    # defectdojo intentionally not in impl
    create_ns_and_registry_secret falco
    # rapidfort intentionally not in impl
  ;;
esac

# deploy bigbang
kustomize build ./ | kubectl apply -f -
