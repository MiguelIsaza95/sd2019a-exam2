FROM ubuntu:14.04
FROM fluent/fluentd:v1.2.6-debian
MAINTAINER Your Name <jonathan.arias@correo.icesi.edu.co>

ENV HOME /root
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -yqq update
RUN apt-get install -yqq python python-dev python-pip
RUN pip install pyramid
RUN apt update -y && apt install vim -y
RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-rdoc", "--no-ri", "--version", "2.12.0"]

WORKDIR /code
CMD ["python", "app.py"]
