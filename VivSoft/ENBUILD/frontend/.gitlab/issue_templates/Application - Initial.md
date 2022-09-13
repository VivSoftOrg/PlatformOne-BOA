## Summary

Requesting application to be hardened. This is only for initial hardening of a container.


## Version Information

Current version: (State the current version of the application as you see it)

## Communication

All communication should occur through this issue. This ensures that all information is documented in a centralized location and also ensures that all of the assignees are notified of updates. It is imperative that all required parties are listed as assignees of this issue and that individuals are not removed. Please do not remove anyone from the assignee list.

If you need to contact the Container Hardening team, please identify your assigned point of contact. You can find your point of contact by:
1. They should be listed as an assignee on this ticket
2. They should be listed in the `hardening_manifest.yaml` file under the `maintainers` section with a field of `cht_member: true`

If you have no assignee, feel free to tag Container Hardening leadership in your issue by commenting on this issue with your questions/concerns and then add `/cc @ironbank-notifications/leadership`. Gitlab will automatically notify all Container Hardening leadership to look at this issue and respond.


## Responsibilities

If this application is owned by a Contributor or Vendor (identifed as `Owner::Contributor` and `Owner::Vendor` respectively), then it is your responsibility to drive this issue through completion. This means that the Container Hardening team is not here to help push any deadlines/timeframes you may have with other customers or DoD agencies. If you have issues with the activity, you may notify Container Hardening leadership above. Do not change the ownership labels.


## Definition of Done

Hardening:
- [ ] Hardening manifest is created and adheres to the schema (https://repo1.dsop.io/ironbank-tools/ironbank-pipeline/-/blob/master/schema/hardening_manifest.schema.json)
- [ ] Container builds successfully through the Gitlab CI pipeline
- [ ] Branch has been merged into `development`
- [ ] Project is configured for automatic renovate updates (if possible)

Justifications:
- [ ] All findings have been justified per the above documentation
- [ ] Justifications have been attached to this issue
- [ ] Apply the label `Approval` to indicate this container is ready for the approval phase

Note: The justifications must be provided in a timely fashion. Failure to do so could result in new findings being identified which may start this process over.

Approval Process (Container Hardening Team processes):
- [ ] Peer review from Container Hardening Team
- [ ] Findings Approver has reviewed and approved all justifications
- [ ] Approval request has been sent to Authorizing Official
- [ ] Approval request has been processed by Authorizing Official

Note: If the above approval process is kicked back for any reason, the `Approval` label will be removed and the issue will be sent back to `Open`. Any comments will be listed in this issue for you to address. Once they have been addressed, you may re-add the `Approval` label.

## Post Approval

### Continuous Monitoring

Once a container is approved, the `Approved` label will be applied to this issue and it will be closed. You will be able to find your applications on http://ironbank.dsop.io and https://registry1.dsop.io.

In addition to the above, your application will now be subscribed to continuous monitoring. This means that any new findings discovered as part of this will need justifications. To satisfy this process, any new findings will trigger a new Gitlab issue in this project with the label `Container::New Findings`. All members listed in the `maintainers` section of the `hardening_manifest.yaml` file will automatically be assigned. It is your responsibility as a Contributor or Vendor to monitor for this and provide justifications in a timely fashion. This newly created issue will have all the instructions necessary to complete the process. Failure to provide justifications could result in the revocation of the application's approval status.

### Updates

It is imperative that application updates be submitted as quickly as possible. We do not want applications to become stale. To help with this process, Ironbank recommends using a tool called [Renovate](https://github.com/renovatebot/renovate). This requires a `renovate.json` file to be placed in your project and can automate the creation of issues and merge requests.

If not using Renovate, it will be up to you as a Contributor or Vendor to keep this image up-to-date at all times. When you wish to submit an application update, you must create a new issue in this project using the `Application - Update` template and associate it with the corresponding merge request. If you submit a merge request alone, work will not proceed until a related issue is created. These issues are tracked using the label `Container::Update`.

Additionally, it is imperative that all updates must be followed through to completion. Simply submitting an application update but not following through on justifications and approvals does not suffice and risk your application's approval status being revoked.

### Bugs

Occassionally, users may file bug reports for your application. It is your responsibility to monitor for these since they are created inside your project repository. Assignees will automatically be populated by the `members` section of the `hardening_manifest.yaml` file and will have the label `Bug`.







/label ~"Container::Initial"