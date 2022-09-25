#!/bin/bash -e
echo "Creating snakeoil key/cert..."
openssl req -quiet -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 1 -subj '/CN=selfsigned' -nodes
echo "Generating istio-secret.dec.yaml..."
cat << EOF > istio-secret.dec.yaml
apiVersion: v1
kind: Secret
metadata:
  name: istio-secret
  namespace: batcave
stringData:
  values.yaml: |-
    istio:
      gateways:
        main:
          tls:
            key: "$(cat key.pem | tr '\n' '\`' | sed 's/`/\\n/g')"
            cert: "$(cat cert.pem | tr '\n' '\`' | sed 's/`/\\n/g')"
EOF
echo "Done.  Copy istio-secret.dec.yaml into the appropriate secret dir and encrypt with sops."
