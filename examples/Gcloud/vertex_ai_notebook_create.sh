#gcloud notebooks instances create example-instance  --vm-image-project=deeplearning-platform-release  --vm-image-family=pytorch-1-9-cu110-notebooks  --machine-type=n1-standard-4  --location=us-west2-b  --boot-disk-size=100 --accelerator-core-count=1 --accelerator-type=NVIDIA_TESLA_V100 --install-gpu-driver --network=custom-network1 --subnet=custom-subnet-us-west2-b --subnet-region=us-west2 --no-public-ip
gcloud notebooks instances create example-instance  --vm-image-project=deeplearning-platform-release  --vm-image-family=pytorch-1-9-cu110-notebooks  --machine-type=n1-standard-4  --location=us-west2-b  --boot-disk-size=100  --install-gpu-driver --network=custom-network1 --subnet=custom-subnet-us-west2-b --subnet-region=us-west2 --no-public-ip