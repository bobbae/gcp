# pod monitor hook

https://github.com/flant/shell-operator#quickstart

Build docker image

```
$ docker build -t 'quay.io/XXXyourname/shell-operator:monitor-pods' .
$ docker push  'quay.io/XXXyourname/shell-operator:monitor-pods' 
```

Create RBAC objects

We need to watch for Pods in all Namespaces. That means that we need specific RBAC definitions for shell-operator:

```
kubectl create namespace example-monitor-pods
kubectl create serviceaccount monitor-pods-acc --namespace example-monitor-pods
kubectl create clusterrole monitor-pods --verb=get,watch,list --resource=pods
kubectl create clusterrolebinding monitor-pods --clusterrole=monitor-pods --serviceaccount=example-monitor-pods:monitor-pods-acc
```

Start the shell-operator 

```
$ cat shell-operator-pod.yaml | IMG=quay.io/XXXyourname/shell-operator:monitor-pods  envsubst | kubectl -n example-monitor-pods apply -f -

```

Deploy a pod 

```
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/aio/deploy/recommended.yaml
```

Examine logs

```
$ kubectl -n example-monitor-pods logs po/shell-operator

or

$ kubectl -n example-monitor-pods run  nginx2 --image=nginx 
```

You should see messages with references to "added" pods.


Clean up

```
$ kubectl delete ns example-monitor-pods
$ kubectl delete clusterrole monitor-pods
$ kubectl delete clusterrolebinding monitor-pods
```

