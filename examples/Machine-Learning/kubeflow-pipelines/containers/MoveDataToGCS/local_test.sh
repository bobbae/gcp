#!/bin/bash -e
./build.sh; docker run -t crypto-move-raw-to-gcs:latest kubeflow-ekaba-bucket