FROM python:3.9-slim

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN set -eux \
 && apk add --no-cache build-base \
 && pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir --trusted-host pypi.python.org -r /src/requirements.txt \
 && apk del build-base \
 && rm -rf /root/.cache/pip

COPY . /src