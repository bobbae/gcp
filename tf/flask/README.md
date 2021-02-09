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
$ export XXXIP=$(terraform output ip)
$ scp files/startup-script-custom $XXXIP 
$ ssh $XXXIP ./startup-script-custom
$ ssh $XXXIP python app.py
```

Browse to $XXXIP:5000.


When done, remove the VM.

```
$ terraform destroy -var "project=$(gcloud config get-value project)" -auto-approve
```
