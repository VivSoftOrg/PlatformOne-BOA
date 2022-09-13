# Utilize the image from download.yaml
# This is because we need to download the latest image from Red Hat. Current
# implementation for doing ARG based FROM instructions require replacing
# the FROM with an already existing image (i.e. one we've previously built).
# This prevents us from retrieving the latest image from Red Hat.
FROM registry.access.redhat.com/ubi8:8.5

COPY scripts /scripts/

COPY nssdb/pkcs11.txt /tmp/pkcs11.txt

COPY certs/Certificates_PKCS7_v5.9_DoD.pem /etc/pki/ca-trust/source/anchors/Certificates_PKCS7_v5.9_DoD.pem
COPY certs/Certificates_PKCS7_v5.12_WCF.pem /etc/pki/ca-trust/source/anchors/Certificates_PKCS7_v5.12_WCF.pem

COPY banner/issue /etc/

# Be careful when adding packages because this will ultimately be built on a licensed RHEL host,
# which enables full RHEL repositories and could allow for installation of packages that would
# violate Red Hat license agreement when running the container on a non-RHEL licensed host.
# See the following link for more details:
# https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/building_running_and_managing_containers/index/#add_software_to_a_running_ubi_container
RUN echo Update packages and install DISA STIG fixes && \
    # Disable all repositories (to limit RHEL host repositories) and only use official UBI repositories
    sed -i "s/enabled=1/enabled=0/" /etc/dnf/plugins/subscription-manager.conf && \
    # exclude upating the 'filesystem' package due to errors with rootless builds
    #     https://github.com/containers/buildah/issues/3309
    # exclude subscription-manager updates due to missing cloud-what dep in UBI repo
    echo "exclude=filesystem-*" >> /etc/dnf/dnf.conf && \
    chmod 644 /etc/issue /etc/pki/ca-trust/source/anchors/*.pem && \
    dnf repolist && \
    dnf update -y && \
    # install missing dependency for libpwquality
    dnf install -y cracklib-dicts nss && \
    echo "* hard maxlogins 10" > /etc/security/limits.d/maxlogins.conf && \
    /scripts/xccdf_org.ssgproject.content_rule_account_disable_post_pw_expiration.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_logon_fail_delay.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_max_concurrent_login_sessions.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_maximum_age_login_defs.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_minimum_age_login_defs.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_password_minlen_login_defs.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_password_pam_dcredit.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_password_pam_dictcheck.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_password_pam_difok.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_password_pam_lcredit.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_password_pam_maxclassrepeat.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_password_pam_maxrepeat.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_password_pam_minclass.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_password_pam_minlen.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_password_pam_ocredit.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_password_pam_pwhistory_remember_password_auth.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_password_pam_pwhistory_remember_system_auth.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_password_pam_ucredit.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_password_pam_unix_remember.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny_root.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_interval.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_unlock_time.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_umask_etc_bashrc.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_umask_etc_csh_cshrc.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_umask_etc_login_defs.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_accounts_umask_etc_profile.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_banner_etc_issue.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_configure_kerberos_crypto_policy.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_configure_openssl_crypto_policy.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_coredump_disable_backtraces.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_coredump_disable_storage.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_disable_ctrlaltdel_burstaction.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_disable_users_coredumps.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_display_login_attempts.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_ensure_gpgcheck_local_packages.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_file_groupownership_system_commands_dirs.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_network_configure_name_resolution.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_no_empty_passwords.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_openssl_use_strong_entropy.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_package_crypto-policies_installed.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_package_iptables_installed.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_configure_crypto_policy.sh && \
    /scripts/xccdf_org.ssgproject.content_rule_configure_kerberos_crypto_policy.sh && \
    cat /tmp/pkcs11.txt >> /etc/pki/nssdb/pkcs11.txt && \
    chown -R root:root /etc/pki/nssdb && \
    chmod 644 /etc/pki/nssdb/* && \
    update-ca-trust && \
    update-ca-trust force-enable && \
    dnf clean all && \
    rm -rf /scripts/ /var/cache/dnf/ /var/tmp/* /tmp/* /tmp/pkcs11.txt /var/tmp/.???* /tmp/.???*

ENV container oci
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

CMD ["/bin/bash"]
