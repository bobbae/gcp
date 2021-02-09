# terraform example

```
$ gcloud auth login
$ gcloud config set project XXX-your-own-project-id
$ terraform init
$ terraform plan -var "project=$(gcloud config get-value project)" -auto-approve
$ terraform apply -var "project=$(gcloud config get-value project)" -auto-approve
```

The IP will be printed.
Use ssh to copy and execute scripts.
```
$ scp files/startup-script-custom  XXX-ip-printed-after-apply
$ ssh XXX-ip ./startup-script-custom
$ ssh XXX-ip python app.py
```

Browse to XXX-ip:5000.


When done, remove the VM.

```
$ terraform destroy -var "project=$(gcloud config get-value project)" -auto-approve
```
