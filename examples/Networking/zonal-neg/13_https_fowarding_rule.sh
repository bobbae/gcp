gcloud compute forwarding-rules create neg-su1-https-forwarding-rule \
    --address=lb2-address \
    --target-https-proxy=neg-su1-https-target-proxy \
    --global \
    --ports=443
