# Must use a Cuda version 11+
FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime

RUN export LD_LIBRARY_PATH=/usr/local/cuda-11.3/lib64:$LD_LIBRARY_PATH
#RUN export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
RUN export CUDA_HOME=/usr/local/cuda-11.3

WORKDIR /

# Install git
RUN apt-get update && apt-get install -y git

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Install python packages
RUN pip3 install --upgrade pip
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# We add the banana boilerplate here
ADD server.py .
EXPOSE 8000

# Add your huggingface auth key here
ENV HF_AUTH_TOKEN=your_token

# Add your model weight files 
# (in this case we have a python script)
ADD download.py .
RUN python3 download.py

# Add your custom app code, init() and inference()
ADD app.py .
ADD ./ .

CMD python3 -u server.py
