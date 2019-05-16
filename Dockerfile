FROM python:3.6.8-stretch

COPY . /judge
WORKDIR /judge
RUN pip install -r requirements.txt
