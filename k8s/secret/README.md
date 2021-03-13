# Using secret

```
$ kubectl apply -f mysecret.yaml
$ kubectl apply -f mypod.yaml
$ echo  YWRtaW4=|base64 -d
admin%                                                                                                                               $ echo  MWYyZDFlMmU2N2Rm|base64 -d
1f2d1e2e67df%                                                     
$ kubectl logs secret-test-pod
```
