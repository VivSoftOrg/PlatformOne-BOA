ARG BASE_REGISTRY=registry1.dso.mil
ARG BASE_IMAGE=ironbank/redhat/ubi/ubi8-minimal
ARG BASE_TAG=8.5

FROM tfsec/tfsec-scratch:v0.61.3 AS base

FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}

RUN microdnf update --nodocs && \
  microdnf clean all && \
  rm -rf /var/yum/cache

COPY --from=base /usr/bin/tfsec /usr/bin/tfsec
USER 1000
HEALTHCHECK NONE
ENTRYPOINT ["tfsec"]
