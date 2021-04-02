# argo examples

## install argo

https://argoproj.github.io/argo-workflows/quick-start/

```
kubectl create ns argo
kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo-workflows/stable/manifests/quick-start-postgres.yaml
```

## examples 

https://github.com/argoproj/argo-workflows/tree/master/examples

To run an example

```
argo submit -n argo --watch https://raw.githubusercontent.com/argoproj/argo-workflows/master/examples/coinflip.yaml

Name:                coinflip-tjc65
Namespace:           argo
ServiceAccount:      default
Status:              Succeeded
Conditions:
 Completed           True
Created:             Mon Mar 15 12:56:13 -0700 (30 seconds ago)
Started:             Mon Mar 15 12:56:13 -0700 (30 seconds ago)
Finished:            Mon Mar 15 12:56:43 -0700 (now)
Duration:            30 seconds
Progress:            2/2
ResourcesDuration:   21s*(1 cpu),21s*(100Mi memory)

STEP               TEMPLATE   PODNAME                    DURATION  MESSAGE
 ✔ coinflip-tjc65  coinflip
 ├───✔ flip-coin   flip-coin  coinflip-tjc65-243219171   19s
 └─┬─✔ heads       heads      coinflip-tjc65-3214171722  7s
   └─○ tails       tails                                           when 'heads == tails' evaluated false
```
