# cratedb 

https://github.com/crate/crate-operator

## Install Operator
$ kubectl --namespace dev create -f dev-cluster.yaml
...

$ kubectl --namespace dev get cratedbs
NAMESPACE   NAME         AGE
dev         my-cluster   36s


## Using the operator.

```
$ kubectl --namespace dev create -f dev-cluster.yaml
...

$ kubectl --namespace dev get cratedbs
NAMESPACE   NAME         AGE
dev         my-cluster   36s
```


