Contributing
Thanks for contributing to this repository!
This repository follows the following conventions:

Semantic Versioning
Keep a Changelog
Conventional Commits

Development requires the Kubernetes CLI tool as well as a local Kubernetes cluster. K3D is recommended as a lightweight local option for standing up Kubernetes clusters.
To contribute a change:

Create a branch on the cloned repository with a descriptive name, prefixed with your name or a tracking number (for work items). For example, bb-123/add-ingress is an appropriate branch name.
Make code changes.  Test the changes in your local environment before pushing them to Git.
Make commits using the Conventional Commits format. This helps with automation for changelog. Update CHANGELOG.md in the same commit using the Keep a Changelog. Depending on tooling maturity, this step may be automated.
Write tests using KUTTL and Conftest

Open a merge request using one of the provided templates. Reference any issues fixed in the merge request.
During this time, ensure that all new commits are rebased into your branch so that it remains up to date with the main branch.
Wait for a maintainer of the repository (see CODEOWNERS) to approve.
If you have permissions to merge, you are responsible for merging. Otherwise, a CODEOWNER will merge the commit
