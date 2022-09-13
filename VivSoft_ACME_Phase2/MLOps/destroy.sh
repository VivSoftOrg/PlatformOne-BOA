#!/usr/bin/env bash

set -eu -o pipefail

kubectl get ns
status=$?
if [ $status != 0 ] ; then 
  echo "Can not connect to Cluster"
  exit 1
fi

# destroy kubeflow
kustomize build . | kubectl delete -f - 
kubectl get ns
# kubeflow delete kubeflow-user-example-com

