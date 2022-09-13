// Generate a URL suffix for dev environment, if -t cluster_name=foo is provided
_cluster_name: *"" | string @tag(cluster_name)
_url_suffix: [
  if _cluster_name == "" {""},
  "-\(_cluster_name)"
][0]

_utility_belt_envs: [
  {
    name: "bat-dev"
    base_url: "batcave-dev.internal.cms.gov"
  },
]
_utility_belt_apps: [
  {
    name: "ArgoCD"
    app_url: "argocd\(_url_suffix)"
  },
  {
    name: "Kiali"
    app_url: "kiali\(_url_suffix)"
  },
  {
    name: "Grafana"
    app_url: "grafana\(_url_suffix)"
  },
  {
    name: "Alert Manager"
    app_url: "alertmanager\(_url_suffix)"
  },
  {
    name: "Jaeger"
    app_url: "tracing\(_url_suffix)"
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
    name: "GitLab"
    group: "bat-prod Shared Services"
    url: "https://code.batcave.internal.cms.gov/explore"
  },
  {
    name: "GitLab"
    group: "bat-test Shared Services"
    url: "https://code.batcave-test.internal.cms.gov/explore"
  },
  {
    name: "batCAVE Status"
    group: "bat-prod Shared Services"
    url: "https://status.batcave.internal.cms.gov/api/v1/services"
    timeout: "15s"
    response_time: "10s"
  },
  {
    name: "DefectDojo"
    group: "bat-prod Shared Services"
    url: "https://defectdojo.batcave.internal.cms.gov/explore"
  },
  {
    name: "DefectDojo"
    group: "bat-test Shared Services"
    url: "https://defectdojo.batcave-test.internal.cms.gov/explore"
  },
  {
    name: "CMS Artifactory"
    group: "CMS Dependencies"
    url: "https://artifactory.cloud.cms.gov/"
  },
  //{
  //  name: "CMS CloudTamer"
  //  group: "CMS Dependencies"
  //  url: "https://cloudtamer.cms.gov/"
  //},
  {
    name: "GitHub"
    group: "CMS Dependencies"
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
    url: site.url
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
