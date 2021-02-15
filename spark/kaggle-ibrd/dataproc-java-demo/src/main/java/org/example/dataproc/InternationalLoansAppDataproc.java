package org.example.dataproc;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SaveMode;
import org.apache.spark.sql.SparkSession;

/**
 * The InternationalLoansAppDataproc Spark job accepts three input arguments.
 * The program is designed to run on Google Cloud Dataproc.
 *
 * @author  Gary A. Stafford
 * @version 1.0
 * @since   2018-12-16
 */
public class InternationalLoansAppDataproc {

    private static String storageBucket;
    private static String dataFile;
    private static String resultsDirectory;

    public static void main(String[] args) {

        if (args.length == 3) {
            storageBucket = args[0];
            dataFile = args[1];
            resultsDirectory = args[2];

            for (String s : args) {
                System.out.println(s);
            }
        } else {
            throw new IllegalArgumentException("Missing required arguments.");
        }

        InternationalLoansAppDataproc app = new InternationalLoansAppDataproc();
        app.start();
    }

    private void start() {

        SparkSession spark = SparkSession.builder()
                .appName("dataproc-java-demo")
                .master("yarn")
                .getOrCreate();

        spark.sparkContext().setLogLevel("WARN"); // INFO by default

        // Loads CSV file from Google Storage Bucket
        Dataset<Row> dfLoans = spark.read()
                .format("csv")
                .option("header", "true")
                .option("inferSchema", true)
                .load(String.format("%s/%s", storageBucket, dataFile));

        // Creates temporary view using DataFrame
        dfLoans.withColumnRenamed("Country", "country")
                .withColumnRenamed("Country Code", "country_code")
                .withColumnRenamed("Disbursed Amount", "disbursed")
                .withColumnRenamed("Borrower's Obligation", "obligation")
                .withColumnRenamed("Interest Rate", "interest_rate")
                .createOrReplaceTempView("loans");

        // Performs basic analysis of dataset
        Dataset<Row> dfDisbursement = spark.sql(
                "SELECT country, country_code, "
                        + "format_number(total_disbursement, 0) AS total_disbursement, "
                        + "format_number(ABS(total_obligation), 0) AS total_obligation, "
                        + "format_number(avg_interest_rate, 2) AS avg_interest_rate "
                        + "FROM ( "
                        + "SELECT country, country_code, "
                        + "SUM(disbursed) AS total_disbursement, "
                        + "SUM(obligation) AS total_obligation, "
                        + "AVG(interest_rate) AS avg_interest_rate "
                        + "FROM loans "
                        + "GROUP BY country, country_code "
                        + "ORDER BY total_disbursement DESC "
                        + "LIMIT 25)"
        );

        System.out.println("Results:");
        dfDisbursement.show(25, 100);

        // Saves results to single CSV file in Google Storage Bucket
        dfDisbursement.repartition(1)
                .write()
                .mode(SaveMode.Overwrite)
                .format("parquet")
                .save(String.format("%s/%s", storageBucket, resultsDirectory));

        System.out.println("Results successfully written to CSV file");
    }
}
