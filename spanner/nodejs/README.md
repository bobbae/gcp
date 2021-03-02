# Spanner

https://cloud.google.com/spanner/docs/getting-started/nodejs

```
$ npm i @google-cloud/spanner
$ gcloud spanner instances create test-instance --config=regional-us-central1 \
    --description="Test Instance" --nodes=1
$ node schema.js createDatabase test-instance example-db $PROJECT
$ node quickstart.js
$ npm i yargs

$ node dml.js writeUsingDml test-instance example-db $PROJECT

$ node crud.js insert test-instance example-db $PROJECT

$ gcloud spanner databases execute-sql example-db --instance=test-instance \
    --sql='SELECT SingerId, AlbumId, AlbumTitle FROM Albums'
SingerId  AlbumId  AlbumTitle
1         1        Total Junk
1         2        Go, Go, Go
2         1        Green
2         2        Forever Hold your Peace
2         3        Terrified

$ node crud.js query test-instance example-db $PROJECT
SingerId: 1, AlbumId: 1, AlbumTitle: Total Junk
SingerId: 1, AlbumId: 2, AlbumTitle: Go, Go, Go
SingerId: 2, AlbumId: 1, AlbumTitle: Green
SingerId: 2, AlbumId: 2, AlbumTitle: Forever Hold your Peace
SingerId: 2, AlbumId: 3, AlbumTitle: Terrified

$ node dml.js queryWithParameter test-instance example-db $PROJECT
SingerId: 12, FirstName: Melissa, LastName: Garcia

$ node crud.js read test-instance example-db $PROJECT
SingerId: 1, AlbumId: 1, AlbumTitle: Total Junk
SingerId: 1, AlbumId: 2, AlbumTitle: Go, Go, Go
SingerId: 2, AlbumId: 1, AlbumTitle: Green
SingerId: 2, AlbumId: 2, AlbumTitle: Forever Hold your Peace
SingerId: 2, AlbumId: 3, AlbumTitle: Terrified
```

These do the same alteration to the table.
```
$ gcloud spanner databases ddl update example-db --instance=test-instance \
    --ddl='ALTER TABLE Albums ADD COLUMN MarketingBudget INT64'

$ node schema.js addColumn test-instance example-db $PROJECT

```

There are much more steps you can try at:
https://cloud.google.com/spanner/docs/getting-started/nodejs

