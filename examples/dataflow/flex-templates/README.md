# using flex templates

## Enable APIs

```
gcloud services enable dataflow compute_component logging storage_component storage_api bigquery pubsub cloudresourcemanager.googleapis.com appengine.googleapis.com cloudscheduler.googleapis.com cloudbuild.googleapis.com

```

## Set GOOGLE_APPLICATION_CREDENTIALS

```
export GOOGLE_APPLICATION_CREDENTIALS=/your/key/for/project-a33eb2XXXXXXXX.json
```

## Create example source and sink

### Create a bucket

```
export BUCKET='my-storage-bucket'
gsutil mb gs://$BUCKET
```

## Pub/Sub

### Create Pub/Sub topic and a subscription to that topic

```
export TOPIC='messages'
export SUBSCRIPTION='ratings'
gcloud pubsub topics create $TOPIC
gcloud pubsub subscriptions create --topic $TOPIC $SUBSCRIPTION
```

### Create a Cloud Scheduler Job that publishes 1 message each minute

```
gcloud scheduler jobs create pubsub positive-ratings-publisher \
  --schedule="* * * * *" \
  --topic="$TOPIC" \
  --message-body='{"url": "https://beam.apache.org/", "review": "positive"}'
```

### Start the scheduler

```
gcloud scheduler jobs run positive-ratings-publisher
```

### Create and run another similar publisher for 'negative ratings' that publishes 1 message every 2 minutes

```
gcloud scheduler jobs create pubsub negative-ratings-publisher \
  --schedule="*/2 * * * *" \
  --topic="$TOPIC" \
  --message-body='{"url": "https://beam.apache.org/", "review": "negative"}'

gcloud scheduler jobs run negative-ratings-publisher
```

## BigQuery

### Create a BigQuery dataset

```
export PROJECT="$(gcloud config get-value project)"
export DATASET="beam_samples"
export TABLE="streaming_beam_sql"

bq mk --dataset "$PROJECT:$DATASET"
```

## Python Code for Beam job

### Python code sample for streaming_beam

Copied from   git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git

```
  cd streaming_beam
```

### export TEMPLATE_IMAGE pointing to the docker image

```
export TEMPLATE_IMAGE="gcr.io/$PROJECT/samples/dataflow/streaming-beam-sql:latest"
```

### Use python 3.7

Create a virtual env if you need to and use it.
```
source your-virtual-env/bin/activate
```

## Docker image

### Steps to create docker image

```
gcloud config set builds/use_kaniko True
```

### Dockerfile

located under `streaming_beam/Dockerfile`


### Build the docker image

```
gcloud builds submit --tag $TEMPLATE_IMAGE .
```


## Template

### Create a template spec file containing info necessary to run the job such as SDK and metadata

```
export TEMPLATE_PATH="gs://$BUCKET/samples/dataflow/templates/streaming-beam-sql.json"
```

Build the flex template

```
    gcloud dataflow flex-template build $TEMPLATE_PATH \
          --image "$TEMPLATE_IMAGE" \
          --sdk-language "PYTHON" \
          --metadata-file "metadata.json"
```


## Running Flex Template pipeline

### Run via gcloud or REST API

First reset SUBSCRIPTION to match the pattern in metadata.json. Otherwise you will not be able to run the template.

```
export SUBSCRIPTION=projects/${PROJECT}/subscriptions/ratings
```

Gcloud

```
  export REGION="us-central1"

    gcloud dataflow flex-template run "streaming-beam-`date +%Y%m%d-%H%M%S`" \
        --template-file-gcs-location "$TEMPLATE_PATH" \
        --parameters input_subscription="$SUBSCRIPTION" \
        --parameters output_table="$PROJECT:$DATASET.$TABLE" \
        --region "$REGION"
```


REST API

```

curl -X POST \
  "https://dataflow.googleapis.com/v1b3/projects/$PROJECT/locations/us-central1/flexTemplates:launch" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -d '{
    "launch_parameter": {
      "jobName": "streaming-beam-sql-'$(date +%Y%m%d-%H%M%S)'",
      "parameters": {
        "inputSubscription": "'$SUBSCRIPTION'",
        "outputTable": "'$PROJECT:$DATASET.$TABLE'"
      },
      "containerSpecGcsPath": "'$TEMPLATE_PATH'"
    }
  }'

```


## Check the results in BigQuery

After some time...

```
bq query --use_legacy_sql=false 'SELECT * FROM `'"$PROJECT.$DATASET.$TABLE"'`'
```



