gcloud compute ssh nat-test-1 \
    --zone us-east4-c \
    --command "curl example.com" \
    --tunnel-through-iap


