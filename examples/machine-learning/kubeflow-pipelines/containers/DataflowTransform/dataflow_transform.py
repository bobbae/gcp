#!/usr/bin/env python

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials
import re
import logging
import argparse
import time

def run(project, source_bucket, target_bucket):
    import csv

    job_name = 'kubeflow-dataflow-crypto'
    options = {
        'staging_location': 'gs://{}/staging'.format(source_bucket),
        'temp_location': 'gs://{}/temp'.format(source_bucket),
        'job_name': job_name,
        'project': project,
        'max_num_workers': 24,
        'teardown_policy': 'TEARDOWN_ALWAYS',
        'no_save_main_session': True,
        'runner': 'DataflowRunner'
      }
    options = beam.pipeline.PipelineOptions(flags=[], **options)
    
    crypto_dataset = 'gs://{}/crypto-markets.csv'.format(source_bucket)
    processed_ds = 'gs://{}/transformed-crypto-bitcoin'.format(target_bucket)

    pipeline = beam.Pipeline(options=options)

    # 0:slug, 3:date, 5:open, 6:high, 7:low, 8:close
    rows = (
        pipeline |
            'Read from bucket' >> ReadFromText(crypto_dataset) |
            'Tokenize as csv columns' >> beam.Map(lambda line: next(csv.reader([line]))) |
            'Select columns' >> beam.Map(lambda fields: (fields[0], fields[3], fields[5], fields[6], fields[7], 
                                                         fields[8])) |
            'Filter bitcoin rows' >> beam.Filter(lambda row: row[0] == 'bitcoin')
        )
        
    combined = (
        rows |
            'Write to bucket' >> beam.Map(lambda (slug, date, open, high, low, close): '{},{},{},{},{},{}'.format(
                slug, date, open, high, low, close)) |
            WriteToText(
                file_path_prefix=processed_ds,
                file_name_suffix=".csv", num_shards=2,
                shard_name_template="-SS-of-NN",
                header='slug, date, open, high, low, close')
        )

    pipeline.run()

    # job logging
    logging.info('Looking for jobs with prefix {} in region {}...'.format(job_name, 'us-central1'))
    dataflow = build('dataflow', 'v1b3', credentials=GoogleCredentials.get_application_default())
    result = dataflow.projects().locations().jobs().list(
      projectId=project,
      location='us-central1',
    ).execute()

    job_id = 'none'
    for job in result['jobs']:
      if re.findall(r'' + re.escape(job_name) + '', job['name']):
        job_id = job['id']
        break

    logging.info('Job ID: {}'.format(job_id))

    while(True):
        jobstatus = dataflow.projects().jobs().get(
            projectId=project,
            jobId=job_id
        ).execute()

        if jobstatus['currentState'] == 'JOB_STATE_DONE':
            # the next step of pipeline will look for this file
            with open('/output.txt', 'w') as output_file:
                output_file.write(target_bucket)
                print('Done!')
            break
        else:            
            time.sleep(60)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('--project',
                        type=str,
                        required=True,
                        help='The GCP project to run the dataflow job.')
    parser.add_argument('--source_bucket',
                        type=str,
                        required=True,
                        help='Source bucket containing raw data.')
    parser.add_argument('--target_bucket',
                        type=str,
                        required=True,
                        help='Target bucket to store outputs.')

    args = parser.parse_args()

    run(args.project, args.source_bucket, args.target_bucket)