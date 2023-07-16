from nvidia/cuda:11.8.0-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip 

COPY . /app

WORKDIR /app

RUN pip3 install -r src/requirements.txt 
CMD ["bash"]
