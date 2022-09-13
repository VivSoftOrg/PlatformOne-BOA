output "efs-id" {
  value = var.create_efs ? aws_efs_file_system.this_efs[0].id : 0
}