gcloud compute firewall-rules create allow-ssh \
    --network custom-network1 \
    --source-ranges 35.235.240.0/20 \
    --allow tcp:22
