data "aws_eks_cluster_auth" "cluster" {
  name = var.cluster_name
}

provider "kubernetes" {
  host                   = var.cluster_endpoint
  cluster_ca_certificate = base64decode(var.cluster_certificate_authority_data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

resource "kubernetes_config_map" "configmap" {
  metadata {
    name      = var.configmap_name
    namespace = var.configmap_namespace
    labels = merge(
      {
        "app.kubernetes.io/managed-by" = "Terraform"
      }, var.configmap_labels
    )
  }
  data = var.configmap_data
}
