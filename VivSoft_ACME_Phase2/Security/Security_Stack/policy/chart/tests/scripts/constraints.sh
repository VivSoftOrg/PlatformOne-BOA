#!/bin/bash

echo "Test 1: Detect missing constraints with bad k8s objects"
echo "*Apply bad k8s objects*"
violations=$(kubectl apply -n default -f /yaml/bad.yaml 2>&1)

for constraint in $(kubectl get constraints -o jsonpath='{range .items[*]}{@.kind}{","}{@.metadata.name}{","}{@.spec.enforcementAction}{"\n"}{end}');
do
# Get all constraints that are set to deny
if [[ $(echo $constraint | cut -d "," -f 3) == "deny" ]]; then
  constraintKind=$(echo $constraint | cut -d "," -f 1)
  constraintName=$(echo $constraint | cut -d "," -f 2)
fi
if [[ ! $violations == *"$constraintName"* && ! "$constraintName" == "allowed-proc-mount" ]]; then
  missing_violation="true"
  echo "MISSING VIOLATION: Constraint $constraintKind/$constraintName"
  echo "${constraint}"
fi
done

if [[ $missing_violation == "true"  ]]; then
  #Due to formatting issue
  echo -e "\n**ALL VIOLATIONS: **"
  kubectl apply -n default -f /yaml/bad.yaml
  echo -e "\n"
  kubectl get all -n default
  echo -e "\nSome constraints are missing violations on bad k8s objects"
  echo "Test 1: Failed"
else
  echo "Test 1: Passed"
fi
echo "*Delete created k8s objects*"
kubectl delete -n default -f /yaml/bad.yaml || true


echo -e "\n\nTest 2: Detect constraints violations with good k8s objects"
echo "*Apply good k8s objects*"

violations=$(kubectl apply -n default -f /yaml/good.yaml 2>&1)

for constraint in $(kubectl get constraints -o jsonpath='{range .items[*]}{@.kind}{","}{@.metadata.name}{","}{@.spec.enforcementAction}{"\n"}{end}');
do
# Get all constraints that are set to deny
if [[ $(echo $constraint | cut -d "," -f 3) == "deny" ]]; then
  constraintKind=$(echo $constraint | cut -d "," -f 1)
  constraintName=$(echo $constraint | cut -d "," -f 2)
fi
if [[ $violations == *"$constraintName"* && ! "$constraintName" == "host-networking" ]]; then
  found_violation="true"
  echo "Found Constraint $constraintKind/$constraintName violation"
  echo "${constraint}"
fi
done

if [[ $found_violation == "true"  ]]; then
  echo -e "\n**ALL VIOLATIONS: **"
  kubectl apply -n default -f /yaml/good.yaml
  echo -e "\n"
  kubectl get all -n default
  echo "\nConstraints violation found on good k8s objects"
  echo "Test 2: Failed"
else
  echo "Test 2: Passed"
fi

#check number of good objects created
objects_created=$(kubectl get ns,pod,svc,ingress -n default -oname -l app.kubernetes.io/name=cluster-auditor | wc -l)
objects_expected="5"

echo "*Delete created k8s objects*"
kubectl delete -n default -f /yaml/good.yaml || true

if [[ $missing_violation == "true" || $found_violation == "true"  ]]; then
  echo -e "\nConclusion: Test Failed"
  exit 1
elif test "$objects_created" -eq "$objects_expected"; then
  echo -e "\nConclusion: Test Passed"
fi
