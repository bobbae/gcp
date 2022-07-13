wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-359.0.0-linux-x86_64.tar.gz
tar xf google-cloud-sdk-*.tar.gz
./google-cloud-sdk/install.sh
# make sure google-cloud-sdk/bin comes before existing gcloud in /snap/bin or remove /snap/bin/gcloud
#-sudo mv /snap/bin/gcloud /snap/bin/gcloud-old
mv google-cloud-sdk ~
rm google-cloud-sdk-*.tar.gz
gcloud init
gcloud components list
gcloud components install kubectl
gcloud components update
