gcloud compute instances create nat-test-1 \
    --image-family debian-9 \
    --image-project debian-cloud \
    --network custom-network1 \
    --subnet subnet-us-east-192 \
    --zone us-east4-c \
    --no-address
