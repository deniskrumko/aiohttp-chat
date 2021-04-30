# aiohttp-chat

Simple chat backend.

**☠️ THIS PROJECT IS NO LONGER SUPPORTED ☠️**

## Requirements

  * python >= 3.6
  * postgres >= 11.1
  * aiohttp >= 3.4.4

## About

This is a test project from one of my interviews:
* Code quality is not garanteed
* No tests at all
* I don't remember how it properly works

---

## How to run with docker and fabric3

1. Install `fabric3` globally or in virtual env

2. Build images

  ```
  fab build
  ```

3. Run containers `db` and then `web`. Container `db` always must be first.

  ```
  fab db
  fab web
  ```

  Also you can run both containers as **daemons** like that:

  ```
  fab db:1
  fab web:1
  ```

4. Stop containers by `fab stop`


## How to run with docker only

1. Build images

  ```
  docker build -t aiochatdb:latest images/postgres
  docker build -t aiochatweb:latest .
  ```

2. Run containers `db` and then `web` as daemons. Container `db` always must be first.

  ```
  docker-compose up -d db
  docker-compose up -d web
  ```

3. Stop containers by `docker-compose stop`

---

## How to run it without docker

1. Create `virtualenv` and install `fabric3`

  ```
  mkvirtualenv aiohttp-chat -p python3.6
  pip install fabric3
  ```

2. Install requirements

  ```
  fab requirements
  ```

3. Create database `aiochat` and populate it with data

  ```
  psql -c 'create database aiochat'
  psql aiochat < images/postgres/initial.sql
  ```

  Do not worry about `role "aiochat" does not exist`. It happens.

4. Run app

  ```
  fab run
  ```

---

## Available API endpoints

All endpoints, except `login` and `signup` require `token` parameter for authentication.

### Authentication

  * POST `/login` - login to app (get API token)
  * POST `/logout` - logout from app (remove API token)
  * POST `/signup` - create new account and auto log in (returns token too)

### Users

  * GET `/users` - list of all users (except current one)
  * GET `/users?type=active` - list of active users (except current one)
  * GET `/users?type=inactive` - list of inactive users (except current one)
  * GET `/current_user` - info about current user

### Send messages
  * POST `/send` - send message to user
  * POST `/send_to_all` - send message to all users

## Chats

  * GET `/chat` - list of available chats
  * GET `/chat/<user_id>` - see chat with specified user

### Other

  * POST `/read/<user_id>` - mark messages from user as read. Note, that only messages, where current user is recipient are updated (not all messages in the chat).

---

## Positive scenario to test

1. `user_1` signs up and logs out
2. `user_2` signs up too
3. `user_1` logs in
4. `user_1` gets active users and finds `user_2`
5. `user_1` sends message `Hello, user_2` to `user_2`
6. `user_2` gets list of chats and sees chat with `user_1`
7. `user_2` gets chat with `user_1` and sees last message
8. `user_2` marks messages with `user_1` as read
9. `user_1` and `user_2` are happy
