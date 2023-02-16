# Must use a Cuda version 11+
FROM nvidia/cuda:10.1-cudnn8-devel-ubuntu18.04

WORKDIR /

# Install git
RUN apt-get update && apt-get install -y git

#install python
RUN apt-get install -y python3.8
RUN apt-get install -y python3-pip

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Install python packages
RUN python3.8 -m pip install --upgrade pip
ADD requirements.txt requirements.txt
RUN python3.8 -m pip install -r requirements.txt

# We add the banana boilerplate here
ADD server.py .
EXPOSE 8000

# Add your huggingface auth key here
ENV HF_AUTH_TOKEN=your_token

# Add your model weight files 
# (in this case we have a python script)
ADD download.py .
RUN python3.8 download.py

# Add your custom app code, init() and inference()
ADD app.py .
ADD ./ .

CMD python3.8 -u server.py
