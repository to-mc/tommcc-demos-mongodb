# Instructions

1. Create EKS cluster using `../../resources/eks-cluster-setup/README.md` (or use a local cluster with kind/minikube)

---

1. install the k8s operator helm repo: `helm repo add mongodb https://mongodb.github.io/helm-charts`
2. install the k8s operator: `helm install atlas-operator --namespace=mongodb --create-namespace mongodb/mongodb-atlas-operator`
3. Create and label a secret with API keys from atlas (access list is required, use public IPs from eks workers)
```
kubectl create secret generic mongodb-atlas-operator-api-key \
         --from-literal="orgId=$ATLAS_ORG_ID" \
         --from-literal="publicApiKey=$ATLAS_PUBLIC_KEY" \
         --from-literal="privateApiKey=$ATLAS_PRIVATE_KEY" \
         -n mongodb

kubectl label secret mongodb-atlas-operator-api-key atlas.mongodb.com/type=credentials -n mongodb
```

4. Deploy resources: `kubectl apply -f .`
5. Connect to mongosh pod: `kubectl exec -n mongodb --stdin --tty mongosh-atlas -- /bin/bash`
6. Connect from pod to mongodb: `mongosh $CONNECTIONSTRING`