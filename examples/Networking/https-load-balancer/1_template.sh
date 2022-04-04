gcloud compute instance-templates create template-1 --region=us-east1 --network=default \
	--subnet=default --tags=allow-health-check --image-family=debian-9 \
	--image-project=debian-cloud --metadata=startup-script='#! /bin/bash
     sudo apt-get update
     sudo apt-get install apache2 -y
     sudo a2ensite default-ssl
     sudo a2enmod ssl
     sudo vm_hostname="$(curl -H "Metadata-Flavor:Google" \
   http://169.254.169.254/computeMetadata/v1/instance/name)"
   sudo echo "Page served from: $vm_hostname" | \
   tee /var/www/html/index.html
   sudo systemctl restart apache2'

