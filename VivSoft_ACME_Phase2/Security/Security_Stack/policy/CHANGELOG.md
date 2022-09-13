# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---
## [3.7.1-bb.0]
### Changed
- Updated application and corresponding helm chart to v3.7.1

## [3.7.0-bb.9]
### Changed
- Updated kubectl images to 1.22.2
- Updated renovate to monitor all images including `kubectl` test and crd images

## [3.7.0-bb.8]
### Changed
- Updated kubectl image

## [3.7.0-bb.7]
### Changed
- Reenabled PSP due to issues on RKE2

## [3.7.0-bb.6]
### Changed
- Disabled PSP due to deprecation warning

## [3.7.0-bb.5]
### Fixed
- Update Chart.yaml to follow new standardization for release automation
- Added renovate check to update new standardization

## [3.7.0-bb.4]
### Fixed
- Missing emptyDir in PSP, copied from upstream fix: https://github.com/open-policy-agent/gatekeeper/commit/ae9e7dd1c8c5a23e748f0893468abe18218fa357

## [3.7.0-bb.3]
### Changed
- Relocated bbtest values

## [3.7.0-bb.2]
### Changed
- Refactoring helm tests

## [3.7.0-bb.1]
### Fixed
- Fixed missing kpt updates from 3.7.0 upgrade

## [3.7.0-bb.0]
### Changed
- Updated application and corresponding helm chart to v3.7.0
- Updated kubectl image

## [3.6.0-bb.2]
### Changed
- Enable OPA to log denies by default

## [3.6.0-bb.1]
### Changed
- Set validatingWebhookTimeoutSeconds to 15 seconds.

## [3.6.0-bb.0]
### Changed
- Updated application and corresponding helm chart to v3.6.0

## [3.5.2-bb.2]
### Added
- ConstraintTemplate CRD v1 version. Storage set to false.

## [3.5.2-bb.1]
### Changed
- Updated upgrade job to remove orphan or disabled constraints.

## [3.5.2-bb.0]
### Changed
- Updated application and corresponding helm chart to v3.5.2

## [3.5.1-bb.16]
### Changed
- Changed resource limits and requirements for manager pods

## [3.5.1-bb.15]
### Changed
- Changed names of several Constraint Templates to workaround upgrade problem when changing CRD schema

## [3.5.1-bb.14]
### Changed
- Fixed problems with K8sPSPHostNetworkingPorts template
- Added fine grained control of excluded resources using namespace and resource name
- Added chart label to controller to force reroll on chart upgrades
- Renamed constraint template `K8sRequiredPod` to `K8sQualityOfService` and removed deprecated violations
### Removed
- Deprecated constraint templates removed
  - `K8sRequiredLabels` (use `K8sRequiredLabelValues` instead)
  - `K8sIstioInjection` (use `K8sRequiredLabelValues` instead )
  - `K8sPSPFSGroup` (use `K8sPSPAllowedUsers` instead)

## [3.5.1-bb.13]
### Changed
- Updated Post-upgrade job to use imagePullSecrets

## [3.5.1-bb.12]
### Changed
- Removed Big Bang overrides from default values.  Look in Big Bang repo under `chart/templates/gatekeeper/values.yaml` for overrides.

## [3.5.1-bb.11]
### Added
- Post-upgrade job to remove disabled constraints
### Changed
- Moved constraint kind and name to values.yaml

## [3.5.1-bb.10]
### Changed
- Removed rule for `unique-service-selector`

## [3.5.1-bb.9]
### Changed
- Changed the resource requests and limits to be equal 

## [3.5.1-bb.8]
### Changed
- Excluded kube-system from all constraints through config
- Reverted values to no longer include kube-system as excluded

## [3.5.1-bb.7]
### Changed
- Set batch mode default to process 500 entries to reduce memory footprint
- Turned on match kind only to reduce memory footprint
- Increased audit interval to every 5 minutes

## [3.5.1-bb.6]
### Changed
- Updated constraint `no-host-namespace` enforcement to default deny
- Removed monitoring namespace exception for constraint `host-networking`

## [3.5.1-bb.5]
### Changed
- Remove duplicate keys in Chart.yaml

## [3.5.1-bb.4]
### Changed
- Updated constraint `https-only` enforcement to default deny

## [3.5.1-bb.3]
### Changed
- Updated constraint `volume-types` enforcement to default deny

## [3.5.1-bb.2]
### Changed
- Updated constraint `allowed-docker-registries` enforcement to default deny
- Excluded kube-system namespace for constraint `allowed-docker-registries`

