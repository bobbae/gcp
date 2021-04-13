#!/bin/bash -e
./build.sh; docker run -t crypto-pipeline-cloud-hypertune-train:latest kubeflow-ekaba-bucket