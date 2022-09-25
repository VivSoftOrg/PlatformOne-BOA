#!/bin/bash
loadbalancers=$(aws elb describe-load-balancers | jq '.LoadBalancerDescriptions[].LoadBalancerName' | xargs aws elb describe-tags --load-balancer-names | jq '.TagDescriptions | map_values({name: .LoadBalancerName, tags: .Tags | from_entries})[] | select(.tags."kubernetes.io/service-name" == "istio-system/istio-ingressgateway") | {(.name): (.tags|keys[]|select(.|test("kubernetes.io/cluster/.*"))|sub("kubernetes.io/cluster/";""))} | "\(.|keys[0]),\(.|flatten[0])"'|sed 's/"//g')
clusters=$(aws eks list-clusters --query clusters)

for loadbalancer in $loadbalancers; do
  lb=$(echo $loadbalancer | cut -d, -f1)
  name=$(echo $loadbalancer | cut -d, -f2)
  echo "lb: $lb"
  echo "lb: $name"
  if aws eks describe-cluster --name $name > /dev/null; then
    echo "Cluster $name exists, not deleting ELB $lb"
  else
    echo "Cluster $name does not exist, deleting ELB $lb"
    aws elb delete-load-balancer --load-balancer-name $lb
  fi
done
echo "Deleting unattached k8s-elb security groups..."
aws ec2 describe-security-groups --filters "Name=group-name,Values=k8s-elb-*" --query "SecurityGroups[].GroupId" --output=text | xargs -n1 aws ec2 delete-security-group --group-id 2>/dev/null
echo "Done."
