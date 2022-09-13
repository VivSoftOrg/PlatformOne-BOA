# Open Policy Agent Gatekeeper

The [Open Policy Agent (OPA) Gatekeeper](https://github.com/open-policy-agent/gatekeeper) assists in enforcing, monitoring, and remediating policies while strengthening governance of an environment. It provides integration between OPA and Kubernetes.

OPA Gatekeeper controls the policies for Kubernetes and acts as a customizable Kubernetes Admission Webhook. Its audit functionality offers constant monitoring of existing clusters to detect policy violations.

OPA Gatekeeper functionality includes:

- [An extensible, parameterized policy library](./docs/policylibrary.md).
- Native Kubernetes CRDs called [`ConstraintTemplates`](./docs/constraint-templates.md) for extending the policy library
  - A high level language, [Rego](./docs/rego.md), to create policies.
- Native Kubernetes CRDs called `Constraints` for instantiating the policy library.
- Audit functionality.
- [Security](./docs/security.md)
- [Test framework](./docs/test.md) for developing tests for policies.
- [Upgrade](./docs/upgrade.md) Guide for upgrading versions.

## Installation

To install and test the Gatekeeper application, follow these steps

### Prerequisite

- A kubernetes cluster with cluster-admin access
- [Helm](https://helm.sh/docs/intro/install/)

### Procedure

- Clone the application repository
   `git clone https://repo1.dso.mil/platform-one/big-bang/apps/core/policy.git`
- Change into the policy directory and lint the chart  - make sure there are no errors.
   `cd policy && helm lint chart`
- Install the chart
    `helm upgrade -i -n gatekeeper-system --create-namespace --wait opa-gatekeeper chart --debug`
- Confirm the application installed with no issues.

    ```shell
    kubectl get po -n gatekeeper-system
    NAME                                            READY   STATUS    RESTARTS   AGE
    gatekeeper-audit-7997ddc847-8pt5h               1/1     Running   0          28s
    gatekeeper-controller-manager-7fdfd7bfd-8g5sm   1/1     Running   0          28s
    gatekeeper-controller-manager-7fdfd7bfd-khc7j   1/1     Running   0          28s
    gatekeeper-controller-manager-7fdfd7bfd-nzzd8   1/1     Running   0          28s
    ```

## ConstraintTemplates and Constraints

The repo contains `ConstraintTemplate` and `Constraints`.

- `ConstraintTemplates` describe both the Rego that enforces the constraint and the schema of the constraint. It is the same context as the `ConstraintTemplate` being a CRD with the schema definition and the `Constraints` being the CRs passing parameters.

You can find `ConstraintTemplates` in [`/chart/templates/constraint-templates`](./chart/templates/constraint-templates).

- `Constraints` represent the instantiation of the `ConstraintTemplates`. They inform Gatekeeper that the admin wants a `ConstraintTemplate` to be enforced, and how.

You can find `Constraint` in [`/chart/templates/constraints`](./chart/templates/constraints).

Further information on `Constraints` and `ConstraintTemplates`:

- [Constraint Framework](./docs/constraint-framework.md)
- [Constraint Template List](./docs/constraint-templates.md)
- [Constraint Annotations](./docs/constraint-annotations.md)
- [Policy Library](./docs/policylibrary.md)
- [Rego](./docs/rego.md)
- [Violation Exceptions](./docs/exceptions.md)

## Additional OPA Gatekeeper Links

- [Webinar: K8s with OPA Gatekeeper](https://www.youtube.com/watch?v=v4wJE3I8BYM)
- [Difference between OPA and Gatekeeper](https://www.infracloud.io/blogs/opa-and-gatekeeper/)
- [K8s with OPA Gatekeeper](https://www.youtube.com/watch?v=v4wJE3I8BYM&t=2735s)
- [Fitness Validation For Your Kubernetes Apps: Policy As Code](https://itnext.io/fitness-validation-for-your-kubernetes-apps-policy-as-code-7fad698e7dec)
- [Introduction to Open Policy Agent | Rawkode Live](https://www.youtube.com/watch?v=ejH4EzmL7e0)
- [Open Policy Agent Debugging](https://www.openpolicyagent.org/docs/latest/kubernetes-debugging/)
- [OPA Gatekeeper Debugging](https://open-policy-agent.github.io/gatekeeper/website/docs/debug/)

For additional info on the architecture and how OPA fits into Big Bang see the [Architecture Doc](https://repo1.dso.mil/platform-one/big-bang/bigbang/-/blob/master/charter/packages/opa-gatekeeper/Architecture.md).
