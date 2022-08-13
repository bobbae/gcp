
```
gcloud builds submit --tag gcr.io/$PROJECT/helloworld
gcloud run deploy --image gcr.io/$PROJECT/helloworld
curl https://helloworld-hjzj3l32pq-uc-xyz.a.run.app
```


```


WORKFLOW=myworkflow
gcloud workflows deploy $WORKFLOW --source httpget.workflows.json
gcloud workflows run $WORKFLOW --format='value(result)' | python -m json.tool
```
