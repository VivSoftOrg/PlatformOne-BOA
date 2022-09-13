#!/usr/bin/env bash

# This script only needs to be run once in an account after creating a secret to store the secret value
# Run me ./put-secret.sh "https://hooks.slack.com/services/XXXXX/XXXX/XXXXXX"

if [ -z "$1" ]
  then
    echo "No secret argument passed"
    exit 1
fi

echo "Putting secret value"
aws secretsmanager put-secret-value \
    --secret-id slack_webhook_url \
    --secret-string $1
