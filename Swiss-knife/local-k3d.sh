#!/bin/bash

set -e

k3d-create() {
  k3d cluster create a-lab \
    --servers 1 \
    --agents 3 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /var/lib/docker:/var/lib/docker \
    --port 80:80@loadbalancer \
    --port 443:443@loadbalancer \
    --api-port 6443 \
    --k3s-arg "--disable=traefik@server:0" \
    --kubeconfig-update-default \
    --registry-config "./registry/registry.yaml"
}

k3d-destroy() {
  k3d cluster delete a-lab
}

istio-create() {
  kubectl create ns istio-system --dry-run=true -o yaml | kubectl apply -f -
  kubectl apply -f istio/manifest.yaml
  kustomize build certificates | kubectl apply -f -
  kustomize build istio-bells | kubectl apply -f - 
}

logging-create() {
  kubectl create ns logging &&
  helm repo add grafana https://grafana.github.io/helm-charts &&
  helm repo update &&
  helm upgrade --install loki --namespace=logging grafana/loki  --set fluent-bit.enabled=true,promtail.enabled=false &&
  helm upgrade --install fluent-bit --namespace=logging grafana/fluent-bit --set loki.serviceName=loki.logging.svc.cluster.local
}

opa-create() {
  helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts &&
  helm repo update &&
  helm install gatekeeper/gatekeeper --name-template=gatekeeper --namespace gatekeeper-system --create-namespace
}

monitoring-create() {
  #istio-create
  kubectl create -f ../monitoring/kube-prometheus/manifests/setup &&
  kubectl create -f ../monitoring/kube-prometheus/manifests/ &&
  kustomize build ../monitoring/support | kubectl apply -f -
}

create_certs() {
  kubectl create secret tls test-tls --key="privkey.pem" --cert="fullchain.pem" -n istio-system
}

argo-create() {
  #istio-create
  kustomize build ../argocd/ | kubectl apply -f -
}

echo_app() {
  kustomize build echo-server/ | kubectl apply -f -
}

deploy_bookapp() {
  kustomize build book-info/ | kubectl apply -f -
}

update_hosts() {
  sudo txeh add 127.0.0.1 test.thisiza.com
}

download_istio() {
  curl -L https://istio.io/downloadIstio | sh -
}

vault-create() {
  kubectl create namespace vault &&
  helm install vault hashicorp/vault --namespace vault --version 0.5.0 &&
  kubectl apply -f ../vault/vault-vs.yaml
  sleep 30 &&
  kubectl exec vault-0 -n vault -- vault operator init -key-shares=1 -key-threshold=1 -format=json > cluster-keys.json &&
  kubectl exec vault-0 -n vault -- vault operator unseal $(cat cluster-keys.json | jq -r ".unseal_keys_b64[]") &&
  kubectl create secret -n vault generic root-token --from-literal=token=$(cat cluster-keys.json | jq -r ".root_token") 
}

vault-destroy() {
  kubectl delete ns vault
}

kc-create() {
  istio-create
  kustomize build ../keycloak/support/ | kubectl apply -f - &&
  helm upgrade keycloak ../keycloak/keycloak/ -n keycloak
}

kc-destroy() {
  kubectl delete ns keycloak
}

$1