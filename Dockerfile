FROM debian:buster-slim
RUN apt-get update && apt-get install -y git gcc g++ make apt-utils build-essential autoconf automake libtool python3 python3-rpi.gpio python3-pip python3-numpy libfreetype6-dev libjpeg-dev libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-mixer1.2-dev libsdl-image1.2-dev
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
WORKDIR /usr/src/app
COPY ./CODE2000.TTF ./main.py ./
CMD python3 main.py
