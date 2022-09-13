# ACME Phase 2 
 
 
## This repository highlights the core DevSecOps capabilities we built for DoD's Platform One and our ENBUILD delivery accelerator co-created on the project with Platform One.  
 
These repositories showcase Infrastructure as Code (IaC) and Configuration as Code (CaC) that we developed in collaboration with Platform One to enable rapid deployment of consistent, secure and scalable DevSecOps tech stacks on AWS (Amazon Web Services) Public Cloud. 
 
Where we cannot share customer code, we have provided the same open-source tooling without customer specific configuration. 
 
We grouped Infrastructure as Code (IaC) and Configuration as Code (CaC) for Cloud, Kubernetes, Continuous Integration (CI), Continuous Delivery (CD) and other aspect of the DevSecOps / MLOps lifecycle into folders to match the Key Areas outlined in the SOO (STATEMENT OF OBJECTIVES).  
 
 
____ 
 
The folders display different capabilities implemented in P1 (Platform One) as outlined below: 
 
1. Architecture (AWS_Architecruree_IaC) - Showcases core AWS Infrastructure creation Terraform Code  
 
2. Security - Showcases core security IaC/CaC for Cloud, Container, OS (Operating System), Security Stack and Zero Trust. 
 
3. Maintainability and Availability (Availability) - Showcases High Availability capabilities at Cloud and Cluster level. 
 
4. Automation (Continuous Delivery) - Showcases the GitOps CD technologies (Flux/Argo). We used Flux (better support for helm) to address the needs of the Platform Engineering persona and Argo (has an UI) for Application Developer persona. 
 
5. Automation (Continuous Integration) - Showcases the CI pipeline stages, and the tools used for Unit testing, Container Build, Software Bill of Materials (SBOM) and Container Scanning.  
 
6. ENBUILD - Showcases our DevSecOps and MLOps accelerator including the ability to create new Catalog Items for different technology stacks. 
 
7. Golden_EC2_AMI - Showcases the packer build automation to create Golden base images.  
 
8. Golden_UBI8_Container_Image - Showcases the build process for the base hardened UBI8 base container image. 
 
9. Logging - Showcases the different logging technologies used within P1 (CloudWatch, Elastic-FluentBit-Kibana (EFK), Grafana-Loki, Splunk, FluentBit). 
 
10. Monitoring - Showcases the different monitoring technologies uses within P1 (Prometheus-Grafana, cis-alarms, Elasticsearch Kibana, metric-alarm, metric-alarms-by-multiple-dimensions, Thanos). 
 
11. MLOps - Showcases the different technologies used in N2X to deploy MLOps (Kubeflow, TensorFlow, PyTorch, Istio, Knative, Kale, Jupyter Notebooks, Katib) 
_____ 
 
### The diagram below highlights the overall architecture of the different technologies separated into the Platform Stack and the Application Stack as deployed at P1. 
 
![DevSecOps](https://user-images.githubusercontent.com/52505604/158180742-96fd974b-ee20-4316-b72b-fce693143794.jpg) 
