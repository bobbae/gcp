# terraform-gke

First edit terraform.tfvars to set project name and region. 

Then do,

```
terraform init
```

Then,
```
terraform plan
terraform apply
```

After cluster is created, get credentials for the cluster just created.
```
gcloud container clusters get-credentials $(terraform output -raw kubernetes_cluster_name) --region $(terraform output -raw region)
kubectl config get-contexts
kubectl get nodes
```

Finaly
```
terraform destroy
```
