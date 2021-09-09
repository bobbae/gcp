# Configuration
export PROJECT_ID=$(gcloud config get-value core/project)

# Deploy Workflow
gcloud workflows deploy wikiwf1  --source=wikiwf1.yaml

# Deploy (private) Function
gcloud functions deploy runWorkflowFunction \
	--runtime nodejs12 \
	--region us-central1 \
	--entry-point runWorkflow \
	--set-env-vars PROJECT_ID=$PROJECT_ID \
	--trigger-http \
	--no-allow-unauthenticated

# Call (private) Function
FUNCTION_URL=https://us-central1-$PROJECT_ID.cloudfunctions.net/runWorkflowFunction
curl -XPOST -H "Authorization: Bearer $(gcloud auth print-identity-token)" $FUNCTION_URL
