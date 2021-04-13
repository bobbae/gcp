# VPC

https://cloud.google.com/vpc/docs/using-vpc

## creating networks 

```

gcloud compute networks create NETWORK \
   --subnet-mode=auto \
   --bgp-routing-mode=DYNAMIC_ROUTING_MODE \
   --mtu=MTU
```

* NETWORK is a name for the VPC network.

* DYNAMIC_ROUTING_MODE can be either global or regional to control the route advertisement behavior of Cloud Routers in the network. For more information, refer to dynamic routing mode.

* MTU is the maximum transmission unit of the network. MTU can either be 1460 (default) or 1500. Review the MTU information in the concepts guide before setting the MTU to 1500.


## creating subnetworks

```
gcloud compute networks subnets create SUBNET \
    --network=NETWORK \
    --range=PRIMARY_RANGE \
    --region=REGION
```

* SUBNET is a name for the new subnet.

* NETWORK is the name of the VPC network that will contain the new subnet.

* PRIMARY_RANGE is the primary IP range for the new subnet, in CIDR notation. For more information, see Subnet ranges.

* REGION is the Google Cloud region in which the new subnet will be created.


## Use terraform

See `terraform/` subdirectory here.
