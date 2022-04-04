gcloud compute target-https-proxies create neg-su1-https-target-proxy \
    --ssl-certificates=lb1-cert \
    --url-map=neg-su1-url-map
