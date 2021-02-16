include config.mk

.PHONY :
default:

.PHONY :
do-everything: 
	make deploy-function-randomgen
	make deploy-function-multiply
	make build-floor
	make deploy-cloud-run-floor
	make template-workflow
	make create-service-account
	make deploy-workflow
	make execute-workflow
	make get-workflow-result

.PHONY :
deploy-function-randomgen:
	cd randomgen; gcloud functions deploy randomgen --runtime python37 --trigger-http --allow-unauthenticated

.PHONY :
deploy-function-multiply:
	cd multiply; gcloud functions deploy multiply --runtime python37 --trigger-http --allow-unauthenticated

.PHONY :
test-function-randomgen:
	curl $(gcloud functions describe randomgen --format='value(httpsTrigger.url)')

.PHONY :
test-function-multiply:
	curl $(gcloud functions describe multiply --format='value(httpsTrigger.url)') -X POST -H "content-type: application/json" -d '{"input": 5}'

.PHONY :
build-floor:
	cd floor; gcloud builds submit --tag gcr.io/$(PROJECT_ID)/floor 

.PHONY :
deploy-cloud-run-floor:
	gcloud run deploy floor --platform managed --no-allow-unauthenticated

.PHONY :
template-workflow:
	APP_URL=$(gcloud run services list --platform managed --format 'value(URL)')
	REGION=$(REGION) PROJECT_ID=$(PROJECT_ID) RUNAPP_URL=$(APP_URL) ./templater workflow.tmpl > workflow.yaml
	./templater workflow.tmpl > workflow.yaml

.PHONY :
create-service-account:
	gcloud iam service-accounts create workflows-sa
	gcloud projects add-iam-policy-binding $(PROJECT_ID) --member "serviceAccount:workflows-sa@$(PROJECT_ID).iam.gserviceaccount.com" --role "roles/run.invoker"

.PHONY :
deploy-workflow:
	gcloud workflows deploy workflow --source workflow.yaml --service-account  workflows-sa@$PROJECT_ID.iam.gserviceaccount.com

.PHONY :
execute-workflow:
	gcloud workflows execute workflow

.PHONY :
get-workflow-result:
	EXE_NAME=$(gcloud workflows executions list  workflow --format 'value(NAME)')
	gcloud workflows executions describe $(EXE_NAME) --workflow workflow
