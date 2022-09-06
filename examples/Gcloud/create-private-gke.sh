gcloud container clusters create private-cluster-0  --subnetwork custom-subnet-us-west2-b --network custom-network1 --enable-master-authorized-networks --enable-ip-alias --enable-private-nodes --enable-private-endpoint --master-ipv4-cidr 172.16.0.32/28 --zone us-west2-b
#gcloud container clusters create-auto private-cluster-1  --region us-west2  --enable-master-authorized-networks --network custom-network1 --subnetwork custom-subnet-us-west2-b --cluster-secondary-range-name my-pods --services-secondary-range-name my-services --enable-private-nodes
# gcloud components install kubectl
# kubectl get nodes
# kubectl create deployment hello-server  --image=us-docker.pkg.dev/google-samples/containers/gke/hello-app:1.0
# kubectl get pods
# kubectl expose deployment hello-server --type LoadBalancer --port 80 --target-port 8080
# kubectl get svc
# curl http://EXTERNAL-IP
