# multicontainer pod

Using minikube,

```
$ kubectl apply -f multi-container-pod.yaml
$ kubectl expose pod  multi-container-pod --port=8080 --target-port=80 --type=LoadBalancer
$ kubectl get svc
$ minikube service multi-container-pod
```

To use ingress example

```
$ minkube addons enable ingress
$ kubectl create deployment web --image=gcr.io/google-samples/hello-app:1.0
$ kubectl expose deployment web --type=NodePort --port=8080
$ kubectl create deployment web2 --image=gcr.io/google-samples/hello-app:2.0
$ kubectl expose deployment web2 --type=NodePort --port=8080
$ kubectl apply -f example-ingress.yaml
$ kubectl get ingress
$ minikube service web --url 
# edit /etc/hosts
$ curl hello-world.info
$ curl hello-world.info/v2
```
