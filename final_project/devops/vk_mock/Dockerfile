# syntax=docker/dockerfile:1

FROM python:3-alpine3.10

WORKDIR /

COPY . .

RUN pip3 install flask
RUN pip3 install requests

ENTRYPOINT [ "python3", "flask_stub.py"]