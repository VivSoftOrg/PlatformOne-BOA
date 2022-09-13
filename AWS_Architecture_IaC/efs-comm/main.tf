resource "aws_efs_file_system" "this_efs" {
  count = var.create_efs ? 1 : 0

  creation_token   = "${var.name}--efs"
  performance_mode = "generalPurpose"
  throughput_mode  = "bursting"
  encrypted        = "true"
  tags = {
    Name = "${var.name}-efs"
  }
}

resource "aws_efs_mount_target" "this_efs_mount_target" {
  count = var.create_efs ? length(var.subnet_ids) : 0

  file_system_id = aws_efs_file_system.this_efs[0].id
  subnet_id      = var.subnet_ids[count.index]

  security_groups = [aws_security_group.efs_security_group[0].id]
}

resource "aws_security_group" "efs_security_group" {
  count       = var.create_efs ? 1 : 0 
  name        = "${var.name}-efs-sg"
  description = "${var.name} EFS SG"
  vpc_id      = var.vpc_id
}

resource "aws_security_group_rule" "efs-ingress" {
  count = var.create_efs ? length(var.access_sg_ids) : 0

  type                     = "ingress"
  description              = "efs traffic ingress"
  from_port                = 2049
  to_port                  = 2049
  protocol                 = "tcp"
  security_group_id        = aws_security_group.efs_security_group[0].id
  source_security_group_id = var.access_sg_ids[count.index]
}

resource "aws_iam_role_policy_attachment" "attach-workers-efs" {
  count = var.iam_role == "" ? 1 : 0

  role       = "${var.cluster_name}-p1-k8s-workers"
  policy_arn = aws_iam_policy.workers-efs[count.index].arn
}

resource "aws_iam_policy" "workers-efs" {
  count = var.iam_role == "" ? 1 : 0

  name   = "${var.cluster_name}-p1-k8s-workers-efs"
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "elasticfilesystem:DescribeFileSystems"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}