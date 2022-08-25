gcloud compute networks list
gcloud compute networks subnets list --filter=custom-network1
gcloud compute networks subnets update custom-subnet-us-west2-b --region=us-west2 --enable-private-ip-google-access
gcloud compute networks subnets describe custom-subnet-us-west2-b --region=us-west2 --format="get(privateIpGoogleAccess)"
