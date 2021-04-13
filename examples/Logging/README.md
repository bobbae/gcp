# Logging example

https://cloud.google.com/logging/docs/quickstart-python

```
python snippets.py mylog write

python snippets.py mylog list
```

## Agents

Monitoring and Logging agents.


https://console.cloud.google.com/monitoring/settings/agents

## MQL

Monitoring Query Language

https://cloud.google.com/monitoring/mql/examples

## Using query via REST API

https://cloud.google.com/monitoring/mql/qn-from-api

```
PROJECT_ID=a-sample-project

gcloud auth login

gcloud config set project ${PROJECT_ID}

TOKEN=`gcloud auth print-access-token`

curl -d @query.json -H "Authorization: Bearer $TOKEN" \
   --header "Content-Type: application/json" -X POST \
   https://monitoring.googleapis.com/v3/projects/${PROJECT_ID}/timeSeries:query
```

With `query.json`:

```
{
  "query": "fetch gce_instance::compute.googleapis.com/instance/disk/read_bytes_count | within 5m"
}
```




