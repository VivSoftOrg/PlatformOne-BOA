// Set the cluster name either cli parameter -t cluster_name=foo or default
_cluster_name: *"batcave-test" | string @tag(cluster_name)

// Define a gatus querystring for all endpoints (for easy log identification)
_gatus_querystring: "healthcheck=gatus.\(_cluster_name).internal.cms.gov"

_utility_belt_envs: [
  {
    name: _cluster_name
    base_url: "\(_cluster_name).internal.cms.gov"
  },
]
_utility_belt_apps: [
  {
    name: "ArgoCD"
    app_url: "argocd"
  },
  {
    name: "Kiali"
    app_url: "kiali"
  },
  {
    name: "Grafana"
    app_url: "grafana"
  },
  {
    name: "Alert Manager"
    app_url: "alertmanager"
  },
  {
    name: "Jaeger"
    app_url: "tracing"
  },
  {
    name: "DefectDojo"
    app_url: "defectdojo"
  },
  {
    name: "GitLab"
    app_url: "code"
  },
  {
    name: "RapidFort"
    app_url: "rapidfort"
  },
]
_utility_belt_sites: [
  for env in _utility_belt_envs
    for app in _utility_belt_apps {
      name: app.name
      group: "\(env.name) Utility Belt"
      url: "https://\(app.app_url).\(env.base_url)"
      interval: *(env.interval&string) | null
    }
]
_one_off_sites: [
  {
    name: "batCAVE GitLab"
    group: "External Dependencies"
    url: "https://code.batcave.internal.cms.gov/explore"
  },
  {
    name: "CMS Artifactory"
    group: "External Dependencies"
    url: "https://artifactory.cloud.cms.gov/"
  },
  {
    name: "GitHub"
    group: "External Dependencies"
    url: "https://www.github.com/"
  },
]
client: {
  "ignore-redirect": true
  timeout: "5s"
}
endpoints: [
  for site in _utility_belt_sites + _one_off_sites {
    name: site.name
    group: site.group
    url: "\(site.url)?\(_gatus_querystring)"
    interval: *(site.interval&string) | "5m"
    client: {
      "ignore-redirect": true
      timeout: *(site.timeout&string) | "5s"
    }
    conditions: [
      "[STATUS] < 400",
      "[RESPONSE_TIME] < \( *(site.response_time&string) | "2s")",
      "[CERTIFICATE_EXPIRATION] > 1d",
      "[CERTIFICATE_EXPIRATION] > 30d",
    ]
  }
]
