# Instructions

1. Login to AWS `aws sso login --profile SA`
2. Create eks cluster in AWS with 3x m5.large `eksctl --profile SA create cluster -f ../../resources/eks-cluster-setup/eksconfig.yaml`
3. `kubectl delete storageclass gp2`
4. `kubectl apply -f storageClass.yaml`
5. Set up kubectl config: `eksctl --profile SA utils write-kubeconfig --cluster=tommcc-cluster`. 
6. If session times out (kubectl commands fail), refresh it with `aws sso login --profile SA`.


