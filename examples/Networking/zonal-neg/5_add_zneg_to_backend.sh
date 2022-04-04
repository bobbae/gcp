  gcloud compute backend-services add-backend neg-su1-backend-service \
      --global \
      --balancing-mode=RATE \
      --max-rate-per-endpoint=100 \
      --network-endpoint-group=neg-su1 \
      --network-endpoint-group-zone=us-west2-b
   
