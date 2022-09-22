1. Create eks cluster in AWS with 3x t3.large and set up kubectl (TODO replace this with CDK!). If session times out, `aws sso login --profile SA`.
2. install the k8s operator helm repo: `helm repo add mongodb https://mongodb.github.io/helm-charts`
3. install the k8s operator: `helm install enterprise-operator mongodb/enterprise-operator --namespace mongodb --create-namespace`
4. Create admin user, make sure password is 8 chars with number & symbol
    ```
    kubectl create secret generic <adminusercredentials> \
    --from-literal=Username="<username>" \
    --from-literal=Password="<password>" \
    --from-literal=FirstName="<firstname>" \
    --from-literal=LastName="<lastname>"
    ```
5. Deploy OM: `kubectl apply -f om.yaml --namespace mongodb`
6. Update `project-configmap.yaml` with the baseUrl (from OM loadbalancer service) and org/project ids
7. `kubectl apply -f project-configmap.yaml --namespace mongodb`
8. Create api credentials in ops manager (org level) and create a k8s secret with them (note: the naming is confusing...):
```
kubectl -n mongodb \
create secret generic om-credentials \
--from-literal="user=<PUBLICAPIKEY>" \
--from-literal="publicApiKey=PRIVATEAPIKEY"
```  
10. `kubectl apply -f database-instance.yaml --namespace mongodb`
11. Create more databases or edit the initial (eg increase members)
12. Run the debug (mongosh) pod `kubectl apply -f mongosh-pod.yaml --namespace mongodb` 
13. Connect to pod `kubectl --namespace mongodb exec -it mongosh -- bash`
14. Connect to the server using the k8s service (you'l also need to enable auth (SCRAM-SHA1) and create a user) eg: `mongosh "mongodb+srv://db-created-with-operator-svc.mongodb.svc.cluster.local/?tls=false&ssl=false" --username admin`