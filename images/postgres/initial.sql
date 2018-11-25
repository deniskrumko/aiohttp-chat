CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
  id              SERIAL PRIMARY KEY,
  username        VARCHAR(255) NOT NULL UNIQUE,
  password        VARCHAR(255) NOT NULL,
  email           VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS messages (
  id              SERIAL PRIMARY KEY,
  sender_id       INTEGER NOT NULL,
  recipient_id    INTEGER NOT NULL,
  message         VARCHAR,
  created         TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  read            BOOLEAN NOT NULL DEFAULT FALSE,
  FOREIGN KEY (sender_id) REFERENCES users (id),
  FOREIGN KEY (recipient_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS tokens (
  token         VARCHAR(64) PRIMARY KEY UNIQUE,
  user_id       INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

ALTER TABLE users OWNER TO aiochat;
ALTER TABLE messages OWNER TO aiochat;
ALTER TABLE tokens OWNER TO aiochat;
