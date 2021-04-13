# Kubebuilder example

 https://book.kubebuilder.io/quick-start.html
 
Created by 

```
$ kubebuilder init --project-version=2 --domain example.org --license apache2 --owner "The Kubernetes authors"
$ kubebuilder create api --group ship --version v1beta1 --kind Frigate
```

```
# make docker image and push
$ make docker-build docker-push IMG=xy/abc:v1
$ make deploy IMG=xy/abc:v1
$ kubectl get pods --all-namespaces
# make sure you don't have errors like ErrImagePull
$ make install  #install CRDs
$ kubectl apply -f config/samples/
$ kubectl get crds
# observe you have new crd
$ kubectl get frigate
$ kubectl get frigate frigate-sample
# modify and add new values in config/samples/ship_v1beta1_frigate.yaml
$ kubectl apply -f config/samples/
# see it changed
$ kubectl get frigate frigate-sample
$ kubectl get pods --all-namespaces # get pod name for kubebuilder-example-controller-manager
# get logs from a container called manager from the pod kubebuilder-example-controller-manager-XXXXXXX
# get a list of containers in a pod
$ kubectl describe pod/kubebuilder-example-controller-manager-XXXXXXXXXXX -n kubebuilder-example-system
$ kubectl logs kubebuilder-example-controller-manager-XXXXXXXXXXX -n kubebuilder-example-system -c manager
# each time config/samples/ship_v1beta1_frigate.yaml change and applied you will see a log added
```


