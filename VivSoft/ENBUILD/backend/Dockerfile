ARG BASE_REGISTRY=registry1.dso.mil
ARG BASE_IMAGE=ironbank/opensource/nodejs/nodejs16
ARG BASE_TAG=16.14.0


FROM public.ecr.aws/b6r5a2q9/enbuild/backend:0.0.1  as builder

FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}

USER root
COPY sops-v3.7.2.linux /usr/local/bin/sops 
RUN chmod +x /usr/local/bin/sops && \
    yum install -y git && \
    yum clean all && \
    rm -rf /var/cache/yum \
           /usr/share/doc/perl-IO-Socket-SSL  \
           /usr/share/doc/perl-Net-SSLeay \
           /usr/libexec/openssh/ssh-keysign


  
USER node
COPY --from=builder /home/node/ .

USER root
RUN rm -rf /home/node/node_modules/nssocket  \
           /home/node/node_modules/proxy-agent \
           /home/node/node_modules/websocket-extensions \
           /home/node/node_modules/glob-parent \
           /home/node/node_modules/node-forge \
           /home/node/node_modules/vm2 \
           /home/node/node_modules/fast-json-patch
           

USER node
EXPOSE  8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=1m --retries=5 CMD curl -I -f --max-time 5 http://localhost:8080 || exit 1

CMD ["npm", "start"]

