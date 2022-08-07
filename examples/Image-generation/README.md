
## testReal-ESRGAN.py

Using and training ImagenT5-3B and Real-ESRGAN.  https://github.com/xinntao/Real-ESRGAN

Based on http://github.com/cene555/Imagen-pytorch

Setting up environment may look roughly the same as below on a machine with Nvidia GPU and CUDA support:
```
cd ~
curl -O http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_10.0.130-1_amd64.deb
dpkg -i cuda-repo-ubuntu1604_10.0.130-1_amd64.deb
apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
apt-get update
apt-get install cuda-10-0 cuda-drivers -y
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
apt-get update
apt-get -y install cuda
#git clone https://github.com/lucidrains/imagen-pytorch
#pip install imagen-pytorch
pip remove numpy
pip install numpy==1.20
pip install git+https://github.com/cene555/Imagen-pytorch.git
pip install git+https://github.com/openai/CLIP.git
pip install basicsr facexlib gfegan gfpgan torch
pip install numpy pillow basicsr lmdb scipy tb-nightly yapf filterpy numba Pillow scipy
pip install typing_extensions
pip install -r requirements.txt
git lfs install
git clone https://github.com/xinntao/Real-ESRGAN.git
cd Real-ESRGAN/
python setup.py develop
cd ~
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P experiments/pretrained_models
git clone https://huggingface.co/Cene655/ImagenT5-3B
```

To check if GPU is working:
```
lsmod |grep -i nvidia
nvidia-smi
/usr/local/cuda/bin/nvcc hello.cu
./a.out
```
