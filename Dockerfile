FROM python:3.8
MAINTAINER 'repavn@gmail.com'
RUN mkdir /opt/app
WORKDIR /opt/app
COPY . .

RUN apt-get update && apt-get install -y python-pip redis-server
RUN rm /etc/redis/redis.conf
RUN mv redis.conf /etc/redis
RUN /etc/init.d/redis-server restart
RUN pip install -r requirements.txt

