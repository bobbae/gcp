# dataflow

## gcloud CLI using template

https://cloud.google.com/dataflow/docs/guides/templates/provided-templates

```
gcloud dataflow jobs run df-job-1 --gcs-location gs://dataflow-templates/latest/Word_Count --parameters inputFile=gs://dataflow-samples/shakespeare/kinglear.txt,output=${BUCKET}/my_output
```

## flex templates

Under `flex-templates/`

## Deleting dataflow jobs

You *cannot* delete dataflow jobs as of now (March, 2021). This feature needs to be implemented by Google.
