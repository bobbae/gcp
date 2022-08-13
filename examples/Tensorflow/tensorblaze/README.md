Tensorflow model for Backblaze data
=========

[Backblaze disk failure dataset](https://www.backblaze.com/blog/hard-drive-reliability-stats-q1-2016/) is disk drive failure stats that are based on vendor, model and [SMART](https://www.backblaze.com/blog/hard-drive-smart-stats/) and some other information.

Using [Tensorflow](https://github.com/tensorflow/tensorflow) it is possible to get a model to predict the failure rates based on the data.  First,  the Backblaze data was cleaned up and preprocessed via some python scripts.  Then the data is used to train a model.


Usage:

```
usage: train.py [-h] [-f FILE] [-t TRAIN] [-p PREDICT]

train backblaze model

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  input file
  -t TRAIN, --train TRAIN
            train and save to file
  -p PREDICT, --predict PREDICT
            predict using model from file
```

Examples:

To train the model:

```
$ python train.py -t modelfailures.tf -f failed.csv
I tensorflow/stream_executor/dso_loader.cc:105] successfully opened CUDA library libcublas.so locally
I tensorflow/stream_executor/dso_loader.cc:105] successfully opened CUDA library libcudnn.so locally
I tensorflow/stream_executor/dso_loader.cc:105] successfully opened CUDA library libcufft.so locally
I tensorflow/stream_executor/dso_loader.cc:105] successfully opened CUDA library libcuda.so.1 locally
I tensorflow/stream_executor/dso_loader.cc:105] successfully opened CUDA library libcurand.so locally
>>>Using input file failed.csv
./failed.csv 4597 bytes.
I tensorflow/core/common_runtime/gpu/gpu_init.cc:102] Found device 0 with properties:
name: GeForce GTX TITAN X
major: 5 minor: 2 memoryClockRate (GHz) 1.2155
pciBusID 0000:81:00.0
Total memory: 12.00GiB
Free memory: 11.87GiB
I tensorflow/core/common_runtime/gpu/gpu_init.cc:126] DMA: 0
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 0:   Y
I tensorflow/core/common_runtime/gpu/gpu_device.cc:755] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce GTX TITAN X, pci bus id: 0000:81:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:755] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce GTX TITAN X, pci bus id: 0000:81:00.0)
---------------------------------
Run id: GIZTH5
Log directory: /tmp/tflearn_logs/
---------------------------------
Training samples: 86
Validation samples: 0
--
Training Step: 6  | total loss: 0.48509
| Adam | epoch: 001 | loss: 0.48509 - acc: 0.9995 -- iter: 86/86
--
Training Step: 12  | total loss: 0.15169
| Adam | epoch: 002 | loss: 0.15169 - acc: 1.0000 -- iter: 86/86
--
Training Step: 18  | total loss: 0.13430
| Adam | epoch: 003 | loss: 0.13430 - acc: 0.9784 -- iter: 86/86
--
Training Step: 24  | total loss: 0.10718
| Adam | epoch: 004 | loss: 0.10718 - acc: 0.9845 -- iter: 86/86
--
Training Step: 30  | total loss: 0.13343
| Adam | epoch: 005 | loss: 0.13343 - acc: 0.9825 -- iter: 86/86
--
Training Step: 36  | total loss: 0.03229
| Adam | epoch: 006 | loss: 0.03229 - acc: 0.9960 -- iter: 86/86
--
Training Step: 42  | total loss: 0.09462
| Adam | epoch: 007 | loss: 0.09462 - acc: 0.9866 -- iter: 86/86
--
Training Step: 48  | total loss: 0.03574
| Adam | epoch: 008 | loss: 0.03574 - acc: 0.9956 -- iter: 86/86
--
Training Step: 54  | total loss: 0.09058
| Adam | epoch: 009 | loss: 0.09058 - acc: 0.9836 -- iter: 86/86
--
Training Step: 60  | total loss: 0.04486
| Adam | epoch: 010 | loss: 0.04486 - acc: 0.9933 -- iter: 86/86
--
```

To use the model:

```
$ python train.py -p modelfailures.tf -d HGST,HMS5C4040ALE640,0,0,0,0,0
I tensorflow/stream_executor/dso_loader.cc:105] successfully opened CUDA library libcublas.so locally
I tensorflow/stream_executor/dso_loader.cc:105] successfully opened CUDA library libcudnn.so locally
I tensorflow/stream_executor/dso_loader.cc:105] successfully opened CUDA library libcufft.so locally
I tensorflow/stream_executor/dso_loader.cc:105] successfully opened CUDA library libcuda.so.1 locally
I tensorflow/stream_executor/dso_loader.cc:105] successfully opened CUDA library libcurand.so locally
I tensorflow/core/common_runtime/gpu/gpu_init.cc:102] Found device 0 with properties:
name: GeForce GTX TITAN X
major: 5 minor: 2 memoryClockRate (GHz) 1.2155
pciBusID 0000:81:00.0
Total memory: 12.00GiB
Free memory: 11.87GiB
I tensorflow/core/common_runtime/gpu/gpu_init.cc:126] DMA: 0
I tensorflow/core/common_runtime/gpu/gpu_init.cc:136] 0:   Y
I tensorflow/core/common_runtime/gpu/gpu_device.cc:755] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce GTX TITAN X, pci bus id: 0000:81:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:755] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce GTX TITAN X, pci bus id: 0000:81:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:755] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce GTX TITAN X, pci bus id: 0000:81:00.0)
I tensorflow/core/common_runtime/gpu/gpu_device.cc:755] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce GTX TITAN X, pci bus id: 0000:81:00.0)
::: [0.47443267703056335, 0.525567352771759]
```
