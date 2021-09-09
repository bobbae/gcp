Based on https://medium.com/google-cloud/call-a-workflow-from-a-function-51fc7fc8e1ff


Deploy the workflow. It gets the day of the week and uses it to query wikipedia.

```
gcloud auth login
gcloud workflows deploy wikiwf1 --source=wikiwf1.yaml
gcloud workflows run wikiwf1
```

Look at `deploy.sh`.  Deploy the cloud function in `index.js`.
To test the function locally, first do

```
gcloud auth application-default login
```

This will save ADC (Application Default Credentials) to ~/.config/gcloud/application_default_credentials.json.

Run locally.

```
export PROJECT_ID=$(gcloud config get-value core/project)
npm i
npm start
```

Test it.

```
curl -XPOST localhost:8080
```

If everything is OK, deploy the function.

```
gcloud functions deploy runWorkflowFunction --runtime nodejs12 --region us-central1 --entry-point runWorkflow --set-env-vars PROJECT_ID=$PROJECT_ID --trigger-http --no-allow-unauthenticated
```

Call the function.

```
FUNCTION_URL=https://us-entral1-$PROJECT_ID.cloudfunctions.net/runWorkflowFunction
curl -XPOST -H "Authorization: Bearer $(gcloud auth print-identity-token)" $FUNCTION_URL
```

Result may vary depending on the day of the week.

```
Result: ["Thursday","Thursday Night Football","Thursday (band)","Thursday Island","Thursday Night Baseball","Thursday at the Square","Thursday Next","Thursday (album)","Thursday Afternoon","Thursday's Child (David Bowie song)"]$```


