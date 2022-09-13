#!/usr/bin/env bash

set -eu -o pipefail

kubectl get ns
status=$?
if [ $status != 0 ] ; then 
  echo "Can not connect to Cluster"
  exit 1
fi

# install kubeflow

while ! kustomize build . | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done

SERVICE_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[*].ip}')

echo "The kubeflow will be available at https://$SERVICE_IP"
USER="kubeflow@vivsoft.io"
PASSWORD='Viv$0ft'
echo "The user-name is $USER and password is $PASSWORD"

