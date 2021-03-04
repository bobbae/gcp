# example k8s Operator

https://sdk.operatorframework.io/docs/building-operators/golang/tutorial/
Created via:

``` 
$ operator-sdk init  --domain example.org  --repo github.com/bobbae/gcp/k8s/memcache-operator
$ operator-sdk create api --group cache --version v1alpha1 --kind Memcached --resource --controller
$ ...
```
If you get error about gcc-5,
https://askubuntu.com/questions/1087150/install-gcc-5-on-ubuntu-18-04

Follow through until the step to build docker

```
$ make docker-build docker-push  IMG=gcr.io/${PROJECT}/memcached-operator:v0.0.1
$ make deploy   IMG=gcr.io/${PROJECT}/memcached-operator:v0.0.1
$ kubectl get deployment -n memcache-operator-system
```

After installing OLM `operator-sdk olm install`,

```
$ make bundle IMG=gcr.io/${PROJECT}/memcached-operator:v0.0.1
$ make bundle-build BUNDLE_IMG=gcr.io/${PROJECT}/memcached-operator-bundle:v0.0.1
$ make docker-push IMG=gcr.io/${PROJECT}/memcached-operator-bundle:v0.0.1
$ operator-sdk run bundle gcr.io/${PROJECT}/memcached-operator-bundle:v0.0.1
```


