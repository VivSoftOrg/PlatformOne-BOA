#!/bin/bash
mkdir zip_content
cd REAN-Managed-Cloud
commit_dev=$(git rev-parse origin/develop)
commit_mas=$(git rev-parse origin/master)
git rev-list --remotes > latest_commit
branch_commit=$(head -n1 latest_commit)
if [ X"$branch_commit" = X"$commit_mas" ]
then 
    echo "master branch have the latest commit"
    git checkout master
    find . -type d -not -iwholename '*.git*' -not -iwholename '.' -not -iwholename 'tests' -exec mv -t "$WORKSPACE/zip_content" {} +
    find . -type f -name 'main.py' -exec mv -t "$WORKSPACE/zip_content" {} +
    cd "$WORKSPACE"/zip_content/
    zip -r master-branch.zip .
    echo "master branch is zipped"
    
else
    echo "develop branch have the latest commit"
    git checkout develop
    find . -type d -not -iwholename '*.git*' -not -iwholename '.' -not -iwholename 'tests' -exec mv -t "$WORKSPACE/zip_content" {} +
    find . -type f -name 'main.py' -exec mv -t "$WORKSPACE/zip_content" {} +
    cd "$WORKSPACE"/zip_content/
    zip -r develop-branch.zip .
    echo "develop branch is zipped"
fi  
