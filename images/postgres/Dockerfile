FROM postgres:latest
ENV POSTGRES_DB aiochat
ENV POSTGRES_USER aiochat
ENV POSTGRES_PASSWORD password

ADD initial.sql /docker-entrypoint-initdb.d/
