Creates an Atlas cluster and a flask app which connects to it. Uses ./resources/flask-app-demo


# REQs

- k8s cluster (kind works)
  - Set context in kubectl: `k config use-context kind-kind` && `k config set-context --current --namespace=default`


# BOOTSTRAP

https://fluxcd.io/flux/get-started/



# INSTRUCTIONS


Run a k8s cluster with kind (kind create cluster)

Watch for changes: flux get kustomizations --watch

Add a document in the test.messages collection in the created db: `{"message": "hello world"}`


Suspend atlas: flux suspend kustomization infrastructure