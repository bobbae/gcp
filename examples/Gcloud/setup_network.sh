## example 1
## create network and subnet
#gcloud compute networks create custom-network1 --subnet-mode custom
#gcloud compute networks subnets create custom-subnet-us-west2-b --network custom-network1 --region us-west2   --range 192.168.1.0/24
## create firewall rules
#gcloud compute firewall-rules create allow-some-tcp     --network custom-network1  --source-ranges 0.0.0.0/0   --allow tcp:22,tcp:80,tcp:443
## create NAT router
#gcloud compute routers create nat-router     --network custom-network1    --region us-west2
#gcloud compute routers nats create nat-config    --router-region us-west2   --router nat-router --nat-all-subnet-ip-ranges   --auto-allocate-nat-external-ips

## example 2
## enable global bgp routing mode on network
#gcloud compute networks create network123 --project=sauni123 --subnet-mode=custom --mtu=1460 --bgp-routing-mode=global 
## enable private ip google access on subnet
#gcloud compute networks subnets create subnet123 --project=sauni123 --range=10.0.0.0/24 --stack-type=IPV4_ONLY --network=network123 --region=us-central1 --enable-private-ip-google-access 
## create firewall rules
#gcloud compute firewall-rules create network123-allow-custom --project=sauni123 --network=projects/sauni123/global/networks/network123 --description=Allows\ connection\ from\ any\ source\ to\ any\ instance\ on\ the\ network\ using\ custom\ protocols. --direction=INGRESS --priority=65534 --source-ranges=10.0.0.0/24 --action=ALLOW --rules=all 
#gcloud compute firewall-rules create network123-allow-icmp --project=sauni123 --network=projects/sauni123/global/networks/network123 --description=Allows\ ICMP\ connections\ from\ any\ source\ to\ any\ instance\ on\ the\ network. --direction=INGRESS --priority=65534 --source-ranges=0.0.0.0/0 --action=ALLOW --rules=icmp 
#gcloud compute firewall-rules create network123-allow-rdp --project=sauni123 --network=projects/sauni123/global/networks/network123 --description=Allows\ RDP\ connections\ from\ any\ source\ to\ any\ instance\ on\ the\ network\ using\ port\ 3389. --direction=INGRESS --priority=65534 --source-ranges=0.0.0.0/0 --action=ALLOW --rules=tcp:3389 
#gcloud compute firewall-rules create network123-allow-ssh --project=sauni123 --network=projects/sauni123/global/networks/network123 --description=Allows\ TCP\ connections\ from\ any\ source\ to\ any\ instance\ on\ the\ network\ using\ port\ 22. --direction=INGRESS --priority=65534 --source-ranges=0.0.0.0/0 --action=ALLOW --rules=tcp:22
## create NAT router
#gcloud compute routers create nat-router     --network network123 --project=sauni123 --region us-central1
#gcloud compute routers nats create nat-config    --router-region us-central1 --router nat-router --project sauni123 --nat-all-subnet-ip-ranges --auto-allocate-nat-external-ips
