#!/bin/bash
PS3='Main menu. Choose one of the following: '
        state=("MDO Test" "MGMT Test" "MDO Staging IL5" "MDO Staging IL4" "MDO Staging IL2" "MDO Prod IL5" "MDO Prod IL4" "MDO Prod IL2" "MGMT Prod IL5" "MGMT Prod IL4" "MGMT Prod IL2" "Cycle istio pods" "Quit")
        while :; do
        select desired in "${state[@]}"; do
            case $desired in
############################                
                "MDO Test")
                    cluster="mdo-mission-il2-test"
                    echo -e "Connecting to $cluster . . ."
                    kubectl config use-context $cluster
                    kubectl cluster-info
                    echo -e "Are you here to 1)Create MR 2)Reconcile"
                    read input
                        if [ "$input" == "2" ]; then
                            cd "$CURRENT_DIR" && cd .. reconcile-bb.sh
                            echo -e "Is istio being updated in this release?(y/n)"
                            read input
                                if [ "$input" != "n" ]; then
                                    cd "$CURRENT_DIR" && cd .. && cd cycle-istio-pods/mdo-environments/test && ./il2.sh
                                    echo "Watching helm release status..."
                                    watch flux get hr -n bigbang
                                    
                                fi
                        elif [ "$input" == "1" ]; then
                            echo -e "Verifying if flux update is needed . . ."
                            cd "$CURRENT_DIR" && cd .. && cd flux-updater
                            echo -e "Pulling the version number from the BB release API . . ."
                            version=$(curl "https://repo1.dso.mil/api/v4/projects/2872/releases" | jq . | grep -o -m 1 '\d.\d\d.\d')
                            envname=".staging.env"
                            echo -e "Updating the version number in$envnamefile . . ."
                            perl -i -pe "s/BIGBANG_TAG.*/BIGBANG_TAG=\"$version\"/" $envname
                            ./updater_for_automation.sh .staging.env
                            kubectl get deploy -n flux-system kustomize-controller -o yaml | grep app.kubernetes.io/version
                            echo -e "Moving on to creating MR . . . "
                            echo -e "${yellow}Creating a workdir folder . . ."
                            rm -rf /tmp/workdir
                            mkdir -p /tmp/workdir
                            cd /tmp/workdir
                            echo -e "Cloning repo . . ."
                            git clone https://code.il2.dso.mil/platform-one/devops/mission-bootstrap/testing-mission-bootstrap.git
                            cd testing-mission-bootstrap
                            echo -e "Pulling to update local branch . . ."
                            git pull
                            echo -e "Fetching all remote branches into your local repo . . ."
                            git fetch origin
                            echo -e "Checking out to master . . ."
                            git checkout master
                            echo -e "Pulling the version number from the BB release API . . ."
                            version=$(curl "https://repo1.dso.mil/api/v4/projects/2872/releases" | jq . | grep -o -m 1 '\d.\d\d.\d')
                            echo -e "Checking out a new branch . . ."
                            git checkout -b test-bb-upgrade-$version
                            echo -e "Updating the version number in gitrepository.yaml file . . ."
                            filename="bigbang/core/base/gitrepository.yaml"
                            perl -i -pe "s/tag.*/tag: \"$version\"/" $filename
                            echo -e "Adding the changes . . ."
                            git add .
                            echo -e "Commiting the changes. . ."
                            git commit -m "test upgrade bb "
                            echo -e "Pushing the changes to the remote repo . . ."
                            #git push --set-upstream origin test-bb-upgrade-$version
                            git push --set-upstream origin test-bb-upgrade-$version -o merge_request.create -o merge_request.title="test upgrade bb $version"
                            cd "$CURRENT_DIR"
                            echo -e "Removing workdir folder . . . "
                            rm -rf /tmp/workdir
                        fi
