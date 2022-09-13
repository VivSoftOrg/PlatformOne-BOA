output "aws_efs_access_point"{
  value = var.create_efs ? "${var.efs_id}::${aws_efs_access_point.this_efs_accesspoint[0].id}" : 0
}