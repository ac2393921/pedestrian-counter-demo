FROM python:3.8

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6

WORKDIR /root/work

COPY ../requirements.txt ./

RUN python3 -m pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

RUN rm -rf /var/lib/apt/lists/*