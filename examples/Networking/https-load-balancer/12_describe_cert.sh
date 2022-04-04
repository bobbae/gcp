gcloud compute ssl-certificates describe www-ssl-cert \
   --global \
   --format="get(name,managed.status, managed.domainStatus)"
