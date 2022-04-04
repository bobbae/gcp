    gcloud compute url-maps create web-map-http \
        --default-service web-backend-service
    
    gcloud compute url-maps create web-map-https \
        --default-service web-backend-service
    