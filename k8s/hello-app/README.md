# Hello Application example


https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app

Modified with additional /podinfo to lookup information on pods
from within k8s cluster.

Install vendor/ modules so that docker build can succeed.
```
$ go mod vendor
```

Assume that you have GKE cluster running.
Build and deploy into cluster.


```
$ docker build -t gcr.io/${PROJECT}/hello-app:v2 .
$ docker images
$ docker auth configure-docker
$ docker push gcr.io/${PROJECT_ID}/hello-app:v2
$ kubectl create deployment hello-app2 --image=gcr.io/${PROJECT_ID}/hello-app:v2
$ kubectl get pods
$ kubectl expose deployment hello-app2 --name=hello-app-service2 --type=LoadBalancer --port 80 --target-port 8080
$ kubectl get svc
```

When EXTERNAL-IP is filled in (not pending). Do curl https://IP/podinfo

You will need to create role binding which will grant the default service account view permissions if you have RBAC enabled on your cluster.

```
$ kubectl create clusterrolebinding default-view --clusterrole=view --serviceaccount=default:default
```

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/GoogleCloudPlatform/kubernetes-engine-samples&cloudshell_tutorial=README.md&cloudshell_workspace=hello-app)

This example shows how to build and deploy a containerized Go web server
application using [Kubernetes](https://kubernetes.io).

Visit https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app
to follow the tutorial and deploy this application on [Google Kubernetes
Engine](https://cloud.google.com/kubernetes-engine).

This directory contains:

- `main.go` contains the HTTP server implementation. It responds to all HTTP
  requests with a  `Hello, world!` response.
- `Dockerfile` is used to build the Docker image for the application.

This application is available as two Docker images, which respond to requests
with different version numbers:

- `gcr.io/google-samples/hello-app:1.0`
- `gcr.io/google-samples/hello-app:2.0`

This example is used in many official/unofficial tutorials, some of them
include:
- [Kubernetes Engine Quickstart](https://cloud.google.com/kubernetes-engine/docs/quickstart)
- [Kubernetes Engine - Deploying a containerized web application](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app) tutorial
- [Kubernetes Engine - Setting up HTTP Load Balancing](https://cloud.google.com/kubernetes-engine/docs/tutorials/http-balancer) tutorial
