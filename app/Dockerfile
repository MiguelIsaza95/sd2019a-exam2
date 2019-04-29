FROM python:3.6
#FROM fluent/fluentd:v1.2.6-debian

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
#RUN apt-get install -yqq python python-dev python-pip
#RUN pip install pyramid 
RUN pip install -r requirements.txt
#RUN apt update -y && apt install vim -y
#RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-rdoc", "--no-ri", "--version", "2.12.0"]

COPY app.py /app
CMD python app.py
