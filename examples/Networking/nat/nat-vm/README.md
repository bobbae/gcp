https://cloud.google.com/nat/docs/gce-example

```
gcloud compute networks create custom-network1 \
    --subnet-mode custom

gcloud compute networks subnets create subnet-us-east-192 \
   --network custom-network1 \
   --region us-east4 \
   --range 192.168.1.0/24

gcloud compute instances create nat-test-1 \
    --image-family debian-9 \
    --image-project debian-cloud \
    --network custom-network1 \
    --subnet subnet-us-east-192 \
    --zone us-east4-c \
    --no-address

gcloud compute firewall-rules create allow-ssh \
    --network custom-network1 \
    --source-ranges 35.235.240.0/20 \
    --allow tcp:22

# PROJECT_ID
# MEMBER_INFO     user:username@example.com    group:admins@example.com    serviceAccount:test123@example.domain.com

gcloud projects add-iam-policy-binding my-project-1 \
    --member=user:bob@example.com \
    --role=roles/iap.tunnelResourceAccessor

gcloud compute ssh nat-test-1 \
    --zone us-east4-c \
    --command "curl example.com" \
    --tunnel-through-iap


gcloud compute routers create nat-router \
    --network custom-network1 \
    --region us-east4

gcloud compute routers nats create nat-config \
    --router-region us-east4 \
    --router nat-router \
    --nat-all-subnet-ip-ranges \
    --auto-allocate-nat-external-ips
```