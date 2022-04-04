gcloud compute forwarding-rules create neg-su1-forwarding-rule \
    --address=lb2-address \
    --target-http-proxy=neg-su1-target-proxy \
    --global \
    --ports=80
