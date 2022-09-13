FROM registry.gitlab.com/enbuild-staging/container_registry/nodejs/nodejs16:17.0.1 as builder

WORKDIR /build
COPY --chown=node:node package.json .
COPY --chown=node:node package-lock.json .

RUN chown -Rh $user:$user /build
USER $user

RUN npm ci
COPY --chown=node:node . .
RUN npm run build


FROM registry.gitlab.com/enbuild-staging/container_registry/nginx/nginx:1.21.4

USER root
# remove the default config file that listens on port 80
RUN rm -rf /etc/nginx/conf.d/default.conf /etc/nginx/html/
# 998 is the user id of nginx user
USER 998
COPY --from=builder /build/build/ /etc/nginx/html/
# This doc folder is copied from backend to frontend in ci before docker build.

