# Setting up wireguard vpn

https://www.juniq.net/blog/diy-vpn-wireguard-gcp/

## Using secret manager 


### creating service account

gcloud iam service-accounts create secret-accessor \
--description "SA for accessing Secret Manager secrets" \
--display-name "secret accessor"

### enable secretmanager.secretAccessor role

gcloud projects add-iam-policy-binding project-123 \
--member serviceAccount:secret-accessor@project-123.iam.gserviceaccount.com \
--role roles/secretmanager.secretAccessor


### setting up firewall rules to open udp port 51820 for wireguard

gcloud compute firewall-rules create wg --direction IN --target-tags wg --allow udp:51820 --source-ranges 0.0.0.0/0gcloud compute firewall-rules create wg --direction IN --target-tags wg --allow udp:51820 --source-ranges 0.0.0.0/0

### create and store secrets 

* WireGuard configuration created in the previous section: 
	gcloud beta secrets create wg_config --data-file wg0.conf --replication-policy automatic

* Cloudflare API token: 
	echo -n 'my_cloudflare_api_token==' | gcloud beta secrets create wg_cf_api_token --data-file - --replication-policy automatic

* Cloudflare Zone ID: 
	echo -n 'my_cloudflare_zone_id_123456' | gcloud beta secrets create wg_cf_zone_id --data-file - --replication-policy automatic

* Hostname of the VM WireGuard clients will conect to: 
	echo -n 'vpn.example.com' | gcloud beta secrets create wg_hostname --data-file - --replication-policy automatic

### Use cloud-init file 

Use `vm-create.sh`

```
./vm-create.sh vpn-ue1b us-east1-b
./vm-create.sh vpn-uc1b us-central1-b
./vm-create.sh vpn-uw1b us-west1-b
```

