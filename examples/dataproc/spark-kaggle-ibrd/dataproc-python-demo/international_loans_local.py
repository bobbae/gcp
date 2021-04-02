#!/usr/bin/python

# Author: Gary A. Stafford
# License: MIT

from pyspark.sql import SparkSession


def main():
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName('dataproc-python-demo') \
        .getOrCreate()

    # Defaults to INFO
    sc = spark.sparkContext
    sc.setLogLevel("INFO")

    # Loads CSV file from local directory
    df_loans = spark \
        .read \
        .format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .load("data/ibrd-statement-of-loans-latest-available-snapshot.csv")

    # Prints basic stats
    print "Rows of data:" + str(df_loans.count())
    print "Inferred Schema:"
    df_loans.printSchema()

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

    df_disbursement.show(25, True)

    # Saves results to a locally CSV file
    df_disbursement.repartition(1) \
        .write \
        .mode("overwrite") \
        .format("csv") \
        .option("header", "true") \
        .save("data/ibrd-summary-small-python")

    print "Results successfully written to CSV file"

    spark.stop()


if __name__ == "__main__":
    main()
