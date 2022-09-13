# Upgrade

## 3.4.0 to  3.5.1

### FluxCD

To upgrade to version 3.5.1 via Flux on bigbang, pass the flag `--set gatekeeper.flux.upgrade.crds=CreateReplace` to your bigbang helm upgrade command. For example;

```bash
helm upgrade ... --set gatekeeper.flux.upgrade.crds=CreateReplace
```

### Helm

For standalone helm upgrade, you will need to upgrade the CRDs with kubectl before doing helm upgrade.

```
kubectl apply -f chart/crds
```

