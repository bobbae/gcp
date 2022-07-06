# Cloud Run

## xkcd

Go based Cloud Run compatible dockerized http json API and endpoint (/xkcd) to view daily comics.

## secrets

Try 

https://shell.cloud.google.com/?walkthrough_tutorial_url=https%3A%2F%2Fwalkthroughs.googleusercontent.com%2Fcontent%2Fsecret_manager_cloud_code_create_secret%2Fsecret_manager_cloud_code_create_secret.md&show=ide%2Cterminal

Some IDP security stuff:

So you have to add a permission for different users and invoke it in a certain way using identity token associated with the permission.  For example.

curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" https://helloworld-ezsdfasdfad-wn.a.run.app
Hello World!

After this:

gcloud run services add-iam-policy-binding helloworld-bob --member=user:bob.someuser@somecompay.com --role=roles/run.invoker

gcloud run services get-iam-policy helloworld-bob
bindings:
- members:
  - user:bob.someuser@somecompay.com
  role: roles/run.invoker
etag: BwasdfasdfE-aa=
version: 1

