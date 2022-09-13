resource "aws_efs_access_point" "this_efs_accesspoint"{
  count = var.create_efs ? 1 : 0
  file_system_id = var.efs_id
  posix_user {
    gid = var.gid
    secondary_gids = var.secondary_gids
    uid = var.uid
  }
  root_directory {
    path = var.mount_path
    creation_info {
      owner_gid = var.gid
      owner_uid = var.uid
      permissions = 0755
    }
  }
  tags = {
    Name = "${var.name}-efs-accesspoint"
  }
}