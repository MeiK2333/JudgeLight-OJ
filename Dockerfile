FROM python:3.6.8-stretch

COPY . /judge
WORKDIR /judge
# install openjdk-8
# RUN apt-get update && \
#     apt-get install -y openjdk-8-jdk && \
#     apt-get install -y ant && \
#     apt-get clean
RUN pip install -r requirements.txt
