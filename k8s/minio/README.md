# minio

The example `minio` install in k8s.

For example to use minikube,

```
$ kubectl apply -f my-minio-fs.yaml
$ kubectl expose deployment/my-minio-fs --type="NodePort" --port 9000
$ kubectl get services/my-minio-fs -o go-template='{{(index .spec.ports 0).nodePort}}'
# wget https://dl.min.io/client/mc/release/linux-amd64/mc
$ mc alias set minio http://192.168.49.2:9000 minio minio123
$ mc admin --json info minio
```

