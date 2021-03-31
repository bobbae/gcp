#!/bin/bash -e
./build.sh ; docker run -t crypto-pipeline-dataflow-transform:latest --project oceanic-sky-230504 --source_bucket kubeflow-ekaba-bucket --target_bucket kubeflow-ekaba-bucket