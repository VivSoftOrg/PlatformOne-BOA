# Introduction
Kyverno is a Kubernetes Native Admissions Controller. It is designed to audit and enforce policies and best practices within the Kubernetes Cluster, by checking all resource requests as they are being created (there is also a separete Kyverno CLI tool to apply policies and checks to YAML files prior to being applied and other similar scenarios), and evaluating them against a set of conditions, and can then do one of the following.

- Audit a rule for pass or fail, but not enforce
- Enforce a rule, and only allow the resouce to be created if it passes, does not create the resouce if it fails
- Mutates/Changes a pod in a particular way that the policy or rule defines, based on the criteria when it matches or passes

Kyverno comes in 2 parts within the cluster.
- The Kyverno Application itself
- The Kyverno Policies, as a separate set of resources

This repository includes the resources and instructions for applying just the Kyverno Policies to the cluster.

Kyverno as an application, needs to be installed in the cluster prior to trying to apply/install the policies.


# Permanently Apply the Policies using Kustomize
- Kyverno as an application, needs to be installed in the cluster prior to trying to apply/install the policies
- From Command Line, enter the necessary environment variables for your AWS Credentials as obtained from Cloudtamer, and connect to the cluster you wish to apply the policies to
- Install the full version of Kyverno, using something like 'brew install kustomize'
- Pull this repository and the correct release branch
- Run the following command, replacing 'overlays/audit-only/' with the path to <repository path>/overlays/audit-only/
```
kustomize build overlays/audit-only/ | kubectl apply -f -
```