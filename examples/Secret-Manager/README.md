# secret manager examples

Make sure your IAM has sufficient permission to read the secret first.


```
echo -n "my super secret data" | gcloud secrets create my-secret \
	--replication-policy="automatic" \
	--data-file=-

gcloud secrets versions access 1 --secret="my-secret"

gcloud secrets versions access latest --secret="my-secret"
```

## Additional examples

In Go and Nodejs.

## cloud-run and secrets

Try 

https://shell.cloud.google.com/?walkthrough_tutorial_url=https%3A%2F%2Fwalkthroughs.googleusercontent.com%2Fcontent%2Fsecret_manager_cloud_code_create_secret%2Fsecret_manager_cloud_code_create_secret.md&show=ide%2Cterminal

# KMS

## Berglas 

https://github.com/GoogleCloudPlatform/berglas
