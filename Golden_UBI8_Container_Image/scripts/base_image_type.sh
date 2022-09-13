#!/bin/bash
set -Eeuo pipefail
podman pull "registry.gitlab.com/atom-container-hardening/rhel-ubi-baseline-image/ubi8:latest"
DOCKER_IMAGE_PATH=$(podman images --noheading | awk '{print $3}')
export DOCKER_IMAGE_PATH
BASE_IMAGE_TYPE=$(podman inspect -f '{{index .Labels "com.redhat.component"}}' "${DOCKER_IMAGE_PATH}")
if [[ "${BASE_IMAGE_TYPE}" == "" ]]; then
  BASE_IMAGE_TYPE=$(podman inspect -f '{{index .Labels "mil.dso.ironbank.os-type"}}' "${DOCKER_IMAGE_PATH}")
  if [[ "${BASE_IMAGE_TYPE}" == "" ]]; then
    labels=$(podman inspect -f '{{index .Labels}}' "${DOCKER_IMAGE_PATH}")
    echo "Unknown image type. Can't choose security guide. labels: ${labels}"
    exit 1
  fi
fi

echo "Base Image Type: ${BASE_IMAGE_TYPE}"

export BASE_IMAGE_TYPE
