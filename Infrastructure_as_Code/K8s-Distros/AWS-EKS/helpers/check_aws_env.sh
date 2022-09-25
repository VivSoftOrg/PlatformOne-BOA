#!/usr/bin/env bash

set -e

########### Passed in Arguments ###########################
# Expected usage is to call this script from other scripts
# where the caller scripts is 1st arg and env requested is
# the second arg.  If this script is called directly then
# the first arg would be the env requested.
if [ $# -eq 2 ]; then
  CALLER_NAME="$1"
  REQUESTED_ENV="$2"
elif [ $# -eq 1 ]; then
  CALLER_NAME="<script.sh>"
  REQUESTED_ENV="$1"
else
  CALLER_NAME="<script.sh>"
  REQUESTED_ENV=""
fi

check_cluster_set() {
  if [[ -z "$CLUSTER_NAME" ]]; then
    echo "[!] No CLUSTER_NAME shell environment variable, exiting!" >&2
    echo ""
    echo "    CLUSTER_NAME needs set when using dev or k3d environments."
    echo "    Recommend using .envrc to configured 'export CLUSTER_NAME=yourcluster'"
    echo ""
    echo "    Dependency for following command:"
    echo '    aws eks update-kubeconfig --name "$CLUSTER_NAME" --region us-east-1'
    echo ""
    exit 1
  fi
}

# TODO: Does not support k3d in ADO environments
case $REQUESTED_ENV in
  dev)
    check_cluster_set
    EXPECTED_CLUSTER="$CLUSTER_NAME"
    EXPECTED_STACK="batcave-$REQUESTED_ENV"
  ;;
  test|impl|prod)
    EXPECTED_CLUSTER="batcave-$REQUESTED_ENV"
    EXPECTED_STACK="batcave-$REQUESTED_ENV"
  ;;
  k3d)
    check_cluster_set
    EXPECTED_STACK="batcave-dev"
    EXPECTED_CLUSTER="$CLUSTER_NAME"
  ;;
  *)
    # default to the cluster name matching the folder name
    EXPECTED_CLUSTER="$REQUESTED_ENV"
    EXPECTED_STACK="$REQUESTED_ENV"
  ;;
esac

########### AWS Login State Values ########################
# Very important to verify the correct envinronment, especially for a production 
# environment.  The following commands query the current environment information 
# from different sources of information.

# Get current logged in AWS Account ID
CURRENT_AWSID="$(aws sts get-caller-identity --query Account --output text)"

# Get current logged in AWS environment parameters
CURRENT_AWS_VPC_ENV="$(aws ec2 describe-vpcs --query 'Vpcs[].Tags[?Key==`Name`][].Value' --output text | sed 's/east-//')"

# Get Kubernetes context
KUBE_CONTEXT="$(kubectl config current-context 2> /dev/null || echo '')"
if [[ "$KUBE_CONTEXT" == "" ]]; then
  echo "Unable to get the current kubectl context."
  echo "Check that ${KUBECONFIG:-~/.kube/config} exists, and has a current context specified."
  echo 'You may need to run: aws eks update-kubeconfig --name $CLUSTER_NAME --region us-east-1'
  exit 1
fi
IFS='/' read -ra KUBE_CONTEXT_PARTS <<< "$KUBE_CONTEXT"
CLUSTER="${KUBE_CONTEXT_PARTS[$((${#KUBE_CONTEXT_PARTS[@]}-1))]}"

syntax() {
  echo ""
  echo "    Syntax:"
  echo "    ${CALLER_NAME} <environment>"
}

########### Display Current Environment ###################
echo ""
echo "[*] Current Environment:"
echo "    Requested Environment:    $REQUESTED_ENV"
echo "    AWS Account ID:           $CURRENT_AWSID"
echo "    Expected AWS Env:         $EXPECTED_STACK"
echo "    AWS EC2 VPC Env:          $CURRENT_AWS_VPC_ENV"
echo "    Expected Cluster:         $EXPECTED_CLUSTER"
echo "    Kubectl Cluster:          $CLUSTER"
echo ""

########### Check Script Arguments ########################
# When a desired script calls this function and passes in an argument 
# for the desired aws environment it wishes to execute against. This option
# is expected when running the 1-update-eni-config.sh and 2-deploy.sh with passing an
# argument from the .../batcave-landing-zone/apps/batcave/, for example
# `1-update-eni-config.sh dev`
if [[ -z $REQUESTED_ENV ]]; then
  # Check that one of the appropriate environments is passed in as an argument. 
  # NOTE! this listed will need to be updated as new environments are supported.
  echo "[!] Missing environment argument, exiting!" >&2
  syntax >&2
  echo ""
  exit 1
fi

########### Check Login & Requested Env ###################
if [[ "$EXPECTED_STACK" != "$CURRENT_AWS_VPC_ENV" ]]; then
  echo "[!] AWS login and requested environment mismatch, exiting!" >&2
  echo ""
  exit 1
fi


########### Check Kubernetes Cluster ######################
if [ "$CLUSTER" != "$EXPECTED_CLUSTER" ]; then
  echo "[!] Current kubernetes cluster \"$CLUSTER\" does not match the expected target: \"$EXPECTED_CLUSTER\""
  echo ""
  exit 1
fi

########### All Parameters Checkout #######################
echo "[x] All parameters check out."
echo ""
if [ $CALLER_NAME != "<script.sh>" ]; then
  echo "You are about to run $CALLER_NAME for the \"$REQUESTED_ENV\" environment on the \"$CLUSTER\" k8s cluster in the \"$EXPECTED_STACK\" account."
  while true; do
    read -p "[?] Do you wish proceed? (y/n)  " yn
    case $yn in
      [Yy]* ) break;;
      [Nn]* ) exit 1;;
      * ) echo "[!] Please answer yes or no.";;
    esac
  done
  echo "[x] Continuing Execution."
  echo ""
fi

exit 0
