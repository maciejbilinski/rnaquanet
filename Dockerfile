FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

RUN apt update && \ 
apt install -y wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev \
libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev software-properties-common openjdk-8-jdk && \ 
add-apt-repository -y ppa:deadsnakes/ppa && \
apt -y install python3.11 && \ 
ln -sf /usr/bin/python3.11 /usr/bin/python && \
ln -sf /usr/bin/python3.11 /usr/bin/python3 && \ 
wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py && \
python3.11 get.pip.py


COPY . /app

WORKDIR /app

RUN python -m pip install -r torch==2.0.1 --index-url https://download.pytorch.org/whl/cu118

RUN python -m pip install --no-index torch-geometric==2.3.1 torch-scatter==2.1.1 -f https://pytorch-geometric.com/whl/torch-2.0.1+cu118.html

RUN python -m pip install -r requirements.txt


CMD ["bash"]
