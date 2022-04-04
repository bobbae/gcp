gcloud compute ssl-certificates create www-ssl-cert \
    --description=gcp-www-ssl-cert \
    --domains=instance-1.goog.cf \
    --global
