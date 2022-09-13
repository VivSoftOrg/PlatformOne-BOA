output "auditinfra_role_arn" {
  value = "${aws_iam_role.auditinfra.arn}"
}

output "auditinfra_instance_profile_name" {
  value = "${aws_iam_role.auditinfra.name}"
}

output "tfdeploy_role_arn" {
  value = "${aws_iam_role.tfdeploy.arn}"
}

output "tfdeploy_instance_profile_name" {
  value = "${aws_iam_role.tfdeploy.name}"
}

output "sshkeys_kms_key_id" {
  value = "${aws_kms_key.ssh-keys.id}"
}

output "sshkeys_kms_key_arn" {
  value = "${aws_kms_key.ssh-keys.arn}"
}

output "aws_region" {
  value = "${data.aws_region.current.name}"
}

output "keypair_name" {
  value = "${aws_key_pair.workloadkey.key_name}"
}

output "s3-shared_role_arn" {
  value = "${aws_iam_role.s3-shared.arn}"
}

output "s3-shared_instance_profile_name" {
  value = "${aws_iam_role.s3-shared.name}"
}

output "s3-shared_iam_policy_arn" {
  value = "${aws_iam_policy.s3-shared.arn}"
}
