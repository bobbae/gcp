gcloud compute networks create custom-network1 \
    --subnet-mode custom

gcloud compute networks subnets create subnet-us-east-192 \
   --network custom-network1 \
   --region us-east4 \
   --range 192.168.1.0/24

