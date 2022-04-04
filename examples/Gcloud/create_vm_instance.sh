gcloud compute instances create instance-1 --project=project-su-1 --zone=us-west2-b \
    --machine-type=n2-standard-4 --network-interface=subnet=custom-subnet-us-west2-b,no-address \
    --maintenance-policy=MIGRATE --service-account=432811401078-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
    --tags=http-server,https-server \
    --create-disk=auto-delete=yes,boot=yes,device-name=instance-2,image=projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20220308,mode=rw,size=200,type=projects/project-su-1/zones/us-west2-b/diskTypes/pd-balanced \
    --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring \
    --reservation-affinity=any

