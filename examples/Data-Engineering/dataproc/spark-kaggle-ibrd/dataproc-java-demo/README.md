# Google Cloud Dataproc Java/Spark Demo

Code repository for post, [Big Data Analytics with Java and Python, using Cloud Dataproc, Google’s Fully-Managed Spark and Hadoop Service](https://wp.me/p1RD28-63y).

## Run with Arguments

To run `InternationalLoansAppDataproc.java` use the following arguments, locally:

```text
"data"
"ibrd-statement-of-loans-latest-available-snapshot.csv"
"ibrd-small-spark"

.master("yarn") must be changes to .master("local[*]")
```

To run `InternationalLoansAppDataproc.java` on Dataproc:

```text
"gs://dataproc-demo-bucket"
"ibrd-statement-of-loans-historical-data.csv"
"ibrd-large-spark"
```
