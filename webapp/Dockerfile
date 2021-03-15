FROM python:3.7-alpine3.9

COPY . /src
WORKDIR /src

RUN apk add --update --no-cache build-base nginx openssl curl unzip supervisor jpeg-dev zlib-dev postgresql-dev freetype-dev nodejs npm tmux&& \
    pip install --no-cache-dir -r /src/requirements.txt && \
    apk del build-base --purge

ENTRYPOINT /src/deploy/entrypoint.sh