## [3.5.1-bb.1]
### Changed
- Updated constraint `restrictedTaint` enforcement to default deny, added exception for `monitoring` namespace for to allow prometheus-node-exporter pods

## [3.5.1-bb.0]
### Changed
- Updated application and corresponding helm chart to v3.5.1

## [3.4.0-bb.19]
### Changed
- Disabled `app-armor-profiles` constraint by default

## [3.4.0-bb.18]
### Changed
- Align Cluster Auditor default constraint values to Kubernetes Pod Security Standard

## [3.4.0-bb.17]
### Changed
- Updated constraint `selinux-policy` enforcement to default deny
- added exception for logging namespace to selinux policy

## [3.4.0-bb.16]
### Changed
- Updated constraint `unique-ingress-hosts` enforcement to default deny

## [3.4.0-bb.15]
### Changed
- Updated constraint `host-networking` enforcement to default deny
- added exemption for monitoring namespace, this will prevent the `K8sPSPHostNetworkingPorts` from reporting a violation on monitoring namespace.

## [3.4.0-bb.14]
### Changed
- Updated constraint `no-privileged-containers` enforcement to default deny
- added exception for logging namespace to no-privileged-containers constraint

## [3.4.0-bb.13]
### Changed
- Updated constraint `banned-image-tags` enforcement to default deny
- added violation to constraintTemplate `k8sbannedimagetags` to not allow containers with no specified tag

## [3.4.0-bb.12]
### Changed
- Changed nosysctls policy to deny

## [3.4.0-bb.11]
### Changed
- Reverted constraint `pods-have-istio` enforcement to default dryrun
- Fixed podsHaveIstio disallowed regex sidecar.istio.io/inject to false and exclude istio-system namespace

## [3.4.0-bb.10]
### Changed
- Remove flexVolume and hostPath as default allowable for allowedFlexVolume constraint

## [3.4.0-bb.9]
### Changed
- Updated constraint  `pods-have-istio` enforcement to default deny

## [3.4.0-bb.8]
### Modified
- Modified the default enforcement action of allowed-flex-volumes to deny

## [3.4.0-bb.7]
### Added
- Added network policies to lock down egress/ingress
### Changed
- Move tests from bb-test-lib to gluon

## [3.4.0-bb.6]
### Modified
- Modified the default enforcement action of allowProcMount to deny.

## [3.4.0-bb.5]
### Changed
- Changed allowed-ips constraint to deny

## [3.4.0-bb.4]
### Changed
- Changed names of all constraints so that during upgrade, cluster-auditor will not delete them.

## [3.4.0-bb.3]
### Changed
- Updated CI values to only include 'default' namespace for deny actions

## [3.4.0-bb.2]
### Added
- `K8sDenySADefault` constraint template.
- `K8sDenySADefault` constraint
- Added `ServiceAccount` for good pod testing
### Changed
- Removed `K8sDenyServiceAccountTokentAutoMount` constraint template
- Updated test script to account for added SA.

## [3.4.0-bb.1]
### Added
- Constraints were moved from cluster-auditor to OPA gatekeeper package
### Changed
- Constraint template library split into individual files
- Constraints renamed to match values.yaml
- Constraint Templates renamed to match kind

## [3.4.0-bb.0]
### Added
- Common labels on Big Bang created components
### Changed
- Updated helm chart to upstream v3.4.0, which included the following notable items:
  - Removal of Helm v2 support. See [upgrade instructions](https://github.com/open-policy-agent/gatekeeper/blob/master/charts/gatekeeper/README.md#upgrade-chart)
  - Experimental use of [Mutation](https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/mutation.md)
  - Use of helm specified namespace vs. hardcoded `gatekeeper-system`
- Update docs/ConstraintTemplates list with latest templates

## [3.3.0-bb.5]
### Changed
- Remove constraint templates K8sRequiredDeploymentLabels & K8sRequiredIronBankImages.
- The constraint templates are replaced with K8sRequiredLabelValues & K8sAllowedRepos

## [3.3.0-bb.4]
### Fixed
- Typo in K8sDenyServiceNodePort message
- Typo in K8sNoAnnotationValues message
- Missing "service" in gatekeeper config

## [3.3.0-bb.3]
### Changed
- More Constraint Templates

## [3.3.0-bb.2]
### Changed
- Added Constraint Templates

## [3.3.0-bb.1]
### Changed
- Added helm test

## [3.3.0-bb.0]
### Changed
- Added changelog
- update chart and image to v3.3.0
