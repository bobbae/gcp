#!/usr/bin/env python3
# Copyright (c) 2019 Ekaba Bisong

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import kfp.dsl as dsl

class ObjectDict(dict):
  def __getattr__(self, name):
    if name in self:
      return self[name]
    else:
      raise AttributeError("No such attribute: " + name)


@dsl.pipeline(
  name='crypto',
  description='Train Bitcoin closing prediction model'
)
def train_and_deploy(
    project='oceanic-sky-230504',
    source_bucket='kubeflow-ekaba-bucket',
    target_bucket='kubeflow-ekaba-bucket'
):
  """Pipeline to train crypto model"""

  # Step 1: transfer the raw dataset from github to gcs
  raw_transfer = dsl.ContainerOp(
    name='raw_data_transfer',
    # image needs to be a compile-time string
    image='gcr.io/oceanic-sky-230504/crypto-move-raw-to-gcs:latest',
    arguments=[
      target_bucket
    ],
    file_outputs={'target_bucket': '/output.txt'}
  )

  # Step 2: create training dataset using Apache Beam on Cloud Dataflow
  preprocess = dsl.ContainerOp(
    name='preprocess',
    # image needs to be a compile-time string
    image='gcr.io/oceanic-sky-230504/crypto-pipeline-dataflow-transform:latest',
    arguments=[
      '--project', project,
      '--source_bucket', source_bucket,
      '--target_bucket', raw_transfer.outputs['target_bucket']
    ],
    file_outputs={'bucket': '/output.txt'}
  )

  # Step 3: Do hyperparameter tuning of the model on Cloud ML Engine
  hparam_train = dsl.ContainerOp(
    name='hypertrain',
    # image needs to be a compile-time string
    image='gcr.io/oceanic-sky-230504/crypto-pipeline-cloud-hypertune-train:latest',
    arguments=[
      preprocess.outputs['bucket']
    ],
    file_outputs={'jobname': '/output.txt'}
  )

  # Step 4: Train the model with the optimized hyper-parameters
  train_optimized_hyperparams = dsl.ContainerOp(
    name='train_optimized_hyperparams',
    # image needs to be a compile-time string
    image='gcr.io/oceanic-sky-230504/crypto-pipeline-train-best-hyperparam:latest',
    arguments=[
      hparam_train.outputs['jobname'],
      target_bucket
    ],
    file_outputs={'train': '/output.txt'}
  )

  # Step 5: Deploy the trained model to Cloud ML Engine
  deploy_cloud_mle = dsl.ContainerOp(
    name='deploy-model-cloud-mle',
    # image needs to be a compile-time string
    image='gcr.io/oceanic-sky-230504/crypto-deploy-cloudmle:latest',
    arguments=[
      train_optimized_hyperparams.outputs['train'],
      'crypto',
      'v1'
    ],
    file_outputs={
      'model': '/model.txt',
      'version': '/version.txt'
    }
  )

if __name__ == '__main__':
  import kfp.compiler as compiler
  import sys
  if len(sys.argv) != 2:
    print("Usage: mlp_crypto  pipeline-output-name")
    sys.exit(-1)
  
  filename = sys.argv[1]
  compiler.Compiler().compile(train_and_deploy, filename)