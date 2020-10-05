# set parent image
FROM python:3.7-alpine

# set working directory
WORKDIR /app

#
COPY ./requirements.txt /app/requirements.txt

#
RUN  apt-get install gcc -y && apt-get clean

#
RUN pip3 install -r /app/requirements.txt && rm -rf /root/.cache/pip3

# copy all files to /app
COPY . /app/

