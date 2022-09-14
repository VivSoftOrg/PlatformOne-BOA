#!/bin/bash

echo "Suspending BigBang.."
flux suspend hr -n bigbang bigbang

printf "Type 'yes' when you've merged your MR: "
read MERGED

if [[ "$MERGED" == "yes" ]]; then
    echo "Reconciling 'this' source.."
    flux reconcile source git -n bigbang this
    sleep 3
    echo "Suspending configs/secrets kustomizations.."
    flux suspend kustomization -n bigbang configs && flux suspend kustomization -n bigbang secrets
    sleep 3
    echo "Resuming configs/secrets kustomizations.."
    flux resume kustomization -n bigbang configs && flux resume kustomization -n bigbang secrets

    echo "Waiting for istio-secret to exist in bigbang namespace.."
      printf "Waiting.."
    while kubectl get secrets -n bigbang istio-secret >/dev/null 2>1 ; ret=$? ; [ $ret -ne 0 ];do
        printf "."
        sleep 3
    done

    echo "Reconciling BigBang.."
    flux suspend hr -n bigbang bigbang && flux resume hr -n bigbang bigbang

    echo ""
    echo "Done!"
    sleep 1
    echo "Watching helm release status..."
    watch flux get hr -n bigbang
    exit 0
fi
