gcloud compute firewall-rules create fw-custom-network1-allow-health-check \
    --network=custom-network1 \
    --action=allow \
    --direction=ingress \
    --target-tags=allow-health-check \
    --source-ranges=130.211.0.0/22,35.191.0.0/16 \
    --rules=tcp:80
    
