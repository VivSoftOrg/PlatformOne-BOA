# OPA Constraint Framework

OPA Gatekeeper uses the [OPA Constraint Framework](https://github.com/open-policy-agent/frameworks/tree/master/constraint) to establish and implement policy enforcement.

## Custom Resource Definitions

[Custom Resources Definitions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/) (CRDs) are utilized as an extension of Kubernetes API. They store collections of API objects. CRDs allow a new restful resource path and create custom objects. OPA Gatekeeper's CRDs have the ability to dynamically configure OPA policies.

The two main types of policy authoring Gatekeeper uses are Constraint Templates and Constraints.

## Constraint Templates

[Constraint Templates](https://github.com/open-policy-agent/gatekeeper#constraint-templates) constraint templates. OPA Gatekeeper's library of parameterized Constraint Templates determine enforcement rules and the constraint schema. The Constraint Template CRDs are written in OPA's query language called Rego. Rego is a simple syntax that incorporates a small set of functions and operators for query evaluation. The Constraint Templates does not trigger the policy enforcement without the assistance of Constraints.

## Constraints

Native Kubernetes CRDs for instantiating the policy library is called constraints. Constraints CRDs are written in the Rego language and are created after the Constraint Templates are in place.  This is accomplished using a post-install/post-upgrade Helm chart hook.  As a result, you must use the `--wait` option in Helm deployments to insure the hook is called at the appropriate time.

Constraints are instances of the Constraint Templates. They define the policies and requirements that need to be met.

For more information on OPA Gatekeeper Constraints and Constraint Template refer to the following [link](https://open-policy-agent.github.io/gatekeeper/website/docs/howto/).
