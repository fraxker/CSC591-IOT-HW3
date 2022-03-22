# syntax=docker/dockerfile:1

FROM python:3.10.2-slim-bullseye

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt
CMD [ "python3", "laptop_2.py" ]