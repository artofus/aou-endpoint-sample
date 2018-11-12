FROM python:3.7-alpine3.7

RUN apk update && \
   apk add --no-cache gcc musl-dev && \
   apk add --no-cache build-base && \
   apk add openssl

WORKDIR /endpoint
COPY source/requirements.txt ./
RUN pip3 install -r requirements.txt

RUN mkdir scripts cert logs

COPY /scripts/container_init.sh /scripts/init.sh
COPY /source/server.py ./server.py

ENTRYPOINT /scripts/init.sh


