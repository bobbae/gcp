#!/usr/bin/env bash
NAME=${1:-vpn-ue1b}
ZONE=${2:-us-east1-b}
gcloud compute instances create "$NAME" \
  --machine-type f1-micro \ # f1-micro is powerful enough to run WireGuard server
  --image-family ubuntu-minimal-1910 \ # Ubuntu 19.10 provides WireGuard in the universe repo
  --image-project ubuntu-os-cloud \
  --metadata-from-file user-data=cloud-init-config.yaml \ # use the prepared cloud-init config here
  --scopes cloud-platform \
  --service-account secret-accessor@project-123.iam.gserviceaccount.com \ # use the prepared secret-accessor service account
  --tags wg \ # use network tags for the firewall rules
  --zone "$ZONE" # zone where to create the instance
