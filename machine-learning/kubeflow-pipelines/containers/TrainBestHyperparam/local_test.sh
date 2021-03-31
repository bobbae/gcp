#!/bin/bash -e
./build.sh; docker run gcr.io/oceanic-sky-230504/crypto-pipeline-train-best-hyperparam:latest crypto_190325_053340 kubeflow-ekaba-bucket
