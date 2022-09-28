Creates an Atlas cluster and a flask app which connects to it. Uses ./resources/flask-app-demo


# REQs

- k8s cluster (kind works)
- Set context in kubectl: `k config use-context kind-kind` && `k config set-context --current --namespace=default`
- Load the docker image to kind cluster: `kind load docker-image python-docker:latest --name mongod`
- Create Atlas credentials:

```
kubectl create secret generic mongodb-atlas-operator-api-key \
         --from-literal="orgId=$ATLAS_ORG_ID" \
         --from-literal="publicApiKey=$ATLAS_PUBLIC_KEY" \
         --from-literal="privateApiKey=$ATLAS_PRIVATE_KEY" \
         -n mongodb-atlas-system
kubectl label secret mongodb-atlas-operator-api-key atlas.mongodb.com/type=credentials -n mongodb-atlas-system

kubectl create secret generic the-user-password --from-literal="password=<somePassword>"
kubectl label secret the-user-password atlas.mongodb.com/type=credentials
```

- If k8s cluster doesn't have flux set up yet:
```
cd .ssh

flux create secret git flask-app-auth \
    --url=ssh://git@github.com/cakepietoast/flask-mongodb-example \
    --private-key-file=id_new


flux bootstrap github \
  --owner=$GITHUB_USER \
  --repository=fleet-infra \
  --branch=main \
  --path=./clusters/my-cluster \
  --personal
  ```


# BOOTSTRAP

https://fluxcd.io/flux/get-started/



# INSTRUCTIONS


Run a k8s cluster with kind (kind create cluster)

Watch for changes: flux get kustomizations --watch

Add a document in the test.messages collection in the created db: `{"message": "hello world"}`


Suspend atlas: flux suspend kustomization infrastructure