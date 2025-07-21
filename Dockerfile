FROM python:3.9-alpine

WORKDIR /app

# requirements.txt をコピーしてインストール
COPY requirements.txt .

# ビルドツールと Python パッケージのインストール
RUN set -eux \
 && apk add --no-cache build-base \
 && pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt \
 && apk del build-base \
 && rm -rf /root/.cache/pip

# アプリケーションコードをコピー
COPY ./app ./app