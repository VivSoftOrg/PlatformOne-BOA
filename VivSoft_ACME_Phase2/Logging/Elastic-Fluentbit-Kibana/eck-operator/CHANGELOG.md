# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0-bb.0]
### Changed
- Updated chart and IB images from 1.9.1 to 2.0.0

## [1.9.1-bb.4]
### Changed
- Modified PeerAuthentication to allow for passing in mode

## [1.9.1-bb.3]
### Added
- Update Chart.yaml to follow new standardization for release automation
- Added renovate check to update new standardization

## [1.9.1-bb.2]
### Added
- Added PeerAuthentication yaml to templates that verifies both Istio and mtls are enabled.  This enables Peer Authentication/mTLS for istio communication within the namespace

## [1.9.1-bb.1]
### Added
- Added OSCAL component for ECK Operator with NIST 800-53 controls

## [1.9.1-bb.0]
### Changed
- Updated from 1.8.0 to 1.9.1

## [1.8.0-bb.0]
### Changed
- Updated from 1.7.1 to 1.8.0

## [1.7.1-bb.0]
### Changed
- Updated to 1.7.1
### Added
- Added upgrade job to replace CRDs due to breaking changes

## [1.6.0-bb.3]
### Added
- NetworkPolicy template to allow istiod communication when istio-injected.
- istio enabled toggle value to control conditional for above NetworkPolicy

## [1.6.0-bb.2]
### Changed
- Set resource limits equal to requests in order to resolve OPA container-ratio violations

## [1.6.0-bb.1]
### Added
- Added openshift toggle. Conditionally modifies networkpolicy for DNS.

## [1.6.0-bb.0]
### Changed
- Upgraded from 1.4.0 to 1.6.0

## [1.4.0-bb.4]
### Added
- Network Policy template for Kibana and Elasticsearch specific egress communication. Alleviating intermittent issue with operator not being able to talk to ES endpoint on tcp/9200

## [1.4.0-bb.3]
### Changed
- Locked egress down to only DNS and API

## [1.4.0-bb.2]
### Added
- BigBang specific Network Policy Templates for package.

## [1.4.0-bb.1]
### Changed
- Cleaned up image section in chart values.

## [1.4.0-bb.0]
### Changed
- Upgraded from 1.3.0 version to 1.4.0
