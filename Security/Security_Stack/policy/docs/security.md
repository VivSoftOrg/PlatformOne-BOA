# Security with OPA Gatekeeper

OPA Gatekeeper enforces security policies through the use of the Admission Controller and Audit Functionality.

## Kubernetes Admission Controller

[Kubernetes Admission Controller](https://kubernetes.io/blog/2019/03/21/a-guide-to-kubernetes-admission-controllers/) is included in OPA Gatekeeper. It inspects and intercepts any Kubernetes resources added or updated
to the cluster. Admission Controller ensures the required policies defined are met. It can either deny an admissions request with the option to provide an explanation or not. However, it can accept an admission request but currently there is not a way to provide
an explanation or warning to the user. Through the usage of Kubernetes Admission Controller a binary approach can be implemented to accept changes on API resources on a cluster.

## Audit Functionality

[Cluster Auditor](https://repo1.dso.mil/platform-one/big-bang/apps/core/cluster-auditor) is used within OPA Gatekeeper services to constantly audit existing cluster objects and ensures their compliance with policies. It highlights invalid resources and violations within the cluster by passing violations to the logging stack.

OPA Gatekeeper's built-in auditing functionality allows all violations to be stored in the status field of the failed Constraint.
