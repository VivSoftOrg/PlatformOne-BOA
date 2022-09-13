# ECK Operator

## Overview 

This package/repo contains customizable installation chart for Elastic Cloud on Kubernetes(ECK) operator. This package is based on the upstream [chart](https://github.com/elastic/cloud-on-k8s) provided by Elastic. 

## ECK-Operator

[ECK](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_learn_more_about_eck.html) gives users the complete Elastic experience on Kubernetes, including features and capabilities that you can only get from Elastic such as APM, Logs, Metrics, SIEM, Canvas, Lens, machine learning, and index lifecycle management. With ECK you can extend the basic Kubernetes orchestration capabilities to easily deploy, secure, upgrade your Elasticsearch cluster, and much more.

## How it works

When installed, ECK-Operator allows you to create configurable deployments of Elasticsearch, Kibana, APM Server, Enterprise Search, and Beats utilizing the Custom Resource Definitions maintained by Elastic. This chart includes the CRDs along with a single operator pod responsible for creating and managing these resources. This chart is to be paired with the [Elasticsearch-Kibana](https://repo1.dso.mil/platform-one/big-bang/apps/core/elasticsearch-kibana/) package also provided by BigBang.

### Additional Links

- [Elstic official website](https://www.elastic.co/)
- [Elastic Forum](https://discuss.elastic.co/c/orchestration/eck/79)
