from nvidia/cuda:11.8.0-runtime-ubuntu22.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-pip wget supervisor && \ 
    apt-get install -y aptitude build-essential dos2unix zip # java dependencies \
    apt-get install -y dos2unix # ensure LF

# prepare java structure descriptor

RUN wget -P /opt/ https://rnasolo.cs.put.poznan.pl/media/describe_structure.zip 

RUN cd /opt/ && \
    unzip describe_structure.zip
	
RUN rm /opt/describe_structure.zip

WORKDIR /opt/describe_structure/



RUN chmod +x /opt/describe_structure/describe

# ---------------------------------

WORKDIR /opt/rnaquanet
COPY . /opt/rnaquanet

RUN pip3 install -r requirements.txt
COPY supervisor.conf /etc/supervisor/conf.d/supervisord.conf

# force CRLF -> LF
RUN dos2unix docker-entrypoint.sh
