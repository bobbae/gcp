#!/bin/sh -e
./build.sh; docker run gcr.io/oceanic-sky-230504/crypto-deploy-cloudmle:latest gs://kubeflow-ekaba-bucket/crypto/hyperparam/4 crypto v1