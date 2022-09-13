# Developer guide

### Dev cluster setup

Using k3d (https://k3d.io/) start a dev cluster on your local machine.

```
k3d cluster create --k3s-server-arg "--disable=traefik" --k3s-server-arg "--disable=metrics-server" -p 80:80@loadbalancer -p 443:443@loadbalancer -s 1 -a 3 -v ~/.k3d/p1-registry.yaml:/etc/rancher/k3s/registries.yaml
```

You will need a file located at: ~/.k3d/p1-registry.yaml  An example of that file is given here. This provides pull access to the repo 1 images that are used from Iron Bank.

```
configs:
  "registry1.dso.mil":
    auth:
      username: "<repo 1 user>"
      password: <repo 1 token>
```
Install the local chart

```
# Clone the repo
git clone https://repo1.dso.mil/platform-one/big-bang/apps/core/eck-operator.git

# The first time that you install the charts, you will need to update the dependencies
cd eck-operator/chart && helm dependency update && cd ..

# Install the chart (be sure to add a namespace to it if you don't want it in default)
helm install eck-operator chart 

# Check to see if it is up
watch kubectl get all -A
```
