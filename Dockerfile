FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone

RUN apt-get update  
RUN apt-get upgrade -y 
RUN apt install -y tzdata wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev \
        libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev software-properties-common openjdk-8-jdk git
RUN add-apt-repository -y ppa:deadsnakes/ppa 
RUN apt-get -y install python3.11 
RUN ln -sf /usr/bin/python3.11 /usr/bin/python 
RUN ln -sf /usr/bin/python3.11 /usr/bin/python3 


RUN wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py && \
python3.11 get-pip.py


RUN python -m pip install torch==2.0.1 --index-url https://download.pytorch.org/whl/cu118

RUN python -m pip install torch-geometric==2.3.1

RUN python -m pip install --no-index torch-scatter==2.1.1 -f https://pytorch-geometric.com/whl/torch-2.0.1+cu118.html

COPY . /app

WORKDIR /app

RUN python -m pip install -r requirements.txt

ENV PYTHONPATH=/app

RUN bash
