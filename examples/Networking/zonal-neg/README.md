https://cloud.google.com/load-balancing/docs/https/setting-up-ext-https-hybrid

```
gcloud compute network-endpoint-groups create neg-su1 \
    --network-endpoint-type=GCE_VM_IP_PORT \
    --zone=us-west2-b \
    --network=custom-network1 \
    --subnet=custom-subnet-us-west2-b 
    
gcloud compute network-endpoint-groups update neg-su1 \
    --zone=us-west2-b \
    --add-endpoint='instance=instance-1,port=80' 

gcloud compute addresses create lb2-address \
      --global
  
gcloud compute health-checks create http neg-su1-health-check \
    --use-serving-port

gcloud compute backend-services create neg-su1-backend-service \
    --health-checks=neg-su1-health-check \
    --global

gcloud compute backend-services add-backend neg-su1-backend-service \
    --global \
    --balancing-mode=RATE \
    --max-rate-per-endpoint=100 \
    --network-endpoint-group=neg-su1 \
    --network-endpoint-group-zone=us-west2-b
 
gcloud compute url-maps create neg-su1-url-map \
    --default-service neg-su1-backend-service

gloud compute target-http-proxies create neg-su1-target-proxy \
    --url-map=neg-su1-url-map
gcloud compute forwarding-rules create neg-su1-forwarding-rule \
    --address=lb2-address \
    --target-http-proxy=neg-su1-target-proxy \
    --global \
    --ports=80

gcloud compute firewall-rules create fw-custom-network1-allow-health-check \
    --network=custom-network1 \
    --action=allow \
    --direction=ingress \
    --target-tags=allow-health-check \
    --source-ranges=130.211.0.0/22,35.191.0.0/16 \
    --rules=tcp:80

# on a VM 
apt-get update
apt-get install apache2 -y
vm_hostname="$(curl -H "Metadata-Flavor:Google" http://169.254.169.254/computeMetadata/v1/instance/name)"
echo "Page served from: $vm_hostname" | tee /var/www/html/index.html
systemctl restart apache2

gcloud compute ssl-certificates create lb1-cert \
    --domains lb1.sadauniv.com

gcloud compute target-https-proxies create neg-su1-https-target-proxy \
    --ssl-certificates=lb1-cert \
    --url-map=neg-su1-url-map

gcloud compute forwarding-rules create neg-su1-https-forwarding-rule \
    --address=lb2-address \
    --target-https-proxy=neg-su1-https-target-proxy \
    --global \
    --ports=443

gcloud compute ssl-certificates describe lb1-cert     --format="get(managed.domainStatus)"

gcloud compute target-https-proxies describe neg-su1-https-target-proxy  \
    --global \
    --format="get(sslCertificates)"
```