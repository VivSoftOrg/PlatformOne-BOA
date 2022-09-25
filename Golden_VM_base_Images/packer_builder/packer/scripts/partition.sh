#!/bin/bash
set -x

yum update -y
yum install -y lvm2

dev="/dev/nvme1n1"
mntpoint="/mnt"

parted -a optimal "${dev}" mklabel gpt print || \
exit 1

parted -a optimal "${dev}" mkpart primary '0%' '100%' set 1 lvm on print

partprobe

mkfs.xfs "${dev}p1" -f

pvcreate "${dev}p1" -f
vgcreate vol_grp "${dev}p1"

lvcreate -L 4G -n lv_var vol_grp
lvcreate -L 4G -n lv_varlog vol_grp
lvcreate -L 8G -n lv_varlogaudit vol_grp

mkfs.xfs /dev/mapper/vol_grp-lv_var
mkfs.xfs /dev/mapper/vol_grp-lv_varlog
mkfs.xfs /dev/mapper/vol_grp-lv_varlogaudit

mkdir -p ${mntpoint}/var
mount /dev/mapper/vol_grp-lv_var ${mntpoint}/var

mkdir -p ${mntpoint}/var/log
mount /dev/mapper/vol_grp-lv_varlog ${mntpoint}/var/log

mkdir -p ${mntpoint}/var/log/audit
mount /dev/mapper/vol_grp-lv_varlogaudit ${mntpoint}/var/log/audit

# Copy all data over to new mount point
rsync -axHAX --exclude={"/var/log"} /var ${mntpoint}

umount -l /mnt/var

# Ensure mounts persist through reboot
echo "/dev/mapper/vol_grp-lv_var /var xfs rw,relatime   0 0" >> /etc/fstab
echo "/dev/mapper/vol_grp-lv_varlog /var/log xfs  rw,relatime   0 0" >> /etc/fstab
echo "/dev/mapper/vol_grp-lv_varlogaudit /var/log/audit xfs  rw,relatime   0 0" >> /etc/fstab

reboot