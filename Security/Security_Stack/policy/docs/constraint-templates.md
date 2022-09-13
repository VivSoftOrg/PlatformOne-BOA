# Constraint Templates

These constraint templates come with OPA Gatekeeper:

## K8sAllowedRepos

Image Repositories
Container images must be pulled from the specified repositories.

## K8sBannedImageTags

Banned Image Tags
Container Images cannot use specified tags

## K8sBlockNodePort

Node Ports
Services must not use node ports.

## K8sContainerLimits

Resource Limits
Containers must have cpu / memory limits and the values must be below the specified maximum.

## K8sContainerRatios

Resource Ratio
Container resource limits to requests ratio must not be higher than specified.

## K8sExternalIPs

External IPs
Services may only contain specified external IPs.

## K8sHttpsOnly

Ingress on HTTPS Only
Ingress must only allow HTTPS connections.

## K8sImageDigests

Image Digests
Containers must use images with a digest instead of a tag.

## K8sIstioInjection

Deprecated in favor of K8sRequiredLabelValues

## K8sNoAnnotationValues

Annotation Values
Containers must have the specified annotations.

## K8sProtectedNamespaces

Protected Namespaces
Resources cannot be deployed into specified namespaces.

## K8sPSPAllowedUsers

Users and Groups
Containers must be run as one of the specified users and groups.

## K8sPSPAllowPrivilegeEscalationContainer

Privilege Escalation
Containers must not allow escalaton of privileges.

## K8sPSPAppArmor

AppArmor Profile
Containers may only use specified AppArmor profiles.

## K8sPSPCapabilities

Linux Capabilities
Containers may only use specified Linux capabilities

## K8sPSPFlexVolumes

Flex Volume Drivers
Containers may only use Flex Volumes with the specified drivers

## K8sPSPForbiddenSysctls

SysCtls
Containers must not use specified sysctls.

## K8sPSPFSGroup

Deprecated in favor of K8sPSPAllowedUsers

## K8sPSPHostFilesystem

Host Filesystem Paths
Containers may only map volumes to the host node at the specified paths.

## K8sPSPHostNamespace

Host Namespace
Containers must not share the host's namespaces

## K8sPSPHostNetworkingPorts

Host Network Ports
Container images may only use host ports that are specified.

## K8sPSPPrivilegedContainer

Privilged Containers
Containers must not run as privileged.

## K8sPSPProcMount

Proc Mount
Containers may only use the specified ProcMount types.

## K8sPSPReadOnlyRootFilesystem

Read-only Root Filesystem
Containers must have read-only root filesystems.

## K8sDenySADefault

Default Service Account
Pods must not have default service account.

## K8sPSPSeccomp

Seccomp
Containers may only use the specified seccomp profiles.

## K8sPSPSELinuxV2

SELinux
Containers may only use the SELnux options specified.

## K8sPSPVolumeTypes

Volume Types
Containers may only use the specified volume types in volume mounts.

## K8sPvcLimits

Persistent Volume Claim Limits
Persistent Volume Claims must not be larger than the specified limit.

## K8sQualityOfService

Guaranteed Quality of Service
Pods must have limits = requests to guarantee Quality of Service

## K8sRegulatedResources

Resource List
Resources must be in the specified allow list or not in the specified deny list.

## K8sRequiredLabels

Deprecated in favor of K8sRequiredLabelValues

## K8sRequiredLabelValues

Required Labels
Containers must have the specified labels and values.

## K8sRequiredPods

Deprecated in favor of using individual constraints.

## K8sRequiredProbes

Probes
Container must have specified probes and probe types.

## K8sUniqueIngressHost

Unique Ingress Hosts
Ingress hosts must be unique.

## K8sUniqueServiceSelector

Unique Service Selector
Services must have unique selectors within a namespace.

## RestrictedTaintToleration

Taints and Tolerations
Container must be configured according to specified taint and toleration rules.
