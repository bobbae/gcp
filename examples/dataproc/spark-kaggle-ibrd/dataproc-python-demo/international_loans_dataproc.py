#!/usr/bin/python

# Author: Gary A. Stafford
# License: MIT
# Arguments Example:
# gs://dataproc-demo-bucket
# ibrd-statement-of-loans-historical-data.csv
# ibrd-summary-large-python

from pyspark.sql import SparkSession
import sys


def main(argv):
    storage_bucket = argv[0]
    data_file = argv[1]
    results_directory = argv[2]

    print "Number of arguments: {0} arguments.".format(len(sys.argv))
    print "Argument List: {0}".format(str(sys.argv))

    spark = SparkSession \
        .builder \
        .master("yarn") \
        .appName('dataproc-python-demo') \
        .getOrCreate()

    # Defaults to INFO
    sc = spark.sparkContext
    sc.setLogLevel("WARN")

    # Loads CSV file from Google Storage Bucket
    df_loans = spark \
        .read \
        .format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .load(storage_bucket + "/" + data_file)

    # Creates temporary view using DataFrame
    df_loans.withColumnRenamed("Country", "country") \
        .withColumnRenamed("Country Code", "country_code") \
        .withColumnRenamed("Disbursed Amount", "disbursed") \
        .withColumnRenamed("Borrower's Obligation", "obligation") \
        .withColumnRenamed("Interest Rate", "interest_rate") \
        .createOrReplaceTempView("loans")

    # Performs basic analysis of dataset
    df_disbursement = spark.sql("""
    SELECT country, country_code,
            format_number(total_disbursement, 0) AS total_disbursement,
            format_number(ABS(total_obligation), 0) AS total_obligation,
            format_number(avg_interest_rate, 2) AS avg_interest_rate
            FROM (
            SELECT country, country_code,
            SUM(disbursed) AS total_disbursement,
            SUM(obligation) AS total_obligation,
            AVG(interest_rate) AS avg_interest_rate
            FROM loans
            GROUP BY country, country_code
            ORDER BY total_disbursement DESC
            LIMIT 25)
    """).cache()

    print "Results:"
    df_disbursement.show(25, True)

    # Saves results to single CSV file in Google Storage Bucket
    df_disbursement.write \
        .mode("overwrite") \
        .format("parquet") \
        .save(storage_bucket + "/" + results_directory)

    spark.stop()


if __name__ == "__main__":
    main(sys.argv[1:])
