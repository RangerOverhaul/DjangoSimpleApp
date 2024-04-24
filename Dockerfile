FROM python:3.11
LABEL authors="Danilo Herazo A"

ENV PYTHONUNBUFFERED 1

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

COPY . /code/
