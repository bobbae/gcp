# terraform example

```
$ gcloud auth login
$ gcloud config set project XXX-your-own-project-id
$ terraform init
$ terraform plan -var "project=$(gcloud config get-value project)" -auto-approve
$ terraform apply -var "project=$(gcloud config get-value project)" -auto-approve
$ terraform destroy -var "project=$(gcloud config get-value project)" -auto-approve
```
