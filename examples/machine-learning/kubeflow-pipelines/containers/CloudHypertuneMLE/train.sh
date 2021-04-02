#!/bin/bash -e

if [ "$#" -ne 1 ]; then
    echo "Usage: ./train.sh  bucket-name"
    exit
fi

# activate gcloud credentials
gcloud auth activate-service-account --key-file=./crypto/service_account.json
gcloud config set project oceanic-sky-230504
GOOGLE_APPLICATION_CREDENTIALS=./crypto/service_account.json

BUCKET=$1
TFVERSION=1.8
REGION=us-central1
TRAIN_FILE=gs://${BUCKET}/transformed-crypto-bitcoin-00-of-02.csv
EVAL_FILE=gs://${BUCKET}/transformed-crypto-bitcoin-01-of-02.csv

# directory containing trainer package in Docker image
# see Dockerfile
CODEDIR=./crypto

OUTDIR=gs://${BUCKET}/crypto/hyperparam
JOBNAME=crypto_$(date -u +%y%m%d_%H%M%S)
echo $OUTDIR $REGION $JOBNAME
# gsutil -m rm -rf $OUTDIR
gcloud ml-engine jobs submit training $JOBNAME \
  --region=$REGION \
  --module-name=trainer.task \
  --package-path=${CODEDIR}/trainer/ \
  --job-dir=$OUTDIR \
  --staging-bucket=gs://$BUCKET \
  --scale-tier=STANDARD_1 \
  --config=${CODEDIR}/hptuning_config.yaml \
  --runtime-version=$TFVERSION \
  --stream-logs \
  -- \
  --train-files $TRAIN_FILE \
  --eval-files $EVAL_FILE \
  --train-steps 5000 \
  --eval-steps 100


gcloud ml-engine jobs stream-logs $JOBNAME

# note --stream-logs above so that we wait for job to finish
# write output file for next step in pipeline
echo $JOBNAME > /output.txt