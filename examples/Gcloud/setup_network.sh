
gcloud compute networks create custom-network1 \
    --subnet-mode custom

gcloud compute networks subnets create custom-subnet-us-west2-b \
   --network custom-network1 \
   --region us-west2 \
   --range 192.168.1.0/24

gcloud compute firewall-rules create allow-some-tcp \
    --network custom-network1 \
    --source-ranges 0.0.0.0/0 \
    --allow tcp:22,tcp:80,tcp:443

gcloud compute routers create nat-router \
    --network custom-network1 \
    --region us-west2

gcloud compute routers nats create nat-config \
    --router-region us-west2 \
    --router nat-router \
    --nat-all-subnet-ip-ranges \
    --auto-allocate-nat-external-ips
