# fluentd/Dockerfile
FROM fluent/fluentd:v1.2.6-debian
RUN apt update -y && apt install vim -y
RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-rdoc", "--no-ri", "--version", "2.12.0"]


