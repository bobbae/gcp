include config.mk

.PHONY : default deploy-function-randomgen deploy-function-multiply test-function-randomgen test-function-multiply build-floor deploy-cloud-run-floor template-workflow create-service-account deploy-workflow execute-workflow get-workflow-result

default: get-workflow-result

deploy-function-randomgen:
	cd randomgen; gcloud functions deploy randomgen --runtime python37 --trigger-http --allow-unauthenticated

deploy-function-multiply: deploy-function-randomgen
	cd multiply; gcloud functions deploy multiply --runtime python37 --trigger-http --allow-unauthenticated

test-function-randomgen:
	curl $(gcloud functions describe randomgen --format='value(httpsTrigger.url)')

test-function-multiply:
	curl $(gcloud functions describe multiply --format='value(httpsTrigger.url)') -X POST -H "content-type: application/json" -d '{"input": 5}'

build-floor: deploy-function-multiply
	cd floor; gcloud builds submit --tag gcr.io/$(PROJECT_ID)/floor 

deploy-cloud-run-floor: build-floor
	gcloud run deploy floor --platform managed --no-allow-unauthenticated

template-workflow: deploy-cloud-run-floor
	APP_URL := $(shell gcloud run services list --platform managed --format 'value(URL)')
	REGION=$(REGION) PROJECT_ID=$(PROJECT_ID) RUNAPP_URL=$(APP_URL) ./templater workflow.tmpl > workflow.yaml
	./templater workflow.tmpl > workflow.yaml

create-service-account: template-workflow
	gcloud iam service-accounts create workflows-sa
	gcloud projects add-iam-policy-binding $(PROJECT_ID) --member "serviceAccount:workflows-sa@$(PROJECT_ID).iam.gserviceaccount.com" --role "roles/run.invoker"

deploy-workflow: create-service-account
	gcloud workflows deploy workflow --source workflow.yaml --service-account  workflows-sa@$PROJECT_ID.iam.gserviceaccount.com

execute-workflow: deploy-workflow
	gcloud workflows execute workflow

get-workflow-result: execute-workflow
	#PROJ := $(shell gcloud config list --format='value(core.project)')
	EXE_NAME := $(shell gcloud workflows executions list  workflow --format 'value(NAME)')
	gcloud workflows executions describe $(EXE_NAME) --workflow workflow
