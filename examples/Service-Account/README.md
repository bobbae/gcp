## Example

```
SERVICE_ACCOUNT_NAME=example-gcs-svc-account
SERVICE_ACCOUNT_DEST=~/example-gcs-svc-account.json

gcloud iam service-accounts create \
    $SERVICE_ACCOUNT_NAME \
    --display-name $SERVICE_ACCOUNT_NAME

SA_EMAIL=$(gcloud iam service-accounts list \
    --filter="displayName:$SERVICE_ACCOUNT_NAME" \
    --format='value(email)')

PROJECT=$(gcloud config get-value project)

gcloud projects add-iam-policy-binding $PROJECT \
    --role roles/storage.admin --member serviceAccount:$SA_EMAIL

mkdir -p $(dirname $SERVICE_ACCOUNT_DEST)

gcloud iam service-accounts keys create $SERVICE_ACCOUNT_DEST \
    --iam-account $SA_EMAIL

gcloud iam roles list

gcloud projects get-iam-policy $PROJECT

gcloud projects get-iam-policy $PROJECT --flatten=bindings[].members --format=table(bindings.role) --filter=bindings.members:$SA_EMAIL

```
