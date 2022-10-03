# Instructions

## Create cluster in AWS

1. Create EKS cluster using `../../resources/eks-cluster-setup/README.md`

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

## Optional

### Connect with mongosh
1. Connect to mongosh pod: `kubectl exec -n mongodb --stdin --tty mongosh-cm -- /bin/bash`
2. Connect from pod to mongodb: `mongosh "$CONNECTIONSTRING&tls=False"`


### Load sample dataset
1. `git clone https://github.com/cakepietoast/mongodb-sample-dataset.git && cd mongodb-sample-dataset`
2. `bash script.sh "mongodb+srv://prod-db-om-svc.mongodb.svc.cluster.local/?tls=false&ssl=false" prod-user prod-password`

### Deploy sample app
1.  Deploy the flask app: `kubectl apply -f ../../resources/flask-mongodb-example/ -n mongodb`