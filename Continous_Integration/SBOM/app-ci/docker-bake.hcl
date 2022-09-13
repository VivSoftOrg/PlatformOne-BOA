variable "CI_REGISTRY_IMAGE" {}

variable "CI_COMMIT_SHA" {}

variable "CI_COMMIT_TIMESTAMP" {}

variable "CI_PROJECT_URL" {}

variable "CI_PROJECT_TITLE" {}

group "sample-app" {
    targets = [
        "react-js-sample-app"
    ]
}

target "react-js-sample-app" {
  pull       = true
  context    = "react-js-sample-app"
  dockerfile = "Dockerfile"
  tags       = ["${CI_REGISTRY_IMAGE}/react-js-sample-app:${CI_COMMIT_SHA}"]
  cache-from = ["type=registry,ref=${CI_REGISTRY_IMAGE}:react-js-sample-app-cache"]
  cache-to   = ["type=registry,ref=${CI_REGISTRY_IMAGE}:react-js-sample-app-cache,mode=max"]
  platforms  = ["linux/amd64"]
  labels     = {
    "org.opencontainers.image.title": "${CI_PROJECT_TITLE}",
    "org.opencontainers.image.description": "react-js-sample-app",
    "org.opencontainers.image.url": "${CI_PROJECT_URL}",
    "org.opencontainers.image.source": "${CI_PROJECT_URL}",
    "org.opencontainers.image.version": "${CI_COMMIT_SHA}",
    "org.opencontainers.image.created": "${CI_COMMIT_TIMESTAMP}",
    "org.opencontainers.image.revision": "${CI_COMMIT_SHA}",
  }
}
