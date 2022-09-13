# gatekeeper

![Version: 3.7.1-bb.0](https://img.shields.io/badge/Version-3.7.1--bb.0-informational?style=flat-square) ![AppVersion: v3.7.1](https://img.shields.io/badge/AppVersion-v3.7.1-informational?style=flat-square)

A Helm chart for Gatekeeper

## Upstream References
* <https://github.com/open-policy-agent/gatekeeper>

* <https://github.com/open-policy-agent/gatekeeper.git>

## Learn More
* [Application Overview](docs/overview.md)
* [Other Documentation](docs/)

## Pre-Requisites

* Kubernetes Cluster deployed
* Kubernetes config installed in `~/.kube/config`
* Helm installed

Install Helm

https://helm.sh/docs/intro/install/

## Deployment

* Clone down the repository
* cd into directory
```bash
helm install gatekeeper chart/
```

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| replicas | int | `3` |  |
| auditInterval | int | `300` |  |
| auditMatchKindOnly | bool | `true` |  |
| constraintViolationsLimit | int | `1000` |  |
| auditFromCache | bool | `false` |  |
| disableMutation | bool | `true` |  |
| disableValidatingWebhook | bool | `false` |  |
| validatingWebhookTimeoutSeconds | int | `15` |  |
| validatingWebhookFailurePolicy | string | `"Ignore"` |  |
| validatingWebhookCheckIgnoreFailurePolicy | string | `"Fail"` |  |
| enableDeleteOperations | bool | `false` |  |
| enableExternalData | bool | `false` |  |
| mutatingWebhookFailurePolicy | string | `"Ignore"` |  |
| mutatingWebhookTimeoutSeconds | int | `3` |  |
| auditChunkSize | int | `500` |  |
| logLevel | string | `"INFO"` |  |
| logDenies | bool | `true` |  |
| emitAdmissionEvents | bool | `false` |  |
| emitAuditEvents | bool | `false` |  |
| resourceQuota | bool | `true` |  |
| postInstall.labelNamespace.enabled | bool | `true` |  |
| postInstall.labelNamespace.image.repository | string | `"registry1.dso.mil/ironbank/opensource/kubernetes/kubectl"` |  |
| postInstall.labelNamespace.image.tag | string | `"v1.22.2"` |  |
| postInstall.labelNamespace.image.pullPolicy | string | `"IfNotPresent"` |  |
| postInstall.labelNamespace.image.pullSecrets | list | `[]` |  |
| image.repository | string | `"registry1.dso.mil/ironbank/opensource/openpolicyagent/gatekeeper"` |  |
| image.release | string | `"v3.7.1"` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.pullSecrets[0].name | string | `"private-registry"` |  |
| image.crdRepository | string | `"registry1.dso.mil/ironbank/opensource/kubernetes/kubectl"` |  |
| image.crdRelease | string | `"v1.22.2"` |  |
| podAnnotations."container.seccomp.security.alpha.kubernetes.io/manager" | string | `"runtime/default"` |  |
| podLabels | object | `{}` |  |
| podCountLimit | int | `100` |  |
| secretAnnotations | object | `{}` |  |
| controllerManager.exemptNamespaces | list | `[]` |  |
| controllerManager.exemptNamespacePrefixes | list | `[]` |  |
| controllerManager.hostNetwork | bool | `false` |  |
| controllerManager.dnsPolicy | string | `"ClusterFirst"` |  |
| controllerManager.port | int | `8443` |  |
| controllerManager.metricsPort | int | `8888` |  |
| controllerManager.healthPort | int | `9090` |  |
| controllerManager.priorityClassName | string | `"system-cluster-critical"` |  |
| controllerManager.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].key | string | `"gatekeeper.sh/operation"` |  |
| controllerManager.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].operator | string | `"In"` |  |
| controllerManager.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].values[0] | string | `"webhook"` |  |
| controllerManager.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.topologyKey | string | `"kubernetes.io/hostname"` |  |
| controllerManager.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].weight | int | `100` |  |
| controllerManager.tolerations | list | `[]` |  |
| controllerManager.nodeSelector."kubernetes.io/os" | string | `"linux"` |  |
| controllerManager.resources.limits.cpu | string | `"175m"` |  |
| controllerManager.resources.limits.memory | string | `"512Mi"` |  |
| controllerManager.resources.requests.cpu | string | `"175m"` |  |
| controllerManager.resources.requests.memory | string | `"512Mi"` |  |
| audit.hostNetwork | bool | `false` |  |
| audit.dnsPolicy | string | `"ClusterFirst"` |  |
| audit.metricsPort | int | `8888` |  |
| audit.healthPort | int | `9090` |  |
| audit.priorityClassName | string | `"system-cluster-critical"` |  |
| audit.affinity | object | `{}` |  |
| audit.tolerations | list | `[]` |  |
| audit.nodeSelector."kubernetes.io/os" | string | `"linux"` |  |
| audit.writeToRAMDisk | bool | `false` |  |
| audit.resources.limits.cpu | float | `1.2` |  |
| audit.resources.limits.memory | string | `"768Mi"` |  |
| audit.resources.requests.cpu | float | `1.2` |  |
| audit.resources.requests.memory | string | `"768Mi"` |  |
| crds.resources | object | `{}` |  |
| pdb.controllerManager.minAvailable | int | `1` |  |
| service | object | `{}` |  |
| disabledBuiltins | string | `nil` |  |
| psp.enabled | bool | `true` |  |
| upgradeCRDs.enabled | bool | `true` |  |
| cleanupCRDs.enabled | bool | `true` |  |
| rbac.create | bool | `true` |  |
| violations.allowedAppArmorProfiles.enabled | bool | `false` |  |
| violations.allowedAppArmorProfiles.enforcementAction | string | `"dryrun"` |  |
| violations.allowedAppArmorProfiles.kind | string | `"K8sPSPAppArmor"` |  |
| violations.allowedAppArmorProfiles.name | string | `"allowed-app-armor-profiles"` |  |
| violations.allowedAppArmorProfiles.match | object | `{}` |  |
| violations.allowedAppArmorProfiles.parameters.allowedProfiles[0] | string | `"runtime/default"` |  |
| violations.allowedAppArmorProfiles.parameters.excludedResources | list | `[]` |  |
| violations.allowedCapabilities.enabled | bool | `true` |  |
| violations.allowedCapabilities.enforcementAction | string | `"dryrun"` |  |
| violations.allowedCapabilities.kind | string | `"K8sPSPCapabilities"` |  |
| violations.allowedCapabilities.name | string | `"allowed-capabilities"` |  |
| violations.allowedCapabilities.match | object | `{}` |  |
| violations.allowedCapabilities.parameters.allowedCapabilities | list | `[]` |  |
| violations.allowedCapabilities.parameters.requiredDropCapabilities[0] | string | `"all"` |  |
| violations.allowedCapabilities.parameters.excludedResources | list | `[]` |  |
| violations.allowedDockerRegistries.enabled | bool | `true` |  |
| violations.allowedDockerRegistries.enforcementAction | string | `"deny"` |  |
| violations.allowedDockerRegistries.kind | string | `"K8sAllowedRepos"` |  |
| violations.allowedDockerRegistries.name | string | `"allowed-docker-registries"` |  |
| violations.allowedDockerRegistries.match | object | `{}` |  |
| violations.allowedDockerRegistries.parameters.repos[0] | string | `"registry1.dso.mil"` |  |
| violations.allowedDockerRegistries.parameters.excludedResources | list | `[]` |  |
| violations.allowedFlexVolumes.enabled | bool | `true` |  |
| violations.allowedFlexVolumes.enforcementAction | string | `"deny"` |  |
| violations.allowedFlexVolumes.kind | string | `"K8sPSPFlexVolumes"` |  |
| violations.allowedFlexVolumes.name | string | `"allowed-flex-volumes"` |  |
| violations.allowedFlexVolumes.match | object | `{}` |  |
| violations.allowedFlexVolumes.parameters.allowedFlexVolumes | list | `[]` |  |
| violations.allowedFlexVolumes.parameters.excludedResources | list | `[]` |  |
| violations.allowedHostFilesystem.enabled | bool | `true` |  |
| violations.allowedHostFilesystem.enforcementAction | string | `"deny"` |  |
| violations.allowedHostFilesystem.kind | string | `"K8sPSPHostFilesystem"` |  |
| violations.allowedHostFilesystem.name | string | `"allowed-host-filesystem"` |  |
| violations.allowedHostFilesystem.match | object | `{}` |  |
| violations.allowedHostFilesystem.parameters.allowedHostPaths | list | `[]` |  |
| violations.allowedHostFilesystem.parameters.excludedResources | list | `[]` |  |
| violations.allowedIPs.enabled | bool | `true` |  |
| violations.allowedIPs.enforcementAction | string | `"deny"` |  |
| violations.allowedIPs.kind | string | `"K8sExternalIPs"` |  |
| violations.allowedIPs.name | string | `"allowed-ips"` |  |
| violations.allowedIPs.match | object | `{}` |  |
| violations.allowedIPs.parameters.allowedIPs | list | `[]` |  |
| violations.allowedIPs.parameters.excludedResources | list | `[]` |  |
| violations.allowedProcMount.enabled | bool | `true` |  |
| violations.allowedProcMount.enforcementAction | string | `"deny"` |  |
| violations.allowedProcMount.kind | string | `"K8sPSPProcMount"` |  |
| violations.allowedProcMount.name | string | `"allowed-proc-mount"` |  |
| violations.allowedProcMount.match | object | `{}` |  |
| violations.allowedProcMount.parameters.procMount | string | `"Default"` |  |
| violations.allowedProcMount.parameters.excludedResources | list | `[]` |  |
| violations.allowedSecCompProfiles.enabled | bool | `true` |  |
| violations.allowedSecCompProfiles.enforcementAction | string | `"dryrun"` |  |
| violations.allowedSecCompProfiles.kind | string | `"K8sPSPSeccomp"` |  |
| violations.allowedSecCompProfiles.name | string | `"allowed-sec-comp-profiles"` |  |
| violations.allowedSecCompProfiles.match | object | `{}` |  |
| violations.allowedSecCompProfiles.parameters.allowedProfiles[0] | string | `"runtime/default"` |  |
| violations.allowedSecCompProfiles.parameters.excludedResources | list | `[]` |  |
| violations.allowedUsers.enabled | bool | `true` |  |
| violations.allowedUsers.enforcementAction | string | `"dryrun"` |  |
| violations.allowedUsers.kind | string | `"K8sPSPAllowedUsers"` |  |
| violations.allowedUsers.name | string | `"allowed-users"` |  |
| violations.allowedUsers.match | object | `{}` |  |
| violations.allowedUsers.parameters.runAsUser.rule | string | `"MustRunAsNonRoot"` |  |
| violations.allowedUsers.parameters.fsGroup.rule | string | `"MustRunAs"` |  |
| violations.allowedUsers.parameters.fsGroup.ranges[0].min | int | `1000` |  |
| violations.allowedUsers.parameters.fsGroup.ranges[0].max | int | `65535` |  |
| violations.allowedUsers.parameters.runAsGroup.rule | string | `"MustRunAs"` |  |
| violations.allowedUsers.parameters.runAsGroup.ranges[0].min | int | `1000` |  |
| violations.allowedUsers.parameters.runAsGroup.ranges[0].max | int | `65535` |  |
| violations.allowedUsers.parameters.supplementalGroups.rule | string | `"MustRunAs"` |  |
| violations.allowedUsers.parameters.supplementalGroups.ranges[0].min | int | `1000` |  |
| violations.allowedUsers.parameters.supplementalGroups.ranges[0].max | int | `65535` |  |
| violations.allowedUsers.parameters.excludedResources | list | `[]` |  |
| violations.bannedImageTags.enabled | bool | `true` |  |
| violations.bannedImageTags.enforcementAction | string | `"deny"` |  |
| violations.bannedImageTags.kind | string | `"K8sBannedImageTags"` |  |
| violations.bannedImageTags.name | string | `"banned-image-tags"` |  |
| violations.bannedImageTags.match | object | `{}` |  |
| violations.bannedImageTags.parameters.tags[0] | string | `"latest"` |  |
| violations.bannedImageTags.parameters.excludedResources | list | `[]` |  |
| violations.blockNodePort.enabled | bool | `true` |  |
| violations.blockNodePort.enforcementAction | string | `"dryrun"` |  |
| violations.blockNodePort.kind | string | `"K8sBlockNodePort"` |  |
| violations.blockNodePort.name | string | `"block-node-ports"` |  |
| violations.blockNodePort.match | object | `{}` |  |
| violations.blockNodePort.parameters.excludedResources | list | `[]` |  |
| violations.containerRatio.enabled | bool | `true` |  |
| violations.containerRatio.enforcementAction | string | `"dryrun"` |  |
| violations.containerRatio.kind | string | `"K8sContainerRatios"` |  |
| violations.containerRatio.name | string | `"container-ratios"` |  |
| violations.containerRatio.match | object | `{}` |  |
| violations.containerRatio.parameters.ratio | string | `"2"` |  |
| violations.containerRatio.parameters.excludedResources | list | `[]` |  |
| violations.hostNetworking.enabled | bool | `true` |  |
| violations.hostNetworking.enforcementAction | string | `"deny"` |  |
| violations.hostNetworking.kind | string | `"K8sPSPHostNetworkingPorts"` |  |
| violations.hostNetworking.name | string | `"host-networking"` |  |
| violations.hostNetworking.match | object | `{}` |  |
| violations.hostNetworking.parameters.hostNetwork | bool | `false` |  |
| violations.hostNetworking.parameters.min | int | `0` |  |
| violations.hostNetworking.parameters.max | int | `0` |  |
| violations.hostNetworking.parameters.excludedResources | list | `[]` |  |
| violations.httpsOnly.enabled | bool | `true` |  |
| violations.httpsOnly.enforcementAction | string | `"deny"` |  |
| violations.httpsOnly.kind | string | `"K8sHttpsOnly2"` |  |
| violations.httpsOnly.name | string | `"https-only"` |  |
| violations.httpsOnly.match | object | `{}` |  |
| violations.httpsOnly.parameters.excludedResources | list | `[]` |  |
| violations.imageDigest.enabled | bool | `true` |  |
| violations.imageDigest.enforcementAction | string | `"dryrun"` |  |
| violations.imageDigest.kind | string | `"K8sImageDigests2"` |  |
| violations.imageDigest.name | string | `"image-digest"` |  |
| violations.imageDigest.match | object | `{}` |  |
| violations.imageDigest.parameters.excludedResources | list | `[]` |  |
| violations.namespacesHaveIstio.enabled | bool | `true` |  |
| violations.namespacesHaveIstio.enforcementAction | string | `"dryrun"` |  |
| violations.namespacesHaveIstio.kind | string | `"K8sRequiredLabelValues"` |  |
| violations.namespacesHaveIstio.name | string | `"namespaces-have-istio"` |  |
| violations.namespacesHaveIstio.match.namespaceSelector.matchExpressions[0].key | string | `"admission.gatekeeper.sh/ignore"` |  |
| violations.namespacesHaveIstio.match.namespaceSelector.matchExpressions[0].operator | string | `"DoesNotExist"` |  |
| violations.namespacesHaveIstio.parameters.labels[0].allowedRegex | string | `"^enabled"` |  |
| violations.namespacesHaveIstio.parameters.labels[0].key | string | `"istio-injection"` |  |
| violations.namespacesHaveIstio.parameters.excludedResources | list | `[]` |  |
| violations.noBigContainers.enabled | bool | `true` |  |
| violations.noBigContainers.enforcementAction | string | `"dryrun"` |  |
| violations.noBigContainers.kind | string | `"K8sContainerLimits"` |  |
| violations.noBigContainers.name | string | `"no-big-container"` |  |
| violations.noBigContainers.match | object | `{}` |  |
| violations.noBigContainers.parameters.cpu | string | `"2000m"` |  |
| violations.noBigContainers.parameters.memory | string | `"4G"` |  |
| violations.noBigContainers.parameters.excludedResources | list | `[]` |  |
| violations.noHostNamespace.enabled | bool | `true` |  |
| violations.noHostNamespace.enforcementAction | string | `"deny"` |  |
| violations.noHostNamespace.kind | string | `"K8sPSPHostNamespace2"` |  |
| violations.noHostNamespace.name | string | `"no-host-namespace"` |  |
| violations.noHostNamespace.match | object | `{}` |  |
| violations.noHostNamespace.parameters.excludedResources | list | `[]` |  |
| violations.noPrivilegedContainers.enabled | bool | `true` |  |
| violations.noPrivilegedContainers.enforcementAction | string | `"deny"` |  |
| violations.noPrivilegedContainers.kind | string | `"K8sPSPPrivilegedContainer2"` |  |
| violations.noPrivilegedContainers.name | string | `"no-privileged-containers"` |  |
| violations.noPrivilegedContainers.match | object | `{}` |  |
| violations.noPrivilegedContainers.parameters.excludedResources | list | `[]` |  |
| violations.noDefaultServiceAccount.enabled | bool | `true` |  |
| violations.noDefaultServiceAccount.enforcementAction | string | `"dryrun"` |  |
| violations.noDefaultServiceAccount.kind | string | `"K8sDenySADefault"` |  |
| violations.noDefaultServiceAccount.name | string | `"no-default-service-account"` |  |
| violations.noDefaultServiceAccount.match | object | `{}` |  |
| violations.noDefaultServiceAccount.parameters.excludedResources | list | `[]` |  |
| violations.noPrivilegedEscalation.enabled | bool | `true` |  |
| violations.noPrivilegedEscalation.enforcementAction | string | `"dryrun"` |  |
| violations.noPrivilegedEscalation.kind | string | `"K8sPSPAllowPrivilegeEscalationContainer2"` |  |
| violations.noPrivilegedEscalation.name | string | `"no-privileged-escalation"` |  |
| violations.noPrivilegedEscalation.match | object | `{}` |  |
| violations.noPrivilegedEscalation.parameters.excludedResources | list | `[]` |  |
| violations.noSysctls.enabled | bool | `true` |  |
| violations.noSysctls.enforcementAction | string | `"deny"` |  |
| violations.noSysctls.kind | string | `"K8sPSPForbiddenSysctls"` |  |
| violations.noSysctls.name | string | `"no-sysctls"` |  |
| violations.noSysctls.match | object | `{}` |  |
| violations.noSysctls.parameters.forbiddenSysctls[0] | string | `"*"` |  |
| violations.noSysctls.parameters.excludedResources | list | `[]` |  |
| violations.podsHaveIstio.enabled | bool | `true` |  |
| violations.podsHaveIstio.enforcementAction | string | `"dryrun"` |  |
| violations.podsHaveIstio.kind | string | `"K8sNoAnnotationValues"` |  |
| violations.podsHaveIstio.name | string | `"pods-have-istio"` |  |
| violations.podsHaveIstio.match | object | `{}` |  |
| violations.podsHaveIstio.parameters.annotations[0].disallowedRegex | string | `"^false"` |  |
| violations.podsHaveIstio.parameters.annotations[0].key | string | `"sidecar.istio.io/inject"` |  |
| violations.podsHaveIstio.parameters.excludedResources | list | `[]` |  |
| violations.readOnlyRoot.enabled | bool | `true` |  |
| violations.readOnlyRoot.enforcementAction | string | `"dryrun"` |  |
| violations.readOnlyRoot.kind | string | `"K8sPSPReadOnlyRootFilesystem2"` |  |
| violations.readOnlyRoot.name | string | `"read-only-root"` |  |
| violations.readOnlyRoot.match | object | `{}` |  |
| violations.readOnlyRoot.parameters.excludedResources | list | `[]` |  |
| violations.requiredLabels.enabled | bool | `true` |  |
| violations.requiredLabels.enforcementAction | string | `"dryrun"` |  |
| violations.requiredLabels.kind | string | `"K8sRequiredLabelValues"` |  |
| violations.requiredLabels.name | string | `"required-labels"` |  |
| violations.requiredLabels.match | object | `{}` |  |
| violations.requiredLabels.parameters.labels[0].allowedRegex | string | `""` |  |
| violations.requiredLabels.parameters.labels[0].key | string | `"app.kubernetes.io/name"` |  |
| violations.requiredLabels.parameters.labels[1].allowedRegex | string | `""` |  |
| violations.requiredLabels.parameters.labels[1].key | string | `"app.kubernetes.io/instance"` |  |
| violations.requiredLabels.parameters.labels[2].allowedRegex | string | `""` |  |
| violations.requiredLabels.parameters.labels[2].key | string | `"app.kubernetes.io/version"` |  |
| violations.requiredLabels.parameters.labels[3].allowedRegex | string | `""` |  |
| violations.requiredLabels.parameters.labels[3].key | string | `"app.kubernetes.io/component"` |  |
| violations.requiredLabels.parameters.labels[4].allowedRegex | string | `""` |  |
| violations.requiredLabels.parameters.labels[4].key | string | `"app.kubernetes.io/part-of"` |  |
| violations.requiredLabels.parameters.labels[5].allowedRegex | string | `""` |  |
| violations.requiredLabels.parameters.labels[5].key | string | `"app.kubernetes.io/managed-by"` |  |
| violations.requiredLabels.parameters.excludedResources | list | `[]` |  |
| violations.requiredProbes.enabled | bool | `true` |  |
| violations.requiredProbes.enforcementAction | string | `"dryrun"` |  |
| violations.requiredProbes.kind | string | `"K8sRequiredProbes"` |  |
| violations.requiredProbes.name | string | `"required-probes"` |  |
| violations.requiredProbes.match | object | `{}` |  |
| violations.requiredProbes.parameters.probeTypes[0] | string | `"tcpSocket"` |  |
| violations.requiredProbes.parameters.probeTypes[1] | string | `"httpGet"` |  |
| violations.requiredProbes.parameters.probeTypes[2] | string | `"exec"` |  |
| violations.requiredProbes.parameters.probes[0] | string | `"readinessProbe"` |  |
| violations.requiredProbes.parameters.probes[1] | string | `"livenessProbe"` |  |
| violations.requiredProbes.parameters.excludedResources | list | `[]` |  |
| violations.restrictedTaint.enabled | bool | `true` |  |
| violations.restrictedTaint.enforcementAction | string | `"deny"` |  |
| violations.restrictedTaint.kind | string | `"RestrictedTaintToleration"` |  |
| violations.restrictedTaint.name | string | `"restricted-taint"` |  |
| violations.restrictedTaint.match | object | `{}` |  |
| violations.restrictedTaint.parameters.allowGlobalToleration | bool | `false` |  |
| violations.restrictedTaint.parameters.restrictedTaint.effect | string | `"NoSchedule"` |  |
| violations.restrictedTaint.parameters.restrictedTaint.key | string | `"privileged"` |  |
| violations.restrictedTaint.parameters.restrictedTaint.value | string | `"true"` |  |
| violations.restrictedTaint.parameters.excludedResources | list | `[]` |  |
| violations.selinuxPolicy.enabled | bool | `true` |  |
| violations.selinuxPolicy.enforcementAction | string | `"deny"` |  |
| violations.selinuxPolicy.kind | string | `"K8sPSPSELinuxV2"` |  |
| violations.selinuxPolicy.name | string | `"selinux-policy"` |  |
| violations.selinuxPolicy.match | object | `{}` |  |
| violations.selinuxPolicy.parameters.allowedSELinuxOptions | list | `[]` |  |
| violations.selinuxPolicy.parameters.excludedResources | list | `[]` |  |
| violations.uniqueIngressHost.enabled | bool | `true` |  |
| violations.uniqueIngressHost.enforcementAction | string | `"deny"` |  |
| violations.uniqueIngressHost.kind | string | `"K8sUniqueIngressHost"` |  |
| violations.uniqueIngressHost.name | string | `"unique-ingress-hosts"` |  |
| violations.uniqueIngressHost.match | object | `{}` |  |
| violations.uniqueIngressHost.parameters.excludedResources | list | `[]` |  |
| violations.volumeTypes.enabled | bool | `true` |  |
| violations.volumeTypes.enforcementAction | string | `"deny"` |  |
| violations.volumeTypes.kind | string | `"K8sPSPVolumeTypes"` |  |
| violations.volumeTypes.name | string | `"volume-types"` |  |
| violations.volumeTypes.match | object | `{}` |  |
| violations.volumeTypes.parameters.volumes[0] | string | `"configMap"` |  |
| violations.volumeTypes.parameters.volumes[1] | string | `"emptyDir"` |  |
| violations.volumeTypes.parameters.volumes[2] | string | `"projected"` |  |
| violations.volumeTypes.parameters.volumes[3] | string | `"secret"` |  |
| violations.volumeTypes.parameters.volumes[4] | string | `"downwardAPI"` |  |
| violations.volumeTypes.parameters.volumes[5] | string | `"persistentVolumeClaim"` |  |
| violations.volumeTypes.parameters.excludedResources | list | `[]` |  |
| monitoring.enabled | bool | `false` |  |
| networkPolicies.enabled | bool | `false` |  |
| networkPolicies.controlPlaneCidr | string | `"0.0.0.0/0"` |  |
| bbtests.enabled | bool | `false` |  |
| bbtests.scripts.image | string | `"registry1.dso.mil/ironbank/opensource/kubernetes/kubectl:v1.22.2"` |  |
| bbtests.scripts.additionalVolumeMounts[0].name | string | `"{{ .Chart.Name }}-test-config"` |  |
| bbtests.scripts.additionalVolumeMounts[0].mountPath | string | `"/yaml"` |  |
| bbtests.scripts.additionalVolumeMounts[1].name | string | `"{{ .Chart.Name }}-kube-cache"` |  |
| bbtests.scripts.additionalVolumeMounts[1].mountPath | string | `"/.kube/cache"` |  |
| bbtests.scripts.additionalVolumes[0].name | string | `"{{ .Chart.Name }}-test-config"` |  |
| bbtests.scripts.additionalVolumes[0].configMap.name | string | `"{{ .Chart.Name }}-test-config"` |  |
| bbtests.scripts.additionalVolumes[1].name | string | `"{{ .Chart.Name }}-kube-cache"` |  |
| bbtests.scripts.additionalVolumes[1].emptyDir | object | `{}` |  |

## Contributing

Please see the [contributing guide](./CONTRIBUTING.md) if you are interested in contributing.
