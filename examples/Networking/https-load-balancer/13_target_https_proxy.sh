    gcloud compute target-https-proxies create https-lb-proxy \
        --url-map=web-map-https \
        --ssl-certificates=www-ssl-cert
    