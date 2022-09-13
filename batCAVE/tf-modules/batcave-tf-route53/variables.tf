variable "hosted_zone_dns" {
  description = "base domain associated with the private hosted zone for this account"
  default     = ""
}

variable "endpoint_subdomain_map" {
  type        = map(any)
  description = "Map of type: {public:{endpoint: <lb-dns>, subdomains: [\"subdomain1\", \"subdomain2\"]}}"
}

variable "ttl" {
  default = "60"
}
