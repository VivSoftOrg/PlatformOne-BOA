# Updating Big Bang
## Background
The Batcave platform  leverages much of its core functionality from the open-source [Big Bang](https://repo1.dso.mil/platform-one/big-bang/bigbang/-/tree/master) project. As such, frequently updating our version of Big Bang ensures we are getting the latest product features and security updates.

## Upgrade Process
The Big Bang update process will be different for every release as Big Bang spans a wide array of products/tooling, and not all tools are updated with every release.

1. Determine which BB release Batcave is currently using by checking the [bigbang.yaml](https://github.com/CMSgov/batcave-landing-zone/blob/main/apps/batcave/base/bigbang.yaml) file and identify what version of BB you want to upgrade to
1. Navigate to the BB [release page](https://repo1.dso.mil/platform-one/big-bang/bigbang/-/releases) and read the changelogs of the target version and all versions in between the target and current Batcave version to identify any breaking changes
1. Most BB upgrades involve updating Flux, so make note of which version the BB upgrade is using. To update Flux, grab the BB [gotk-components.yaml](https://repo1.dso.mil/platform-one/big-bang/bigbang/-/blob/1.38.0/base/flux/gotk-components.yaml) paying attention to the release tag, and paste the contents into the `gotk-components.yaml` [file in Batcave](https://github.com/CMSgov/batcave-landing-zone/blob/main/apps/batcave/base/flux/gotk-components.yaml)
    - For example,  if you are updating Flux to the version used by BB 1.38.0, be sure to check out `gotk-components.yaml` for the 1.38.0 version of BB
    - Also you will need to update the [Flux container versions](https://github.com/CMSgov/batcave-landing-zone/blob/main/apps/batcave/base/flux/kustomization.yaml) in Batcave by matching them to the Flux container versions identified in the BB release notes
    - The Flux CLI is not guaranteed to be backwards compatible, so make note of the new Flux version and update your local CLI to match. Also, update the Flux section in the Batcave README to match the latest CLI tool
1. Make any other necessary changes identified in the BB release notes
1. Test these changes in a new dev cluster and ensure all pods come up and applications are reachable (look at VirtualServices to determine endpoints, sometimes these must be updated to match what's in Route53 due to limitations of our dev configs)
1. Test the upgrade path by building a dev cluster off of the main branch and then performing all upgrade steps. This will be the actual process by which all long-lived clusters are upgraded, so test thoroughly and don’t forget Flux!
1. Once the changes have been thoroughly tested and the upgrade path is clear, make a PR. Once merged, the changes will automatically deploy on the `batcave-test` cluster.
1. Inspect the `batcave-test` cluster thoroughly. Once there is a high degree of confidence in the upgrade process, proceed to upgrade the rest of the clusters by updating the tags in the rest of the overlays.
    - Notify any involved parties if necessary
    - If Gitlab updates are expected, put Gitlab in [Maintenance Mode](https://docs.gitlab.com/ee/administration/maintenance_mode/) and notify the pipelines team.
    - If any downtime is expected based on the upgrade plan, coordinate with other teams in the public batcave-infrastructure channel in Slack
    - If a Flux update was required, let the developers know in the public batcave-infrastructure channel in Slack

## Testing
1. Verify that all pods are `Running`
   ```bash
   kubectl get pods -A
   ```
1. Check to see if flux, bigbang, and all other services are upgraded to your desired version  
   [Big-bang Core Apps](https://repo1.dso.mil/platform-one/big-bang/apps/core)
   ```bash
   kubectl get deployments -n flux-system source-controller -o yaml | grep "app.kubernetes.io/version: v"
   kubectl get gitrepositories.source.toolkit.fluxcd.io -n batcave bigbang -o yaml | grep tag
   ```
1. Get a list of virtual services and make sure each is working in the browser
   ```bash
   kubectl get vs -A
   ```
   > **_Note:_**  
   For tracing and alertmanager you will may receive a 400 Bad Request. This is expected.
   Alert Manager doesn't have built-in SSO, we offload SSO to authservice.

1. Make sure logs are making it to the right places (both S3 buckets)
1. Verify that helm releases have "Release reconciliation succeeded"  
   From k9s type `helmrelease`
