output "dockerhost_role_arn" {
  value = "${aws_iam_role.dockerhost.arn}"
}

output "dockerhost_instance_profile_name" {
  value = "${aws_iam_role.dockerhost.name}"
}

output "dockerhost-attachebs_policy_name" {
  value = "${aws_iam_policy.dockerhost-attachebs.name}"
}

output "dockerhost-s3-access_policy_name" {
  value = "${aws_iam_policy.dockerhost-s3-access.name}"
}

output "viv_softjenkins_role_arn" {
  value = "${aws_iam_role.viv_softjenkins.arn}"
}

output "viv_softjenkins_instance_profile_name" {
  value = "${aws_iam_role.viv_softjenkins.name}"
}

output "viv_softjenkins_instance_ebs_policy_name" {
  value = "${aws_iam_policy.viv_softjenkins-attachebs.name}"
}

output "viv_softjenkins_instance_core_policy_name" {
  value = "${aws_iam_policy.viv_softjenkins-assumerole-core.name}"
}

output "aws_region" {
  value = "${data.aws_region.current.name}"
}

output "sshkeys_kms_key_id" {
  value = "${aws_kms_key.ssh-keys.id}"
}

output "sshkeys_kms_key_arn" {
  value = "${aws_kms_key.ssh-keys.arn}"
}

output "sshkeys_kms_alias_name" {
  value = "${aws_kms_alias.ssh-keys.name}"
}

output "rds_kms_key_id" {
  value = "${aws_kms_key.rds.id}"
}

output "rds_kms_key_arn" {
  value = "${aws_kms_key.rds.arn}"
}

output "rds_kms_alias_name" {
  value = "${aws_kms_alias.rds.name}"
}

output "ebs_kms_key_id" {
  value = "${aws_kms_key.ebs.id}"
}

output "ebs_kms_key_arn" {
  value = "${aws_kms_key.ebs.arn}"
}

output "ebs_kms_alias_name" {
  value = "${aws_kms_alias.ebs.name}"
}

output "keypair_name" {
  value = "${aws_key_pair.corekey.key_name}"
}

output "elb_access_logs_bucket" {
  value = "${aws_s3_bucket.elb_access_logs_bucket.id}"
}

output "elb_logs_policy" {
  value = "${aws_s3_bucket_policy.elb_logs.policy}"
}

output "cloudwatch_logs_write_access_policy_name" {
  value = "${aws_iam_policy.cloudwatch_logs_write_access-policy.arn}"
}

output "ssm_core_policy_arn" {
  value = "${join(",", aws_iam_policy.ssm_core_policy.*.arn)}"
}
