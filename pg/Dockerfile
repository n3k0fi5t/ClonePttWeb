FROM postgres:10-alpine

WORKDIR /src

ENV SCWS_HOME=/usr/local/scws/

RUN apk add --no-cache build-base postgresql-dev git

RUN wget -q -O - http://www.xunsearch.com/scws/down/scws-1.2.2.tar.bz2 | tar xvjf - && \
	cd scws-1.2.2 && ./configure --prefix=/usr/local/scws && make && make install

RUN git clone https://github.com/amutu/zhparser.git && cd ./zhparser && make && make install

COPY init.sql /docker-entrypoint-initdb.d/
