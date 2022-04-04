    gcloud compute forwarding-rules create https-content-rule \
        --load-balancing-scheme=EXTERNAL \
        --network-tier=PREMIUM \
        --address=lb-ipv4-1 \
        --global \
        --target-https-proxy=https-lb-proxy \
        --ports=443
    