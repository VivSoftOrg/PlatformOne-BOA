ARG BASE_REGISTRY=registry1.dso.mil
ARG BASE_IMAGE=ironbank/opensource/nginx/nginx
ARG BASE_TAG=1.21.6

FROM public.ecr.aws/b6r5a2q9/enbuild/frontend:0.0.1 as builder

FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}

USER root
# remove the default config file that listens on port 80
RUN rm -rf  /etc/nginx/html/
# 998 is the user id of nginx user
USER 998

COPY --from=builder /etc/nginx/html/ /etc/nginx/html

HEALTHCHECK --interval=10s --timeout=5s --start-period=1m --retries=5 CMD curl -I -f --max-time 5 http://localhost:8080 || curl -fsk https://localhost:8443 || exit 1

STOPSIGNAL SIGQUIT

CMD ["nginx", "-g", "daemon off;"]
