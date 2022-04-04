gcloud compute network-endpoint-groups create neg-su1 \
    --network-endpoint-type=GCE_VM_IP_PORT \
    --zone=us-west2-b \
    --network=custom-network1 \
    --subnet=custom-subnet-us-west2-b 
    
