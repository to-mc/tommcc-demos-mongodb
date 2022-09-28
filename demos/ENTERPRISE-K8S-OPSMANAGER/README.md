

## Create cluster in AWS

1. Login to AWS `aws sso login --profile SA`
2. Create eks cluster in AWS with 3x t3.large `eksctl --profile SA create cluster -f ../../resources/eks-cluster-setup/eksconfig.yaml`
3. Set up kubectl config: `eksctl --profile SA utils write-kubeconfig --cluster=tommcc-cluster`. 
4. If session times out (kubectl commands fail), refresh it with `aws sso login --profile SA`.

---

1. install the k8s operator helm repo: `helm repo add mongodb https://mongodb.github.io/helm-charts`
2. install the k8s operator: `helm install enterprise-operator mongodb/enterprise-operator --namespace mongodb --create-namespace`
3. Create admin user for ops manager, make sure password is 8 chars with number & symbol
    ```
    kubectl create secret generic admin-user-credentials \
    --from-literal=Username="<username>" \
    --from-literal=Password="<password>" \
    --from-literal=FirstName="<firstname>" \
    --from-literal=LastName="<lastname>"
    ```
 
4. Apply kubernetes resources `kubectl apply -f . --namespace mongodb`
5. Once ops manager is up, you'll need to create api credentials in ops manager (org level) and create a k8s secret with them:
```
kubectl -n mongodb \
create secret generic om-credentials \
--from-literal="publicKey=<PUBLICAPIKEY>" \
--from-literal="privateKey=<PRIVATEAPIKEY>"
```
6. Update `project-configmap.yaml` with orgId from ops manager (shouldn't need to do this but can't figure out why it doesn't work without it)

---


## Optional

### Connect with mongosh
1. Connect to pod `kubectl --namespace mongodb exec -it mongosh -- bash`
2. Connect to the server using the k8s service eg: `mongosh "mongodb+srv://prod-db-om-svc.mongodb.svc.cluster.local/?tls=false&ssl=false" --username prod-user`

### Load sample dataset
1. `git clone https://github.com/cakepietoast/mongodb-sample-dataset.git && cd mongodb-sample-dataset`
2. `bash script.sh "mongodb+srv://prod-db-om-svc.mongodb.svc.cluster.local/?tls=false&ssl=false" prod-user prod-password`