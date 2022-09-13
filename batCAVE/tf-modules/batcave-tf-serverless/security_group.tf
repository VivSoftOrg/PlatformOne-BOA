# NOTE: Lambda ENIs can take up to 45 minutes to delete
#  So when blowing away this module, be prepared for it to take a while
#  Alternately, search ENIs for the security group ID and delete them
#  manually while you wait
resource "aws_security_group" "lambda" {
  name        = "${var.service_name}-alb-lambda"
  description = "Security group for ${var.service_name}"
  vpc_id      = local.vpc_id

  provisioner "local-exec" {
    ## https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group#timeouts
    ## ENIs created by lambda can take up to 45 minutes to destroy.
    ## This destroy-time local-exec will (hopefully) just delete them by hand before the SG gets destroyed
    when    = destroy
    command = "aws ec2 describe-network-interfaces --filters Name=group-id,Values=${self.id} --query NetworkInterfaces[].NetworkInterfaceId --output text | xargs -n1 aws ec2 delete-network-interface --network-interface-id || true"
  }
}

resource "aws_security_group_rule" "egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.lambda.id
}

resource "aws_security_group_rule" "ingress_cidrs" {
  count             = length(var.ingress_cidrs) > 0 ? 1 : 0
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = var.ingress_cidrs
  security_group_id = aws_security_group.lambda.id
}
resource "aws_security_group_rule" "ingress_prefix_list" {
  count             = length(var.ingress_prefix_lists) > 0 ? 1 : 0
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  prefix_list_ids   = var.ingress_prefix_lists
  security_group_id = aws_security_group.lambda.id
}

resource "aws_security_group_rule" "https-ingress" {
  for_each = toset(var.ingress_sgs)
  description = "allow ingress from lambda"
  type = "ingress" 
  to_port = 443
  from_port = 443
  protocol = "TCP"
  security_group_id = each.key
  source_security_group_id = aws_security_group.lambda.id
}
