# custom terraform provider for hashicups

https://learn.hashicorp.com/tutorials/terraform/provider-use?in=terraform/providers

## run hashicups server

```
$ cd learn-terraform-hashicups-provider/docker-compose
$ docker-compose up

```

Verify it is running OK.
Go to another termainal and

```
$ curl localhost:19019/health
ok
```

## Build  the provider

```
$ cd ../terraform-provider-hashicups/
$ go build
$ mkdir -p ~/.terraform.d/plugins/hashicorp.com/edu/hashicups/0.3.1/linux_amd64 
$ cp terraform-provider-hashicups ~/.terraform.d/plugins/hashicorp.com/edu/hashicups/0.3.1/linux_amd64 
```

## create new hashicups user

```
$ curl -X POST localhost:19090/signup -d '{"username":"education", "password":"test123"}'
$ curl -X POST localhost:19090/signin -d '{"username":"education", "password":"test123"}'
```

Save the hash printed via `signin` above and set to HASHCUPS_TOKEN.

```
$ export HASHICUPS_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Run terraform using custom plugin

```
$ terraform init
$ terraform apply
```

There are more steps to update and delete you can try at the reference site.
