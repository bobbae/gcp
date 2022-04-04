gcloud compute network-endpoint-groups update neg-su1 \
    --zone=us-west2-b \
    --add-endpoint='instance=instance-1,port=80' #--add-endpoint='instance=vm-a2,[port=PORT_VM_A2]'
