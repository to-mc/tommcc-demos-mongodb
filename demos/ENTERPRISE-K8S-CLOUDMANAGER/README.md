# Instructions

## Create cluster in AWS

1. Login to AWS `aws sso login --profile SA`
2. Create eks cluster in AWS with 3x t3.large `eksctl --profile SA create cluster -f ../../resources/eks-cluster-setup/eksconfig.yaml`
3. Set up kubectl config: `eksctl --profile SA utils write-kubeconfig --cluster=tommcc-cluster`. 
4. If session times out (kubectl commands fail), refresh it with `aws sso login --profile SA`.

---

1. install the k8s operator helm repo: `helm repo add mongodb https://mongodb.github.io/helm-charts.`
2. install the k8s operator: `helm install enterprise-operator mongodb/enterprise-operator --namespace mongodb --create-namespace`
3. Create api credentials in cloud manager (make sure access list is correct, you can use local range for k8s cluster eg `10.0.0.0/16`) and create a k8s secret with them:
```
kubectl -n mongodb \
create secret generic cm-credentials \
--from-literal="publicKey=<PUBLICAPIKEY>" \
--from-literal="privateKey=<PRIVATEAPIKEY>"
```  
5. Apply kubernetes resources `kubectl apply -f . --namespace mongodb`

---

1.  Connect to pod `kubectl --namespace mongodb exec -it mongosh -- bash`
2.  Connect to the server using the k8s service eg: `mongosh "mongodb+srv://prod-db-cm-svc.mongodb.svc.cluster.local/?tls=false&ssl=false" --username prod-user`