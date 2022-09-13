import * as https from 'https'
import middy from '@middy/core'
import errorLogger from '@middy/error-logger'
import httpErrorHandler from "@middy/http-error-handler"
import httpRouterHandler from '@middy/http-router'

const statusMap = {
  // Note: unconventional property name casing is deliberate so that
  // "aggregate_severity" values can also be used as a lookup key.
  Unresponsive: {
    "aggregate_severity": "Unresponsive",
    "aggregate_color": "#B50101",
    "aggregate_value": 0,
  },
  Operational: {
    "aggregate_severity": "Operational",
    "aggregate_color": "#99D18B",
    "aggregate_value": 100,
  },
  Degraded: {
    "aggregate_severity": "Degraded",
    "aggregate_color": "#FFE98C",
    "aggregate_value": 50,
  },
}
const statusRank = [
  "Unresponsive",
  "Degraded",
  // Unknown indicates that for some reason we are unable to perform any check
  // for the status of the given service
  "Unknown",
  "Operational"
]

const domain = process.env.BASE_DOMAIN || "batcave-test.internal.cms.gov"

// In some environments we add a suffix to the subdomain for each service based
// on the cluster name
const serviceNameSuffix = process.env.SERVICE_NAME_SUFFIX || ""

const degradedPerformanceThresholdMillis = 2 * 1000 // 2 seconds

// serviceNames should be lowercase
const services = [
  {
    enableStatus: true,
    service: "code",
    serviceName: "sourcecode",
    productName: "GitLab",
    description: "Source code repository for ADO applications."
  },
  {
    enableStatus: true,
    service: "alertmanager",
    serviceName: "alerting",
    productName: "Alertmanager",
    description: "Handles alerts sent by monitoring service and routes them to the correct receiver."
  },
  {
    enableStatus: true,
    service: "grafana",
    serviceName: "monitoring",
    productName: "Grafana",
    description: "Provide realtime access to performance metrics with predefined and customizable dashboards to visualize logging and monitoring data."
  },
  {
    enableStatus: true,
    service: "rapidfort",
    serviceName: "container-hardening",
    productName: "RapidFort",
    description: "Strips out unused container components to reduce vulnerability surface."
  },
  {
    enableStatus: false,
    service: "tracing",
    serviceName: "event-tracing",
    productName: "Jaeger",
    description: "Enables tracing of events in a distributed architecture."
  },
  {
    enableStatus: !!process.env.SIGNAL_URL,
    serviceName: "signal",
    productName: "SIGNAL",
    description: "Schedule cybersecurity testing.",
    url: process.env.SIGNAL_URL
  }
]
const serviceHierarchy = [
  {
    name: "shared-services",
    description: "ADO Shared Services",
    children: [
      {
        name: "dev-tools",
        description: "DevSecOps Enablement",
        children: ["sourcecode"]
      },
      {
        name: "logging-monitoring-alerting",
        description: "Logging, Monitoring, and Alerting",
        children: ["monitoring", "alerting"]
      },
      {
        name: "container-security",
        description: "Container Security",
        children: ["container-hardening"]
      }
    ]
  },
  {
    name: "applications",
    description: "Applications",
    children: [
      {
        name: "cybersecurity-test-scheduling",
        description: "Cybersecurity Test Scheduling",
        children: ["signal"]
      }
    ]
  }
]
const httpOptions = {
  timeout: 5000
}

function queryService(service, url, { debug }) {
  return new Promise((resolve, reject) => {
    const start = new Date()
    const debugDetails = {}
    const req = https.get(url, httpOptions, (res) => {
      // This is necessary to avoid a memory leak of the body.
      res.on('data', () => {
      })
      const end = new Date()
      if (res.statusCode >= 400) {
        resolve({
          ...statusMap.Unresponsive,
          ...debugDetails,
          detail: `Invalid HTTP status code: ${res.statusCode}`
        })
      }
      const delta = end - start
      if (delta < degradedPerformanceThresholdMillis) {
        resolve({
          ...statusMap.Operational,
          ...debugDetails
        })
      } else {
        resolve({
          ...statusMap.Degraded,
          ...debugDetails,
          detail: `Service took longer than expected to respond: ${delta}ms`
        })
      }
    }).on('timeout', (e) => {
      resolve({
        ...statusMap.Unresponsive,
        ...debugDetails,
        detail: "Request timed out."
      })
    }).on('error', (e) => {
      // DNS resolution failure, connection refused, invalid certificate, other?
      resolve({
        ...statusMap.Unresponsive,
        ...debugDetails,
        detail: "Unexpected error making request."
      })
    })

    if (debug) {
      req.on('socket', (socket) => {
        socket.on('lookup', (err, address, family, host) => {
          debugDetails.remoteAddress = address;
        })
        socket.on('connect', () => {
          debugDetails.connected = true;
        })
      });
    }
  }).then(result => ({
    service_name: service.serviceName,
    product_name: service.productName,
    description: service.description,
    ...result,
    service_url: url
  }))
}

