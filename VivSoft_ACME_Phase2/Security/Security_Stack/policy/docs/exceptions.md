# OPA Gatekeeper Violation Exceptions

If you have a violation in OPA Gatekeeper, one of the following actions can be taken to remedy the situation.  The actions are listed from most-preferred to least preferred.

## Fix the resource problem

Whenever possible, attempt to fix the problem in the resource that is causing the violation.  This eliminates the risk and provides the highest security posture.

> If you cannot fix the problem, you must discuss your exception plan with your security team to insure the risk is acceptable for your cluster.

## Add a specific exclusion

The `excludedResources` value is available in each violation's properties to exclude a specific resource.  Set this to the namespace/resource_name to create an exclusion.  For example, to exclude the container "bad-container" from the namespace `myns`:

```yaml
violations:
  someConstraint:
    properties:
      excludedResources:
      # Make sure to add a justification here for future inquiries
      - myns/bad-container
```

> The resource name may be the name of a container, pod, service, ingress, etc., depending on the constraint

**Risk**: The single excluded resource now has the ability to violate the rule set in the constraint.

## Add a wildcard resource exclusion

In some cases, you may not know the exact name of the resource, or it is burdensome to list them all.  In this case, a regular expression can be used in the `excludedResources` value to match the namespace/resource_names.  Care should be taken to match as much as possible to limit risk.  For example, a deployment will add alphanumeric characters as a suffix to pod names.  To match `myns` namespace pods `node-exporter-Uak3`,  `node-exporter-wSlp`, and any future deployments, you would use:

```yaml
violations:
  someConstraint:
    properties:
      excludedResources:
      # Make sure to add a justification here for future inquiries
      - myns/node-exporter-.*
```

> The resource name may be the name of a container, pod, service, ingress, etc., depending on the constraint

**Risk**: Any resources that match the regex now have the ability to violate the rule set in the constraint.

## Exclude a namespace

In some cases, you may need to apply a constraint only on specific namespaces.  This type of exclusion usually applies to features that you only have enabled but don't apply to some namespaces (e.g. istio sidecar injection).  To exclude by namespace, use the `excludedNamespaces` value under `match`.  The following shows how you can exclude an entire namespace.

```yaml
violations:
  someConstraint:
    match:
      excludedNamespaces:
      # Make sure to add a justification here for future inquiries
      - myns
```

**Risk**: Any resources in the namespace now have the ability to violate the rule set in the constraint.

## Only include specific namespaces

In some cases, you may want to only apply a constraint to a whitelist of namespaces.  For example, you want to insure [Guaranteed Quality of Service](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/) on high priority namespaces.  To do this, you would use the `namespaces` value under `match`.  The following shows an example of adding a namespace to the constraint:

```yaml
violations:
  someConstraint:
    match:
      namespaces:
      # Make sure to add a justification here for future inquiries
      - myns
```

> For other options that can be used in `match` (e.g. namespace selectors, label selectors), refer to the [OPA Gatekeeper Constraint documentation](https://open-policy-agent.github.io/gatekeeper/website/docs/howto#constraints).

**Risk**: All resources outside of the specified namespace now have the ability to violate the rule set in the constraint.

## Add an allowance to the constraint

Some constraints have a whitelist of allowed properties that can be expanded to reduce the violations.  You will need to look at the `properties` section for the specific violation to see what allowances it may have.  For example, the `allowedDockerRegistries` has a list of registries that containers can pull from.   Below is an example of adding an allowance:

```yaml
violations:
  allowedDockerRegistries:
    parameters:
      repos:
      - registry1.dso.mil
      # Make sure to add a justification here for future inquiries
      - myregistry.dso.mil
```

> If you only need an allowance added for a subset of the cluster, it is better to create a duplicate constraint and allowances along with included/excluded namespaces.

**Risk**: All resources, cluster wide, will not be flagged if they use one of the values.

## Disable the constraint

As a last resort, constraints can be disabled using the `enabled` flag, like the following:

```yaml
violations:
  someConstraint:
    enabled: false
```
