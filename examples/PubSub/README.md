# Demo to have GCS notify a message to pubsub topic when a file is created in a bucket.

### service account

Have service account keys pointed by 

GOOGLE_APPLICATION_CREDENTIALS env var.

Make sure you have pubsub role added to this service account.

### add IAM policy binding to service account for pubsub role

gcloud pubsub subscriptions add-iam-policy-binding  your-subscription-id --member serviceAccount:your-service-account@your-project.iam.gserviceaccount.com --role=roles/editor


### running the demo
Run this demo by doing:

```
# set BUCKET environment variable
export BUCKET=my-special-bucket
# if you don't have a bucket create it use gsutil mb gs://my-special-bucket
# run the demo
python3 sub.py your-project-name your-subscription-id 
```

### assumptions
you should have a project called `your-project-name` and you have created a subscription for a topic.

```
# create a topic
gcloud pubsub topics create my-special-topic
gcloud pubsub subscriptions create my-special-subscription --topic my-special-topic
```

### test environment first before running the demo
Before running this demo you may want to test out the topic

```
# send a message to the topic
gcloud pubsub topics publish my-special-topic --message '{ "kind": "hello" }'
# and try to receive it
gcloud pubsub subscriptions pull my-special-subscription --auto-ack
```

If that works then test with the GCS bucket

```
# make GCS send notifications
gsutil notification create -f json -t my-special-topic gs://my-special-bucket
# cp a file to the bucket and it will generate a notification message to the pubsub topic
gsutil cp ~/some-test-file gs://my-special-bucket
# pull a message
gcloud pubsub subscriptions pull my-special-subscription --auto-ack
```

If this works, your demo should run OK.
Just run

```
python3 sub.py my-project-1 my-subscription-1
```

and in another window copy a file to the bucket, then you will get a notification message.

