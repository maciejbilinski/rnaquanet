FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone

# packages installation
RUN apt-get update  
RUN apt-get upgrade -y 
RUN apt-get install -y tzdata wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev \
        libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev software-properties-common openjdk-8-jdk git \
        curl redis-server

# python installation
RUN add-apt-repository -y ppa:deadsnakes/ppa 
RUN apt-get -y install python3.11 
RUN ln -sf /usr/bin/python3.11 /usr/bin/python 
RUN ln -sf /usr/bin/python3.11 /usr/bin/python3 
RUN wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py && \
python3.11 get-pip.py

# pytorch installation
RUN python -m pip install torch==2.0.1 --index-url https://download.pytorch.org/whl/cu118
RUN python -m pip install torch-geometric==2.3.1
RUN python -m pip install --no-index torch-scatter==2.1.1 -f https://pytorch-geometric.com/whl/torch-2.0.1+cu118.html

# node installation
RUN dpkg --remove --force-remove-reinstreq libnode-dev && dpkg --remove --force-remove-reinstreq libnode72:amd64
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash -
RUN apt install -y nodejs

# file configuration
COPY . /app
WORKDIR /app

# python configuration
RUN python -m pip install --ignore-installed -r requirements.txt
ENV PYTHONPATH=/app
RUN apt-get install ca-certificates curl
RUN install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
RUN chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

RUN apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io

RUN bash
