# End-to-end ML solution on Kubeflow pipelines

From chapter 47 of the book Machine Learning and Deep Learning Models on Google Cloud Platform.

https://github.com/Apress/building-ml-and-dl-models-on-gcp

## Overview

Steps:

1. Move raw data on Github to storage bucket
2. Transform dataset using Google Dataflow
3. Carray out hyper-parameter training on Cloud ML engine
4. Train the model with optimized hyper-parameters
5. Deploy the model for serving on Cloud MLE

## containers

There are 5 containers under `containers` directory here. They can be built via `build.sh` in each directory, which will build the docker image and push to the docker image registry at `gcr.io`.  The script `build_containers.sh` will go through each of the directories and call the `build.sh`.

The following are the containers that match the steps: 

1. MoveDataToGCS
2. DataflowTransform
3. CloudHypertuneMLE
4. TrainBestHyperparam
5. DeployCMLE
 
## GKE cluster

You will need GKE cluster to run the kubeflow.

```
gcloud container clusters create my-gke-cluster-name
```

Install kubeflow using `kfctl.sh` script.
```
mkdir kubeflow

cd kubeflow

export KUBEFLOW_SRC=$(pwd)

export KUBEFLOW_TAG=v0.5.0

curl https://raw.githubusercontent.com/kubeflow/kubeflow/${KUBEFLOW_TAG}/scripts/download.sh | bash

export KFAPP=my-kubeflow-app

${KUBEFLOW_SRC}/scripts/kfctl.sh init ${KFAPP} --platform gcp --project ${PROJECT}

cd ${KFAPP}

${KUBEFLOW_SRC}/scripts/kfctl.sh generate platform

${KUBEFLOW_SRC}/scripts/kfctl.sh apply platform

${KUBEFLOW_SRC}/scripts/kfctl.sh generate k8s

${KUBEFLOW_SRC}/scripts/kfctl.sh apply k8s

kubectl -n kubeflow get all

```


## Kubeflow

Each of the steps will be part of the pieline for kubeflow. Install kubeflow pipelines SDK which includes DSL language compiler `dsl-compile`. First you need python3 and probably virtual environment.

```
pip install https://storage.googleapis.com/ml-pipeline/release/0.1.12/kfp.tar.gz --upgrade
```

Or follow directions from https://www.kubeflow.org/docs/components/pipelines/sdk/install-sdk/

Verify the installation of `dsl-compile`:
```
which dsl-compile
```

To compile the pipeline
```
python3 crypto_pipeline.py crypto_pipeline.tar.gz
```

You can then upload the pipeline to Kubeflow using `upload pipeline` button on your kubeflow instance on GCP and create and run the experiment using the pipeline.



