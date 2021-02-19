# Google Cloud Storage

* [Benchmark using GCS vs. GCSFUSE](https://github.com/bobbae/gcp/blob/main/gcs/GCS_vs_GCSFUSE.md)
* [modified notification polling code](https://github.com/bobbae/gcp/blob/main/gcs/notification_polling.py) that:

    - gets notification when files are added to GCS bucket
    - pubsub message is sent and received
    - a Bigquery table entry is created.

   For example:

    - gsutil mb gs://$BUCKET
    - gsutil notification create -f json -t $TOPIC gs://$BUCKET
    - gcloud pubsub subscriptions create $SUB --topic $TOPIC
    - python notification_polling.py $PROJECT $sub $PROJECT.test1.table1
