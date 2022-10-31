FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt requirements.txt

RUN apt-get update
RUN apt-get -y install gcc

RUN python -m venv venv
CMD ['source', 'venv/bin/activate']

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000

COPY . /code/

