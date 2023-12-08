# load base image
FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04
# copy requirement.txt file inside docker image
COPY ./requirements.txt /
# install python3 and then install dependencies using pip3 and then clean apt cache
RUN apt update && apt install -y \
    python3 python3-pip && \
    pip3 install -r requirements.txt && \
    apt clean && rm -rf /var/lib/apt/lists/*
# copy necessary files to docker image
COPY ./inference /inference/
# run app.py
CMD python3 app.py