## install google cloud pubsub package

```
pip install --upgrade google-cloud-pubsub
```

## create topic
```
gcloud pubsub topics create my-topic
```

## create subscription

```
gcloud pubsub subscriptions create my-sub --topic my-topic
```

## subscribe and read message 
```
gcloud pubsub subscriptions pull my-special-subscription --auto-ack
```

## publish the message
```
gcloud pubsub topics publish my-special-topic --message '{ "kind": "hello" }'
```


## Adding IAM policy to service account

### publish topic IAM policy binding

```
gcloud pubsub topics add-iam-policy-binding --member serviceAccount:some-user-sa@project-1.iam.gserviceaccount.com --role roles/owner my-topic
```

### subscription IAM policy binding

```
gcloud pubsub subscriptions add-iam-policy-binding --member serviceAccount:some-user-sa1@project-1.iam.gserviceaccount.com --role roles/owner mysubscription
```


## testing example scripts

### run the reader and the sender

```
python sub.py
```

and in another window do:

```
python pub.py
```

