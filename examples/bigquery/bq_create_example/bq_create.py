from google.cloud import bigquery
import os

project_id = os.getenv("DEVSHELL_PROJECT_ID")
if project_id == None:
    print 'cannot get project id, possibly missing env var DEVSHELL_PROJECT_ID, please set DEVSHELL_PROJECT_ID env var'
    exit(1)
print 'project id is', project_id

# Construct a BigQuery client object.
client = bigquery.Client(project=project_id)

dataset_id = project_id + ".example_dataset1"
print("dataset_id",dataset_id)
#dataset = client.get_dataset(dataset_id)

dataset = client.create_dataset(dataset_id, timeout=30) 
print("creating new dataset")

# TODO(developer): Specify the geographic location where the dataset should reside.
dataset.location = "US"

# Send the dataset to the API for creation, with an explicit timeout.
# Raises google.api_core.exceptions.Conflict if the Dataset already
# exists within the project.
#dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name"
table_id = dataset_id + ".example_table1"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ],
    skip_leading_rows=1,
    # The source format defaults to CSV, so the line below is optional.
    source_format=bigquery.SourceFormat.CSV,
)
uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)  # Make an API request.
print("Loaded {} rows.".format(destination_table.num_rows))
