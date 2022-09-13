# TFsec

TFSec is a tool to scan terraform files for potential security vulnerabilities.
`"tfsec uses static analysis of your terraform templates to spot potential security issues"`

Upstream documentation can be found [here](https://github.com/tfsec/tfsec).

## Features

- Checks for sensitive data inclusion across all providers
- Checks for violations of AWS, Azure and GCP security best practice recommendations
- Scans modules (currently only local modules are supported)
- Evaluates expressions as well as literal values
- Evaluates Terraform functions e.g. concat()