async function queryHierarchy(item, options) {
  if (typeof item === 'string') {
    // Service
    const serviceId = item.toLowerCase()
    const service = services.find(s => s.serviceName === serviceId)
    if (service?.enableStatus) {
      const url = service.url ?? `https://${service.service}${serviceNameSuffix}.${domain}/`
      return queryService(service, url, options)
    }
  } else {
    const children = await Promise.all(
      item.children.map(c => queryHierarchy(c, options))
    )

    let aggregateStatus = undefined
    let aggregateRank = undefined
    for (const child of children) {
      if (child?.aggregate_severity) {
        const rank = statusRank.indexOf(child.aggregate_severity)
        // Lower values are worse. We want to aggregate to the value of the worst child.
        if (aggregateRank === undefined || rank < aggregateRank) {
          aggregateRank = rank
          aggregateStatus = child.aggregate_severity
        }
      }
    }

    let statusDetail = aggregateStatus ?
      { ...statusMap[aggregateStatus] } :
      { aggregate_severity: "Unknown" }

    // Don't include value when aggregating
    delete statusDetail.aggregate_value

    return {
      service_name: item.name,
      description: item.description,
      ...statusDetail,
      children: children.filter(status => status != null)
    }
  }
}

function selectPath(pathArray) {
  let children = serviceHierarchy
  let current = undefined
  for (let i = 0; i < pathArray.length; i++) {
    const part = pathArray[i].toLowerCase()
    const match = children.find(c => c === part || c.name === part)

    if (!match) {
      return
    } else if (typeof match === 'string') {
      if (i + 1 === pathArray.length) {
        return match
      } else {
        return
      }
    } else {
      current = match
      children = current.children
    }
  }

  return current
}
function getHealthcheckOptions(event) {
  return { debug: event.queryStringParameters["debug"] != null }
}

async function listAllServices(event) {
  const options = getHealthcheckOptions(event)
  const result = await Promise.all(serviceHierarchy.map(s => queryHierarchy(s, options)))
  return successResponse(result)
}

const getServicePathRegExp = /\/api\/v1\/services\/(?<path>.*)$/i
async function getService(event) {
  const options = getHealthcheckOptions(event)
  const pathArray = getServicePathRegExp.exec(event.path)?.groups["path"].split('/').filter(p => !!p)
  const item = selectPath(pathArray)
  if (item) {
    const result = await queryHierarchy(item, options)
    return successResponse(result)
  } else {
    return notFoundResponse(
      `No service matching the specified path could be found: '${pathArray.join('/')}'`
    )
  }
}

async function legacyGetService(event) {
  const options = getHealthcheckOptions(event)
  let serviceName = event.path.substring(1);
  let service;
  switch (serviceName) {
    case 'code':
    case 'tracing':
      service = services.find(svc => svc.service === serviceName);
      const url = service.url ?? `https://${service.service}${serviceNameSuffix}.${domain}/`
      const result = await queryService(service, url, options)
      return successResponse({
        "service_name": result.product_name.toLowerCase(),
        "aggregate_severity": result.aggregate_severity,
        "aggregate_color": result.aggregate_color,
        "aggregate_value": result.aggregate_value
      })
    default:
      return successResponse({
        "service_name": serviceName,
        ...statusMap.Unresponsive,
      })
  }
}

const listChildServicesPathRegExp = /\/api\/v1\/services\/(?<path>.*)\/children$/i
async function listChildServices(event) {
  const options = getHealthcheckOptions(event)
  const pathArray = listChildServicesPathRegExp.exec(event.path)?.groups["path"].split('/').filter(p => !!p)
  const item = selectPath(pathArray)
  if (item) {
    const result = await queryHierarchy(item, options)
    return successResponse(result.children)
  } else {
    return notFoundResponse(
      `No service matching the specified path could be found: '${pathArray.join('/')}'`
    )
  }
}

const successResponse = (body) => {
  return {
    statusCode: 200,
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json"
    }
  }
}

const notFoundResponse = (message) => {
  return {
    statusCode: 404,
    body: message,
    headers: {
      "Content-Type": "text/plain"
    }
  }
}

const routes = [
  {
    method: "GET",
    path: "/api/v1/services",
    handler: middy(listAllServices).use(errorLogger())
  },
  {
    method: "GET",
    path: "/api/v1/services/{path}/children",
    handler: middy(listChildServices).use(errorLogger())
  },
  {
    method: "GET",
    path: "/api/v1/services/{path}",
    handler: middy(getService).use(errorLogger())
  },
  {
    method: "GET",
    path: "/api/{path}",
    handler: middy(() => notFoundResponse("Route does not exis"))
  },
  {
    method: "GET",
    path: "/{service}",
    handler: middy(legacyGetService).use(errorLogger())
  }
]

export const lambdaHandler = middy()
  .handler(httpRouterHandler(routes))
  // Note: this error handler needs to be registered *before* the
  // httpErrorHandler because the error handlers are executed in reverse order
  .onError(request => {
    if (request.error && !request.response) {
      // Report unhandled
      request.response = {
        statusCode: 500,
        body: "An unhandled internal error occurred.",
        headers: {
          "Content-Type": "text/plain"
        }
      }
    }
  })
  // This is needed to handle errors from httpRouterHandler
  .use(httpErrorHandler())
