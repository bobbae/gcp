# Create Memorystore Redis instance from a GKE cluster

To create redis instance:
https://cloud.google.com/memorystore/docs/redis/quickstart-gcloud

```
$ gcloud redis instances create myinstance --size=2 --region=us-central1 \
    --redis-version=redis_5_0
$ gcloud redis instances describe myinstance --region=us-central1

```

App original source code
https://github.com/GoogleCloudPlatform/golang-samples/blob/master/memorystore/redis/main.go

Try bulding the Go program.
```
$ go mod init visit-counter
$ go test
$ go build
```




To create GKE and connect app:
https://cloud.google.com/memorystore/docs/redis/connect-redis-instance-gke


```
$ gcloud compute zones list
$ gcloud config set compute/zone us-central1-a
$ gcloud container clusters create visitcount-cluster --num-nodes=3 --enable-ip-alias
$ kubectl get nodes
```

Create configmap for redis instance:

```
$ gcloud redis instances describe myinstance --region=us-central1
```

Use the Redis host IP address to make a configmap:
```
$ export REDISHOST=XX.XX.XX.XX
$ kubectl create configmap redishost --from-literal=REDISHOST=${REDISHOST}
$ kubectl get configmaps redishost -o yaml
```

Build the container and push to GCR.
```
$ export PROJECT_ID="$(gcloud config get-value project -q)"
$ docker build -t gcr.io/${PROJECT_ID}/visit-counter:v1 .
$ gcloud docker -- push gcr.io/${PROJECT_ID}/visit-counter:v1
```

Deploy service to k8s cluster.
```
$ kubectl apply -f visit-counter.yaml
$ kubectl get svc
$ kubectl get deploy
$ kubectl get service visit-counter

```
