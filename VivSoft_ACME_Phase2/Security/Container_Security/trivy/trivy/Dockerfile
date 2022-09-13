ARG BASE_REGISTRY=registry1.dso.mil
ARG BASE_IMAGE=ironbank/redhat/ubi/ubi8-minimal
ARG BASE_TAG=8.5

FROM aquasec/trivy:0.24.2 AS base

FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}

RUN microdnf update --nodocs && \ 
  microdnf install -y --nodocs git shadow-utils findutils && \
  groupadd -r scanner && useradd --no-log-init -r -g scanner scanner && \
  mkdir -p /root/.cache /home/scanner/.cache && \
  chown scanner:scanner /root/.cache && \
  chown scanner:scanner /home/scanner/.cache && \
  find / -path /proc -prune -o -perm /4000 -exec chmod u-s {} \; && \
  find / -path /proc -prune -o -perm /2000 -exec chmod g-s {} \; && \
  microdnf remove libsemanage shadow-utils findutils && \
  microdnf clean all && \
  rm -rf /var/yum/cache

COPY --from=base /usr/local/bin/trivy /usr/bin/trivy
COPY --from=base --chown=scanner:scanner /contrib /contrib
WORKDIR /home/scanner
USER scanner
HEALTHCHECK NONE
ENTRYPOINT ["trivy"]
