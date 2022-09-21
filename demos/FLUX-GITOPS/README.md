Creates an Atlas cluster and a flask app which connects to it. 


# REQs

- k8s cluster (kind works)


# BOOTSTRAP

https://fluxcd.io/flux/get-started/



# INSTRUCTIONS


Run a k8s cluster with kind (kind create cluster)

Watch for changes: flux get kustomizations --watch

Suspend atlas: flux suspend kustomization infrastructure