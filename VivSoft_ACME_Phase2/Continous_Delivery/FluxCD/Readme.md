# FLUX CD


### Flux CD provides GitOps for the platform layer at P1.


It orchestrates the deployment of different CI pipeline tools and security stack using the concept of "Wave Deployment". Wave Deployment sequences the series of tools needed
within the pipeline to take into account dependencies.

Flux CD also integrates with Mozilla SOPS and Helm Secretes to ensure that secrets are applied right before cluster deployment using rotating keys.

