#!/usr/bin/env bash

# Run with AWS creds in env vars
# ./account-info-for-nessus.sh
# 
# Run with AWS profile
# ./account-info-for-nessus.sh myawsprofile
#
# Outputs a local file named ACCOUNT_ALIAS.txt e.g. batcave-dev.txt

if [[ -n "${1}" ]]; then
    PROFILE="--profile ${1}"
else
    PROFILE=""
fi

# This will break if we have more than 1 vpc
ACCOUNT_ALIAS=$(aws ${PROFILE} ec2 describe-vpcs --query 'Vpcs[].Tags[?Key==`Name`][].Value' --output text | sed 's/east-//')
ACCOUNT_ID=$(aws ${PROFILE} sts get-caller-identity --query 'Account' --output text)
VPC_ID=$(aws ${PROFILE} ec2 describe-vpcs --query 'Vpcs[].VpcId' --output text)
SUBNETS=$(aws ${PROFILE} ec2 describe-subnets --filters Name=vpc-id,Values=${VPC_ID} --query 'Subnets[].SubnetId')

echo "Account Alias: ${ACCOUNT_ALIAS}" > ./${ACCOUNT_ALIAS}.txt
echo "Account ID: ${ACCOUNT_ID}" >> ./${ACCOUNT_ALIAS}.txt
echo "VPC ID: ${VPC_ID}" >> ./${ACCOUNT_ALIAS}.txt
echo "Subnet IDs: ${SUBNETS}" >> ./${ACCOUNT_ALIAS}.txt
