#!/bin/bash -ex

if [ "$#" -ne 2 ]; then
    echo "Usage: ./train.sh  hyperparam_jobname  bucket-name"
    exit
fi

# activate gcloud credentials
gcloud auth activate-service-account --key-file=./crypto/service_account.json
gcloud config set project oceanic-sky-230504
GOOGLE_APPLICATION_CREDENTIALS=./crypto/service_account.json

HYPERJOB=$1
BUCKET=$2
TFVERSION=1.8
REGION=us-central1
TRAIN_FILE=gs://${BUCKET}/transformed-crypto-bitcoin-00-of-02.csv
EVAL_FILE=gs://${BUCKET}/transformed-crypto-bitcoin-01-of-02.csv

echo "Extracting information for job $HYPERJOB"

# get information from the best hyperparameter job
RMSE=$(gcloud ml-engine jobs describe $HYPERJOB --format 'value(trainingOutput.trials.finalMetric.objectiveValue.slice(0))')
LEARNING_RATE=$(gcloud ml-engine jobs describe $HYPERJOB --format 'value(trainingOutput.trials.hyperparameters.learning-rate.slice(0))')
FIRST_LAYER_SIZE=$(gcloud ml-engine jobs describe $HYPERJOB --format 'value(trainingOutput.trials.hyperparameters.first-layer-size.slice(0))')
NUM_LAYERS=$(gcloud ml-engine jobs describe $HYPERJOB --format 'value(trainingOutput.trials.hyperparameters.num-layers.slice(0))')
SCALE_FACTOR=$(gcloud ml-engine jobs describe $HYPERJOB --format 'value(trainingOutput.trials.hyperparameters.scale-factor.slice(0))')
TRIALID=$(gcloud ml-engine jobs describe $HYPERJOB --format 'value(trainingOutput.trials.trialId.slice(0))')

echo "Continuing to train model in trial_id=$TRIALID with learning_rate=$LEARNING_RATE first_layer_size=$FIRST_LAYER_SIZE num_layers=$NUM_LAYERS scale_factor=$SCALE_FACTOR"

# directory containing trainer package in Docker image
# see Dockerfile
CODEDIR=./crypto

OUTDIR=gs://${BUCKET}/crypto/hyperparam/$TRIALID
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
  --runtime-version=$TFVERSION \
  --stream-logs \
  -- \
  --train-files $TRAIN_FILE \
  --eval-files $EVAL_FILE \
  --learning_rate $LEARNING_RATE \
  --first-layer-size $FIRST_LAYER_SIZE \
  --num-layers $NUM_LAYERS \
  --scale-factor $SCALE_FACTOR \
  --train-steps 5000 \
  --eval-steps 100

gcloud ml-engine jobs stream-logs $JOBNAME

# note --stream-logs above so that we wait for job to finish
# write output file for next step in pipeline
echo $OUTDIR > /output.txt