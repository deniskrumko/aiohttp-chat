# aiohttp-chat

Simple chat backend on `aiohttp` and `postgres`.

## How to run with docker and fabric3

1. Install `fabric3` globally or in virtual env

2. Build images

  ```
  fab build
  ```

3. Run containers `db` and then `web`. `db` always must be first.

  ```
  fab db
  fab web
  ```

  Also you can run both containers as daemons like that:

  ```
  fab db:1
  fab web:1
  ```

## How to run with docker only

1. Build images

  ```
  docker build -t aiochatdb:latest images/postgres
  docker build -t aiochatweb:latest .
  ```

2. Run containers `db` and then `web` as daemons. `db` always must be first.

  ```
  docker-compose up -d db
  docker-compose up -d web
  ```

## How to run it without docker

1. Clone repository

  ```
  git clone git@github.com:deniskrumko/aiohttp-chat.git
  ```

2. Create `virtualenv` and install `fabric3`

  ```
  mkvirtualenv aiohttp-chat -p python3.6
  pip install fabric3
  ```

3. Install requirements

  ```
  fab requirements
  ```

4. Create database `aiochat` and populate it with data

  ```
  psql -c 'create database aiochat'
  psql aiochat < images/postgres/initial.sql
  ```

  Do not worry about `role "aiochat" does not exist`. It happens.

5. Run app

  ```
  fab run
  ```
