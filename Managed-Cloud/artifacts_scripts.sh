#!/bin/bash
cd "$WORKSPACE"/zip_content/
zipfile=$(find -iname *.zip | awk -F'/' '{print $NF}')
if [ X"$zipfile" =  X"develop-branch.zip" ]
then
    cd "$WORKSPACE"/REAN-Managed-Cloud
    commit_dev=$(git rev-parse --short origin/develop)
    git diff-tree --name-only "$commit_dev" > CommitDetails
    latest_commit=$(head -n1 CommitDetails)
    file_name=$(tail -n1 CommitDetails)
    commit_date=$(git show -s --format=%ci "$commit_dev" --date=short --pretty=format:%cd)
    commit_time=$(git show -s --format=%ci "$commit_dev" | awk -F' ' '{print $2}')
    zip_file_name="$file_name"_"$commit_dev"_"$commit_date"-"$commit_time".zip
    mv "$WORKSPACE"/zip_content/develop-branch.zip "$zip_file_name"
    set -e
    TMP_CREDS=`aws sts assume-role --role-arn "$crossaccount_role_arn" --role-session-name ManagedCloud`
    export AWS_SECRET_ACCESS_KEY=$(echo "$TMP_CREDS" | jq -r .Credentials.SecretAccessKey)
    export AWS_ACCESS_KEY_ID=$(echo "$TMP_CREDS" | jq -r .Credentials.AccessKeyId)
    export AWS_SESSION_TOKEN=$(echo "$TMP_CREDS" | jq -r .Credentials.SessionToken)
    aws s3 cp "$zip_file_name" s3://"${destBucket}/${developDestPath}/$zip_file_name"
    echo "artitacts sent to s3 Develop folder" 
else
    cd "$WORKSPACE"/REAN-Managed-Cloud
    commit_mas=$(git rev-parse --short origin/master)
    echo "$commit_mas"
    git diff-tree --name-only "$commit_mas" > CommitDetails
    file_name=$(tail -n1 CommitDetails)
    zip_file_name="$file_name"_"$git_tag".zip
    mv "$WORKSPACE"/zip_content/master-branch.zip "$zip_file_name"
    set -e
    TMP_CREDS=`aws sts assume-role --role-arn "$crossaccount_role_arn" --role-session-name DeployNow`
    export AWS_SECRET_ACCESS_KEY=$(echo "$TMP_CREDS" | jq -r .Credentials.SecretAccessKey)
    export AWS_ACCESS_KEY_ID=$(echo "$TMP_CREDS" | jq -r .Credentials.AccessKeyId)
    export AWS_SESSION_TOKEN=$(echo "$TMP_CREDS" | jq -r .Credentials.SessionToken)
    aws s3 cp "$zip_file_name" s3://"${destBucket}/${masterDestPath}/$zip_file_name"
    echo "artitacts sent to s3 Master folder"
    if [ $(git tag | grep "$zip_file_name") ]
    then
        echo "tag named $zip_file_name already exists"
    else
        echo "tag named $zip_file_name pushed in to the repository"
        git tag "$zip_file_name"
        git push origin "$zip_file_name"
    fi
fi
