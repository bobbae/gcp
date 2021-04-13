#!/bin/bash -e

if [ -z "$1" ]; then
  BUCKET_NAME=kubeflow-ekaba-bucket
else
  BUCKET_NAME=$1
fi

# gcloud configuration
gcloud auth activate-service-account --key-file=./crypto/service_account.json
gcloud config set project oceanic-sky-230504

# create bucket
gsutil mb gs://${BUCKET_NAME}

# transfer file from github
curl https://raw.githubusercontent.com/dvdbisong/gcp-learningmodels-book/master/Chapter_09/crypto-markets.csv | gsutil cp - gs://${BUCKET_NAME}/crypto-markets.csv

# write output file for next step in pipeline
echo $BUCKET_NAME > /output.txt