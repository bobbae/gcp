# cockroach DB


## Using the cockroach db operator

https://www.cockroachlabs.com/docs/stable/orchestrate-a-local-cluster-with-kubernetes.html


```
kubectl apply -f https://raw.githubusercontent.com/cockroachdb/cockroach-operator/master/config/crd/bases/crdb.cockroachlabs.com_crdbclusters.yaml
kubectl apply -f https://raw.githubusercontent.com/cockroachdb/cockroach-operator/master/manifests/operator.yaml
# curl -O https://raw.githubusercontent.com/cockroachdb/cockroach-operator/master/examples/example.yaml
# edit example.yaml
kubectl apply -f example.yaml
```


Then wait a bit for pods to come up and login to do SQL commands:

```
kubectl exec -it cockroachdb-2 -- ./cockroach sql --certs-dir cockroach-certs
CREATE DATABASE bank;
CREATE TABLE bank.accounts (id INT PRIMARY KEY, balance DECIMAL);
INSERT INTO bank.accounts VALUES (1, 1000.50);
SELECT * FROM bank.accounts;
CREATE USER roach WITH PASSWORD 'Q7gc8rEdS';
GRANT admin TO roach;
\q
```

Run service
```
kubectl port-forward service/cockroachdb-public 8080
```

The cockroach db web console is available at https://localhost:8080

## Simulate node failure

```
kubectl delete pod cockroachdb-2
```

